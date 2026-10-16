"""
Unified Processing Pipeline Runner for Indian Sign Language (ISL) Projects.
Provides an extensible CLI interface to execute, monitor, and verify all
data processing, feature extraction, model retraining, and asset compilation pipelines.
"""

import os
import sys
import argparse
import time
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def banner(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def cmd_verify():
    """Verify integrity of dataset, models, dictionaries, and image assets."""
    banner("ISL Project Health & Asset Verification")
    
    checks = []
    
    # 1. Dataset CSV
    csv_path = os.path.join(PROJECT_ROOT, "data", "isl_landmarks.csv")
    if os.path.exists(csv_path):
        size_mb = os.path.getsize(csv_path) / (1024 * 1024)
        with open(csv_path, "r", encoding="utf-8") as f:
            lines = sum(1 for _ in f) - 1
        checks.append((True, f"Dataset CSV: {csv_path} ({lines:,} samples, {size_mb:.2f} MB)"))
    else:
        checks.append((False, f"Dataset CSV not found at: {csv_path}"))

    # 2. Model artifacts
    model_files = [
        ("Classifier Pickle", "models/isl_classifier.pkl"),
        ("Label Encoder", "models/label_encoder.pkl"),
        ("Classes JSON", "models/isl_classes.json"),
        ("Metrics JSON", "models/model_metrics.json"),
    ]
    for name, rel in model_files:
        p = os.path.join(PROJECT_ROOT, rel)
        if os.path.exists(p):
            sz = os.path.getsize(p)
            checks.append((True, f"Model Artifact [{name}]: {rel} ({sz / 1024:.1f} KB)"))
        else:
            checks.append((False, f"Missing Model Artifact: {rel}"))

    # 3. Model metrics summary
    metrics_path = os.path.join(PROJECT_ROOT, "models", "model_metrics.json")
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                m = json.load(f)
            acc = m.get("accuracy", 0) * 100
            f1 = m.get("f1_score", 0) * 100
            classes = m.get("num_classes", 0)
            checks.append((True, f"Model Accuracy: {acc:.2f}% | F1-Score: {f1:.2f}% across {classes} classes"))
        except Exception as e:
            checks.append((False, f"Error reading metrics JSON: {e}"))

    # 4. Sign dictionary assets
    signs_dir = os.path.join(PROJECT_ROOT, "static", "assets", "signs")
    if os.path.exists(signs_dir):
        sign_imgs = [f for f in os.listdir(signs_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        total_sz = sum(os.path.getsize(os.path.join(signs_dir, f)) for f in sign_imgs) / (1024 * 1024)
        checks.append((True, f"Sign Reference Images: {len(sign_imgs)} images ({total_sz:.2f} MB total in static/assets/signs)"))
    else:
        checks.append((False, f"Missing signs directory: {signs_dir}"))

    # 5. Video demonstrations
    vids_dir = os.path.join(PROJECT_ROOT, "Images", "isl_videos")
    if os.path.exists(vids_dir):
        vids = [f for f in os.listdir(vids_dir) if f.lower().endswith('.mp4')]
        checks.append((True, f"ISL Demonstration Videos: {len(vids)} MP4 files in Images/isl_videos"))
    else:
        checks.append((False, f"Missing videos directory: {vids_dir}"))

    # Print summary
    print("-" * 70)
    for ok, msg in checks:
        status = "[ OK ]" if ok else "[FAIL]"
        print(f" {status}  {msg}")
    print("-" * 70)
    
    all_ok = all(c[0] for c in checks)
    if all_ok:
        print("\nAll core project assets and models verified successfully!")
    else:
        print("\nSome components require attention or generation.")
    return all_ok


def cmd_train():
    """Retrain the ISL Random Forest classifier and output metrics."""
    banner("Running ISL Model Training & Metric Evaluation")
    t0 = time.time()
    from ml_pipeline.model_trainer import train_isl_model
    results = train_isl_model()
    dt = time.time() - t0
    print(f"\nTraining completed in {dt:.2f} seconds!")
    print(f"Validation Accuracy: {results.get('accuracy', 0)*100:.2f}%")
    f1_val = results.get('f1') or results.get('f1_score') or 0.0
    print(f"Weighted F1-Score:   {f1_val*100:.2f}%")
    return results


def cmd_extract_uploaded():
    """Extract MediaPipe landmark features from Images/A-Z and Images/0-9."""
    banner("Extracting Landmark Features from Uploaded Sign Images")
    t0 = time.time()
    from ml_pipeline.extract_uploaded_images import process_uploaded_images
    total = process_uploaded_images()
    dt = time.time() - t0
    print(f"\nCompleted uploaded image processing in {dt:.2f} seconds! Added {total} samples.")
    return total


def cmd_build_dict():
    """Compile and synchronize ISL sign definitions and video mappings."""
    banner("Compiling Master ISL Sign Dictionary")
    from ml_pipeline.build_isl_dictionary import generate_dictionary
    full_dict = generate_dictionary()
    print(f"\nDictionary compiled successfully with {len(full_dict)} entries!")
    return full_dict


def cmd_render_landmarks():
    """Generate 3D skeletal landmark visualizer diagrams."""
    banner("Rendering Publication-Grade MediaPipe 3D Landmark Diagrams")
    from ml_pipeline.render_mediapipe_landmarks import (
        render_publication_diagram,
        render_dark_cyberpunk_diagram,
        render_minimal_vector_diagram
    )
    render_publication_diagram()
    render_dark_cyberpunk_diagram()
    render_minimal_vector_diagram()
    print("\nRendered 3D MediaPipe landmark diagrams in thesis Figures and Images!")


def cmd_full_pipeline():
    """Execute the complete end-to-end processing pipeline."""
    banner("STARTING FULL END-TO-END PROCESSING PIPELINE")
    start = time.time()
    
    print("\n--- STEP 1/4: Feature Extraction from Custom Images ---")
    cmd_extract_uploaded()

    print("\n--- STEP 2/4: Retraining Classifier & Evaluating Metrics ---")
    cmd_train()

    print("\n--- STEP 3/4: Building ISL Dictionary & Video Mappings ---")
    cmd_build_dict()

    print("\n--- STEP 4/4: Rendering Skeletal Keypoint Visualizations ---")
    cmd_render_landmarks()

    elapsed = time.time() - start
    banner(f"FULL PIPELINE EXECUTION COMPLETED IN {elapsed:.2f} SECONDS")
    cmd_verify()


def main():
    parser = argparse.ArgumentParser(
        description="ISL Project Processing & Machine Learning Pipeline Runner"
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="verify",
        choices=[
            "verify",
            "train",
            "extract-uploaded",
            "build-dict",
            "render-landmarks",
            "full-pipeline"
        ],
        help="Action to perform (default: verify)"
    )

    args = parser.parse_args()

    if args.action == "verify":
        cmd_verify()
    elif args.action == "train":
        cmd_train()
    elif args.action == "extract-uploaded":
        cmd_extract_uploaded()
    elif args.action == "build-dict":
        cmd_build_dict()
    elif args.action == "render-landmarks":
        cmd_render_landmarks()
    elif args.action == "full-pipeline":
        cmd_full_pipeline()


if __name__ == "__main__":
    main()
