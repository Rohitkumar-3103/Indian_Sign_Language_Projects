"""
Extract Landmarks from Images/data/ for Model Training.
Samples diverse images across the 35 classes in Images/data (1-9, A-Z),
extracts invariant 156-dim MediaPipe 3D hand landmarks,
and appends them to data/isl_landmarks.csv.
"""

import os
import cv2
import csv
import numpy as np
import mediapipe as mp
from ml_pipeline.feature_extractor import build_feature_vector

def extract_from_dataset_folder(
    dataset_dir="Images/data",
    output_csv="data/isl_landmarks.csv",
    samples_per_class=20,
    augmentations=4
):
    if not os.path.exists(dataset_dir):
        print(f"Error: {dataset_dir} does not exist.")
        return 0

    print("Initializing MediaPipe Hands for Images/data extraction...")
    mp_hands = mp.solutions.hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.3
    )

    classes = sorted([d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))])
    print(f"Found {len(classes)} classes in {dataset_dir}: {classes}")

    total_added = 0
    rows = []

    for label in classes:
        folder = os.path.join(dataset_dir, label)
        all_files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if not all_files:
            continue

        # Sample evenly across the file list (e.g., indices spread across 0 to len)
        step = max(1, len(all_files) // samples_per_class)
        chosen_files = all_files[::step][:samples_per_class]

        class_samples = 0

        for fname in chosen_files:
            fpath = os.path.join(folder, fname)
            img = cv2.imread(fpath)
            if img is None:
                continue

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = mp_hands.process(rgb)

            if not res.multi_hand_landmarks:
                continue

            hands_landmarks = []
            for idx, hand_lms in enumerate(res.multi_hand_landmarks):
                raw_pts = [[lm.x, lm.y, lm.z] for lm in hand_lms.landmark]
                handedness = "Right"
                if res.multi_handedness and idx < len(res.multi_handedness):
                    handedness = res.multi_handedness[idx].classification[0].label
                hands_landmarks.append({"label": handedness, "landmarks": raw_pts})

            h1 = hands_landmarks[0]["landmarks"] if len(hands_landmarks) > 0 else None
            h2 = hands_landmarks[1]["landmarks"] if len(hands_landmarks) > 1 else None

            # Base features
            base_feats = build_feature_vector(h1, h2)
            rows.append(list(base_feats) + [label.upper()])
            class_samples += 1
            total_added += 1

            # Augmentations
            for _ in range(augmentations):
                h1_aug = None
                h2_aug = None

                if h1 is not None:
                    noise = np.random.normal(0, 0.015, (len(h1), 3))
                    h1_aug = (np.array(h1) + noise).tolist()

                if h2 is not None:
                    noise = np.random.normal(0, 0.015, (len(h2), 3))
                    h2_aug = (np.array(h2) + noise).tolist()

                aug_feats = build_feature_vector(h1_aug, h2_aug)
                rows.append(list(aug_feats) + [label.upper()])
                class_samples += 1
                total_added += 1

        print(f"[{label.upper()}] Processed {len(chosen_files)} raw images -> Generated {class_samples} landmark samples")

    # Append to CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    mp_hands.close()
    print(f"\nSuccessfully added {total_added} high-quality samples from Images/data to {output_csv}!")
    return total_added

if __name__ == "__main__":
    extract_from_dataset_folder()
