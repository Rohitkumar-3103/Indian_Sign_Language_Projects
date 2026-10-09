"""
Indian Sign Language (ISL) Interactive Webcam Dataset Collector.
Captures webcam gesture frames, extracts MediaPipe landmarks, and saves both:
1. Raw image frames to Images/<Category>/<Class>/
2. Normalized 156-element feature vectors to data/isl_landmarks.csv
"""

import os
import cv2
import csv
import time
import argparse
import numpy as np
try:
    from ml_pipeline.isl_dictionary import ISL_CLASSES, get_class_info
    from ml_pipeline.feature_extractor import ISLFeatureExtractor
    from ml_pipeline.model_trainer import train_isl_model
except ImportError:
    from isl_dictionary import ISL_CLASSES, get_class_info
    from feature_extractor import ISLFeatureExtractor
    from model_trainer import train_isl_model

def get_category_for_label(label):
    info = get_class_info(label)
    cat = info.get("category", "alphabet")
    if cat == "alphabet":
        return "A-Z"
    elif cat == "number":
        return "0-9"
    else:
        return "Words"

def run_collector(
    target_class="A",
    samples_to_collect=40,
    camera_index=0,
    output_csv="data/isl_landmarks.csv"
):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    category_folder = get_category_for_label(target_class)
    img_dir = os.path.join("Images", category_folder, target_class)
    os.makedirs(img_dir, exist_ok=True)

    extractor = ISLFeatureExtractor(static_image_mode=False)
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        return

    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Initialize CSV if not exists
    if not os.path.exists(output_csv):
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([f"f_{i}" for i in range(156)] + ["label"])

    info = get_class_info(target_class)
    collected_count = 0
    state = "READY" # READY, COUNTDOWN, RECORDING
    countdown_start = 0
    countdown_duration = 3.0
    last_capture_time = 0
    capture_interval = 0.08 # ~12 fps burst

    print("=" * 60)
    print(f"ISL Dataset Collector - Target Class: [{target_class}]")
    print(f"Name: {info.get('name')}")
    print(f"Category: {info.get('category')} | Hands Required: {info.get('hands')}")
    print(f"Description: {info.get('description')}")
    print("Controls: [SPACE]=Start Capture | [C]=Change Class | [T]=Train | [Q]=Quit")
    print("=" * 60)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab camera frame.")
            break

        frame = cv2.flip(frame, 1) # Mirror preview
        h, w = frame.shape[:2]

        # Extract features and landmark coordinates
        features, hands_data = extractor.extract_features_from_image(frame)

        # Draw MediaPipe hand landmarks skeleton
        display_frame = frame.copy()
        display_frame = extractor.draw_landmarks_on_frame(display_frame, hands_data)

        # Top HUD Banner
        cv2.rectangle(display_frame, (0, 0), (w, 75), (15, 23, 42), -1) # Dark Slate
        cv2.putText(display_frame, f"CLASS: {target_class} ({info.get('name')})", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (16, 185, 129), 2)
        cv2.putText(display_frame, f"Hands: {hands_data.get('num_hands', 0)} / {info.get('hands', 1)} detected | Progress: {collected_count}/{samples_to_collect}",
                    (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

        # State Handling
        curr_time = time.time()
        if state == "COUNTDOWN":
            elapsed = curr_time - countdown_start
            remaining = countdown_duration - elapsed
            if remaining > 0:
                text = f"Get Ready... {int(remaining) + 1}"
                cv2.putText(display_frame, text, (w//2 - 140, h//2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 165, 255), 3)
            else:
                state = "RECORDING"
                last_capture_time = curr_time

        elif state == "RECORDING":
            cv2.rectangle(display_frame, (w - 170, 15), (w - 15, 55), (0, 0, 220), -1)
            cv2.putText(display_frame, "RECORDING", (w - 155, 42),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

            if hands_data.get("num_hands", 0) > 0 and (curr_time - last_capture_time >= capture_interval):
                last_capture_time = curr_time

                # Save raw image
                timestamp = int(curr_time * 1000)
                img_path = os.path.join(img_dir, f"sample_{timestamp}.jpg")
                cv2.imwrite(img_path, frame)

                # Append feature vector to CSV
                with open(output_csv, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(list(features) + [target_class])

                collected_count += 1

                if collected_count >= samples_to_collect:
                    state = "READY"
                    print(f"Finished capturing {samples_to_collect} samples for class {target_class}!")

        # Bottom Instructions Banner
        cv2.rectangle(display_frame, (0, h - 45), (w, h), (15, 23, 42), -1)
        tip_text = f"Tip: {info.get('tips', 'Hold hands clearly inside frame')[:65]}"
        cv2.putText(display_frame, tip_text, (15, h - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        cv2.putText(display_frame, "[SPACE] Record | [C] Change | [T] Train | [Q] Quit", (15, h - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 200, 255), 1)

        cv2.imshow("ISL Dataset Collector", display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == 27:
            break
        elif key == 32: # SPACE
            if state == "READY":
                state = "COUNTDOWN"
                countdown_start = time.time()
                collected_count = 0
        elif key == ord('t'):
            print("Triggering model training...")
            train_isl_model(csv_path=output_csv)
        elif key == ord('c'):
            print("\nEnter new class label (e.g. A-Z, 0-9, HELLO, THANK_YOU, etc.):")
            cv2.destroyAllWindows()
            new_label = input("Class label: ").strip().upper()
            if new_label in ISL_CLASSES:
                target_class = new_label
                info = get_class_info(target_class)
                category_folder = get_category_for_label(target_class)
                img_dir = os.path.join("Images", category_folder, target_class)
                os.makedirs(img_dir, exist_ok=True)
                collected_count = 0
                state = "READY"
            else:
                print(f"Unknown class '{new_label}'. Keeping '{target_class}'")

    cap.release()
    cv2.destroyAllWindows()
    extractor.close()
    print("Collector closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ISL Interactive Dataset Collector")
    parser.add_argument("--class_label", type=str, default="A", help="Target gesture class")
    parser.add_argument("--samples", type=int, default=40, help="Number of samples to collect")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    args = parser.parse_args()

    run_collector(
        target_class=args.class_label.upper(),
        samples_to_collect=args.samples,
        camera_index=args.camera
    )
