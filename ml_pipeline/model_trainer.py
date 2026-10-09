"""
Model Trainer for Indian Sign Language (ISL) Recognition.
Trains multi-class classifiers (Random Forest & MLP Neural Network) on extracted landmark features,
computes comprehensive evaluation metrics, and saves deployment artifacts.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)
try:
    from ml_pipeline.isl_dictionary import ISL_CLASSES
except ImportError:
    from isl_dictionary import ISL_CLASSES

def train_isl_model(
    csv_path="data/isl_landmarks.csv",
    output_dir="models",
    model_type="random_forest",
    test_size=0.2,
    random_state=42
):
    """
    Train an ISL classifier on landmark CSV data and save artifacts.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset CSV not found at: {csv_path}")

    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)

    if "label" not in df.columns:
        raise ValueError("Dataset CSV must have a 'label' column.")

    feature_cols = [c for c in df.columns if c != "label"]
    X = df[feature_cols].values.astype(np.float32)
    y_raw = df["label"].values

    class_counts = pd.Series(y_raw).value_counts().to_dict()
    unique_classes = sorted(list(set(y_raw)))
    print(f"Total samples: {len(X)}, Feature dimensions: {X.shape[1]}, Classes: {len(unique_classes)}")

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    class_mapping = {int(idx): str(cls_name) for idx, cls_name in enumerate(label_encoder.classes_)}

    # Stratified Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples")

    # Select and train model
    if model_type == "mlp":
        print("Training Multi-Layer Perceptron (MLP) Neural Network...")
        model = MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation="relu",
            max_iter=350,
            alpha=0.0005,
            early_stopping=True,
            random_state=random_state
        )
    else:
        print("Training Random Forest Classifier (Ensemble)...")
        model = RandomForestClassifier(
            n_estimators=160,
            max_depth=25,
            min_samples_split=2,
            n_jobs=-1,
            random_state=random_state
        )

    model.fit(X_train, y_train)

    # Predictions & Evaluation
    y_pred = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))

    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average="weighted", zero_division=0
    )

    cm = confusion_matrix(y_test, y_pred)
    report_dict = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True, zero_division=0)

    print(f"Model Training Completed!")
    print(f"Validation Accuracy: {accuracy * 100:.2f}%")
    print(f"Weighted F1-Score:   {f1 * 100:.2f}%")

    # Save Model Artifacts
    model_path = os.path.join(output_dir, "isl_classifier.pkl")
    encoder_path = os.path.join(output_dir, "label_encoder.pkl")
    classes_json_path = os.path.join(output_dir, "isl_classes.json")
    metrics_json_path = os.path.join(output_dir, "model_metrics.json")

    joblib.dump(model, model_path)
    joblib.dump(label_encoder, encoder_path)

    # Class metadata with dictionary info
    classes_meta = {}
    for idx, name in class_mapping.items():
        dict_info = ISL_CLASSES.get(name, {})
        classes_meta[name] = {
            "index": idx,
            "category": dict_info.get("category", "custom"),
            "hands": dict_info.get("hands", 1),
            "name": dict_info.get("name", name),
            "description": dict_info.get("description", ""),
            "tips": dict_info.get("tips", ""),
            "sample_count": class_counts.get(name, 0)
        }

    with open(classes_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "classes": class_mapping,
            "metadata": classes_meta,
            "num_classes": len(unique_classes),
            "num_features": X.shape[1]
        }, f, indent=2)

    # Metrics JSON
    metrics_data = {
        "model_type": model_type,
        "accuracy": accuracy,
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "total_samples": int(len(X)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "num_classes": len(unique_classes),
        "class_counts": class_counts,
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict
    }

    with open(metrics_json_path, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)

    print(f"Artifacts successfully saved to {output_dir}/")
    return {
        "accuracy": accuracy,
        "f1": f1,
        "num_classes": len(unique_classes),
        "total_samples": len(X)
    }

if __name__ == "__main__":
    train_isl_model()
