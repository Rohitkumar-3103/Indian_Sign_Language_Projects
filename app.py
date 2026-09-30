"""
Indian Sign Language (ISL) Recognition - Flask Web Application & Backend API.
Provides real-time gesture recognition, dataset management, model retraining,
and interactive sign learning dictionary endpoints.
"""

import os
import sys
import json
import base64
import time
import csv
import cv2
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS

from ml_pipeline.isl_dictionary import ISL_CLASSES, get_class_info
from ml_pipeline.feature_extractor import ISLFeatureExtractor, build_feature_vector
from ml_pipeline.model_trainer import train_isl_model

# Flask app initialization
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Global ML Model & Extractor State
MODEL_PATH = "models/isl_classifier.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
CLASSES_PATH = "models/isl_classes.json"
METRICS_PATH = "models/model_metrics.json"
DATASET_CSV = "data/isl_landmarks.csv"

classifier = None
label_encoder = None
class_metadata = {}
extractor = None

# Indian-Sign-Language-Detection-main Keras Model Integration
import string
KERAS_MODEL_PATH = "Indian-Sign-Language-Detection-main/model.h5"
keras_model = None
KERAS_CLASSES = ['1','2','3','4','5','6','7','8','9'] + list(string.ascii_uppercase)

def load_artifacts():
    global classifier, label_encoder, class_metadata, keras_model
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
            classifier = joblib.load(MODEL_PATH)
            label_encoder = joblib.load(ENCODER_PATH)
            print(f"Loaded classifier model with {len(label_encoder.classes_)} classes.")
        if os.path.exists(CLASSES_PATH):
            with open(CLASSES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                class_metadata = data.get("metadata", {})
    except Exception as e:
        print(f"Error loading model artifacts: {e}")

    # Load Keras Deep Neural Network from Indian-Sign-Language-Detection-main
    if os.path.exists(KERAS_MODEL_PATH):
        try:
            from tensorflow import keras
            keras_model = keras.models.load_model(KERAS_MODEL_PATH)
            print(f"Loaded Keras Deep Neural Network model from {KERAS_MODEL_PATH} (35 classes).")
        except Exception as e:
            print(f"Notice: Keras model loading deferred: {e}")

def predict_keras_landmarks(raw_pts):
    """Predicts gesture class using the 42-dim Keras Deep Neural Network model."""
    if keras_model is None or not raw_pts or len(raw_pts) < 21:
        return None
    try:
        coords = []
        base_x, base_y = raw_pts[0][0], raw_pts[0][1]
        for pt in raw_pts[:21]:
            coords.append(pt[0] - base_x)
            coords.append(pt[1] - base_y)
        max_val = max(map(abs, coords)) if max(map(abs, coords)) > 1e-4 else 1.0
        norm_42 = [c / max_val for c in coords]
        preds = keras_model.predict(np.array([norm_42], dtype=np.float32), verbose=0)[0]
        top_idx = int(np.argmax(preds))
        return {
            "label": KERAS_CLASSES[top_idx],
            "confidence": round(float(preds[top_idx]), 3)
        }
    except Exception as e:
        return None

# Initialize extractor and load models
extractor = ISLFeatureExtractor(static_image_mode=False)
load_artifacts()

# ----------------- Helper Functions -----------------

def get_dataset_stats():
    """Count samples per class from CSV file."""
    stats = {}
    total = 0
    if os.path.exists(DATASET_CSV):
        try:
            with open(DATASET_CSV, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row:
                        lbl = row[-1]
                        stats[lbl] = stats.get(lbl, 0) + 1
                        total += 1
        except Exception as e:
            print(f"Error reading dataset stats: {e}")
    return stats, total

# ----------------- Web Routes -----------------

@app.route("/")
def index():
    return render_template("index.html")

# ----------------- API Endpoints -----------------

@app.route("/api/status", methods=["GET"])
def api_status():
    stats, total_samples = get_dataset_stats()
    return jsonify({
        "status": "online",
        "model_loaded": classifier is not None,
        "keras_model_loaded": keras_model is not None,
        "num_classes": len(label_encoder.classes_) if label_encoder is not None else 0,
        "total_dataset_samples": total_samples,
        "mediapipe_ready": extractor.hands_detector is not None
    })

@app.route("/api/classes", methods=["GET"])
def api_classes():
    stats, _ = get_dataset_stats()
    result = {}
    for key, info in ISL_CLASSES.items():
        result[key] = {
            "label": key,
            "name": info.get("name", key),
            "category": info.get("category", "alphabet"),
            "hands": info.get("hands", 1),
            "description": info.get("description", ""),
            "tips": info.get("tips", ""),
            "sample_count": stats.get(key, 0)
        }
    return jsonify({
        "classes": result,
        "total_count": len(result)
    })

@app.route("/api/metrics", methods=["GET"])
def api_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Metrics not found. Train the model first."}), 404

# ----------------- Text to Sign Translation API -----------------

WORD_ALIASES = {
    "HI": "HELLO",
    "HEY": "HELLO",
    "NAMASTE": "HELLO",
    "HELLO": "HELLO",
    "THANKS": "THANK_YOU",
    "THANK": "THANK_YOU",
    "THANKYOU": "THANK_YOU",
    "THANK_YOU": "THANK_YOU",
    "YES": "YES",
    "YEAH": "YES",
    "YUP": "YES",
    "HAAN": "YES",
    "NO": "NO",
    "NOPE": "NO",
    "NAHI": "NO",
    "PLEASE": "PLEASE",
    "KRPAYA": "PLEASE",
    "HELP": "HELP",
    "MADAD": "HELP",
    "WATER": "WATER",
    "PANI": "WATER",
    "PAANI": "WATER",
    "FOOD": "FOOD",
    "EAT": "FOOD",
    "KHANA": "FOOD",
    "ILOVEYOU": "ILOVEYOU",
    "LOVE": "ILOVEYOU"
}

@app.route("/api/text_to_sign", methods=["POST"])
def api_text_to_sign():
    """
    Translates input text or transcribed voice into Indian Sign Language (ISL) sequence.
    Handles whole-word signs where available and finger-spells alphabets & digits.
    """
    try:
        data = request.get_json(force=True) or {}
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "Empty text provided"}), 400

        raw_words = text.upper().split()
        sequence = []
        i = 0

        while i < len(raw_words):
            # Check 2-word phrase
            if i + 1 < len(raw_words):
                two_word = f"{raw_words[i]}_{raw_words[i+1]}"
                if two_word in WORD_ALIASES:
                    sign_key = WORD_ALIASES[two_word]
                    meta = ISL_CLASSES.get(sign_key, {})
                    sequence.append({
                        "token": f"{raw_words[i]} {raw_words[i+1]}",
                        "sign_key": sign_key,
                        "is_word": True,
                        "image_url": f"/static/assets/signs/{sign_key}.jpg",
                        "name": meta.get("name", sign_key),
                        "description": meta.get("description", ""),
                        "tips": meta.get("tips", ""),
                        "hands": meta.get("hands", 1)
                    })
                    i += 2
                    continue

            w = raw_words[i]
            clean_w = "".join(ch for ch in w if ch.isalnum() or ch == '_')

            if clean_w in WORD_ALIASES:
                sign_key = WORD_ALIASES[clean_w]
                meta = ISL_CLASSES.get(sign_key, {})
                sequence.append({
                    "token": clean_w,
                    "sign_key": sign_key,
                    "is_word": True,
                    "image_url": f"/static/assets/signs/{sign_key}.jpg",
                    "name": meta.get("name", sign_key),
                    "description": meta.get("description", ""),
                    "tips": meta.get("tips", ""),
                    "hands": meta.get("hands", 1)
                })
            else:
                # Finger spell character by character
                for char in clean_w:
                    if char in ISL_CLASSES:
                        meta = ISL_CLASSES[char]
                        sequence.append({
                            "token": char,
                            "sign_key": char,
                            "is_word": False,
                            "image_url": f"/static/assets/signs/{char}.jpg",
                            "name": meta.get("name", f"Letter {char}"),
                            "description": meta.get("description", ""),
                            "tips": meta.get("tips", ""),
                            "hands": meta.get("hands", 1)
                        })
            i += 1

        return jsonify({
            "original_text": text,
            "total_signs": len(sequence),
            "sequence": sequence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/predict_frame", methods=["POST"])
def api_predict_frame():
    """
    Accepts base64 image, extracts landmarks via server MediaPipe, and predicts gesture.
    """
    if classifier is None or label_encoder is None:
        return jsonify({"error": "Classifier model not initialized"}), 503

    try:
        data = request.get_json(force=True)
        img_data = data.get("image", "")
        if "," in img_data:
            img_data = img_data.split(",", 1)[1]

        image_bytes = base64.b64decode(img_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Could not decode image"}), 400

        features, hands_data = extractor.extract_features_from_image(frame)

        if hands_data["num_hands"] == 0:
            return jsonify({
                "detected": False,
                "prediction": None,
                "confidence": 0.0,
                "message": "No hands detected in frame"
            })

        # Run inference
        probs = classifier.predict_proba([features])[0]
        top_idx = int(np.argmax(probs))
        predicted_label = str(label_encoder.classes_[top_idx])
        confidence = float(probs[top_idx])

        # Top 3 predictions
        top_indices = np.argsort(probs)[::-1][:3]
        top_k = [
            {"label": str(label_encoder.classes_[i]), "confidence": round(float(probs[i]), 3)}
            for i in top_indices if probs[i] > 0.01
        ]

        # Convert hands data pixel points for frontend overlay
        frontend_hands = []
        for h in hands_data["hands"]:
            frontend_hands.append({
                "label": h["label"],
                "score": round(h["score"], 2),
                "bbox": h["bbox"],
                "pixel_pts": h["pixel_pts"]
            })

        return jsonify({
            "detected": True,
            "prediction": predicted_label,
            "confidence": round(confidence, 3),
            "top_k": top_k,
            "hands": frontend_hands,
            "metadata": ISL_CLASSES.get(predicted_label, {})
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/predict_landmarks", methods=["POST"])
def api_predict_landmarks():
    """
    Accepts raw landmark arrays directly from web client (MediaPipe JS),
    constructs feature vector, and predicts gesture with ultra-low latency.
    Payload: { "hands": [ { "label": "Right", "landmarks": [[x,y,z], ...] }, ... ] }
    """
    if classifier is None or label_encoder is None:
        return jsonify({"error": "Classifier model not initialized"}), 503

    try:
        data = request.get_json(force=True)
        hands_in = data.get("hands", [])

        if not hands_in:
            return jsonify({
                "detected": False,
                "prediction": None,
                "confidence": 0.0,
                "message": "No hands detected"
            })

        hand1_pts = None
        hand2_pts = None

        if len(hands_in) == 1:
            hand1_pts = hands_in[0].get("landmarks")
        elif len(hands_in) >= 2:
            # Sort Right to hand1, Left to hand2
            if hands_in[0].get("label") == "Right":
                hand1_pts = hands_in[0].get("landmarks")
                hand2_pts = hands_in[1].get("landmarks")
            elif hands_in[1].get("label") == "Right":
                hand1_pts = hands_in[1].get("landmarks")
                hand2_pts = hands_in[0].get("landmarks")
            else:
                hand1_pts = hands_in[0].get("landmarks")
                hand2_pts = hands_in[1].get("landmarks")

        features = build_feature_vector(hand1_pts, hand2_pts)

        probs = classifier.predict_proba([features])[0]
        top_idx = int(np.argmax(probs))
        predicted_label = str(label_encoder.classes_[top_idx])
        confidence = float(probs[top_idx])

        top_indices = np.argsort(probs)[::-1][:3]
        top_k = [
            {"label": str(label_encoder.classes_[i]), "confidence": round(float(probs[i]), 3)}
            for i in top_indices if probs[i] > 0.01
        ]

        keras_res = None
        if hand1_pts is not None and len(hand1_pts) >= 21:
            keras_res = predict_keras_landmarks(hand1_pts)

        return jsonify({
            "detected": True,
            "prediction": predicted_label,
            "confidence": round(confidence, 3),
            "top_k": top_k,
            "keras_model": keras_res,
            "metadata": ISL_CLASSES.get(predicted_label, {})
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/collect_sample", methods=["POST"])
def api_collect_sample():
    """
    Appends a new sample to the dataset from the web studio.
    Payload: { "label": "A", "features": [156 numbers] } OR { "label": "A", "hands": [...] }
    """
    try:
        data = request.get_json(force=True)
        label = data.get("label", "").upper()
        if not label:
            return jsonify({"error": "Missing label"}), 400

        features = data.get("features", None)
        if features is None and "hands" in data:
            hands_in = data["hands"]
            h1 = hands_in[0].get("landmarks") if len(hands_in) > 0 else None
            h2 = hands_in[1].get("landmarks") if len(hands_in) > 1 else None
            features = list(build_feature_vector(h1, h2))

        if not features or len(features) != 156:
            return jsonify({"error": "Features must contain exactly 156 elements"}), 400

        os.makedirs(os.path.dirname(DATASET_CSV), exist_ok=True)
        file_exists = os.path.exists(DATASET_CSV)

        with open(DATASET_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([f"f_{i}" for i in range(156)] + ["label"])
            writer.writerow(list(features) + [label])

        stats, total = get_dataset_stats()
        return jsonify({
            "success": True,
            "label": label,
            "sample_count": stats.get(label, 0),
            "total_samples": total
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/train", methods=["POST"])
def api_train():
    """
    Triggers model training from web UI and reloads artifacts.
    """
    try:
        data = request.get_json(silent=True) or {}
        model_type = data.get("model_type", "random_forest")

        metrics = train_isl_model(
            csv_path=DATASET_CSV,
            output_dir="models",
            model_type=model_type
        )
        load_artifacts()

        return jsonify({
            "success": True,
            "message": "Model trained and loaded successfully!",
            "accuracy": round(metrics["accuracy"] * 100, 2),
            "f1_score": round(metrics["f1"] * 100, 2),
            "classes": metrics["num_classes"],
            "total_samples": metrics["total_samples"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------- MJPEG Camera Streaming Route -----------------

def generate_video_stream():
    """Generator for streaming live OpenCV video with HUD annotations."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        features, hands_data = extractor.extract_features_from_image(frame)
        frame = extractor.draw_landmarks_on_frame(frame, hands_data)

        if classifier and hands_data["num_hands"] > 0:
            probs = classifier.predict_proba([features])[0]
            top_idx = int(np.argmax(probs))
            label = str(label_encoder.classes_[top_idx])
            conf = float(probs[top_idx])

            # Draw HUD
            cv2.rectangle(frame, (10, 10), (320, 65), (15, 23, 42), -1)
            cv2.putText(frame, f"Sign: {label} ({int(conf*100)}%)", (20, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (16, 185, 129), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route("/video_feed")
def video_feed():
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("=" * 60)
    print("Indian Sign Language (ISL) Recognition Web Server")
    print("Access application at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)
