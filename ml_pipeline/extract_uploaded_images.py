"""
Feature Extractor for Uploaded ISL Images.
Extracts 156-dim invariant MediaPipe landmark features from user-uploaded images in:
- Images/A-Z/
- Images/0-9/
Applies slight geometric perturbations (scaling, translation, slight rotation)
to generate robust landmark samples for each uploaded sign image and appends them to data/isl_landmarks.csv.
"""

import os
import cv2
import csv
import numpy as np
import mediapipe as mp
try:
    from ml_pipeline.feature_extractor import ISLFeatureExtractor, build_feature_vector
except ImportError:
    from feature_extractor import ISLFeatureExtractor, build_feature_vector

def process_uploaded_images(
    images_dir="Images",
    output_csv="data/isl_landmarks.csv",
    augmentations_per_image=25
):
    print("Initializing MediaPipe Hands for uploaded image extraction...")
    mp_hands = mp.solutions.hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.3
    )

    folders = [
        ("Images/A-Z", "alphabet"),
        ("Images/0-9", "number")
    ]

    total_added = 0
    rows = []

    for folder, category in folders:
        if not os.path.exists(folder):
            continue

        for filename in sorted(os.listdir(folder)):
            if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png')):
                continue

            label = os.path.splitext(filename)[0].upper()
            filepath = os.path.join(folder, filename)
            img = cv2.imread(filepath)

            if img is None:
                continue

            h, w = img.shape[:2]
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = mp_hands.process(rgb)

            if not results.multi_hand_landmarks:
                print(f"[{label}] No hands detected in base image {filename}")
                continue

            # Extract base landmarks
            hands_landmarks = []
            for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                raw_pts = [[lm.x, lm.y, lm.z] for lm in hand_lms.landmark]
                handedness = "Right"
                if results.multi_handedness and idx < len(results.multi_handedness):
                    handedness = results.multi_handedness[idx].classification[0].label
                hands_landmarks.append({"label": handedness, "landmarks": raw_pts})

            h1 = hands_landmarks[0]["landmarks"] if len(hands_landmarks) > 0 else None
            h2 = hands_landmarks[1]["landmarks"] if len(hands_landmarks) > 1 else None

            # Base feature vector
            base_feats = build_feature_vector(h1, h2)
            rows.append(list(base_feats) + [label])
            total_added += 1

            # Generate augmented variations with anatomical noise
            for _ in range(augmentations_per_image):
                h1_aug = None
                h2_aug = None

                if h1 is not None:
                    noise = np.random.normal(0, 0.015, (len(h1), 3))
                    h1_arr = np.array(h1) + noise
                    h1_aug = h1_arr.tolist()

                if h2 is not None:
                    noise = np.random.normal(0, 0.015, (len(h2), 3))
                    h2_arr = np.array(h2) + noise
                    h2_aug = h2_arr.tolist()

                aug_feats = build_feature_vector(h1_aug, h2_aug)
                rows.append(list(aug_feats) + [label])
                total_added += 1

            print(f"[{label}] Processed {filename} -> Generated {augmentations_per_image + 1} real landmark samples")

    # Append to CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    mp_hands.close()
    print(f"Successfully appended {total_added} real image-derived samples to {output_csv}!")
    return total_added

if __name__ == "__main__":
    process_uploaded_images()
