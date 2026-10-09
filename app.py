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
import re
import requests
import cv2
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
from flask_cors import CORS

from ml_pipeline.isl_dictionary import ISL_CLASSES, get_class_info
from ml_pipeline.feature_extractor import ISLFeatureExtractor, build_feature_vector
from ml_pipeline.model_trainer import train_isl_model

# Flask app initialization
# Load local .env file if available
_env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_file):
    try:
        with open(_env_file, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())
    except Exception:
        pass

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True
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
KERAS_WEIGHTS_PATH = "Indian-Sign-Language-Detection-main/model_weights.npz"
keras_model = None
keras_np_weights = None
KERAS_CLASSES = ['1','2','3','4','5','6','7','8','9'] + list(string.ascii_uppercase)

def load_artifacts():
    global classifier, label_encoder, class_metadata, keras_model, keras_np_weights
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
        except Exception:
            pass

    # High-speed NumPy engine fallback (pure matrix multiplication)
    if keras_model is None and os.path.exists(KERAS_WEIGHTS_PATH):
        try:
            data = np.load(KERAS_WEIGHTS_PATH)
            keras_np_weights = [
                (data['w_0'], data['b_0']),
                (data['w_1'], data['b_1']),
                (data['w_2'], data['b_2']),
                (data['w_3'], data['b_3']),
                (data['w_4'], data['b_4']),
            ]
            print(f"Loaded Keras 5-layer DNN weights into high-speed NumPy engine (35 classes).")
        except Exception as e:
            print(f"Notice: NumPy weights loading error: {e}")

def predict_keras_landmarks(raw_pts):
    """Predicts gesture class using the 42-dim Deep Neural Network model (Keras or NumPy engine)."""
    if (keras_model is None and keras_np_weights is None) or not raw_pts or len(raw_pts) < 21:
        return None
    try:
        coords = []
        base_x, base_y = raw_pts[0][0], raw_pts[0][1]
        for pt in raw_pts[:21]:
            coords.append(pt[0] - base_x)
            coords.append(pt[1] - base_y)
        max_val = max(map(abs, coords)) if max(map(abs, coords)) > 1e-4 else 1.0
        norm_42 = [c / max_val for c in coords]

        if keras_model is not None:
            preds = keras_model.predict(np.array([norm_42], dtype=np.float32), verbose=0)[0]
        else:
            x = np.array([norm_42], dtype=np.float32)
            for w, b in keras_np_weights[:-1]:
                x = np.maximum(0, np.dot(x, w) + b)
            w_last, b_last = keras_np_weights[-1]
            logits = np.dot(x, w_last) + b_last
            exp_x = np.exp(logits - np.max(logits, axis=1, keepdims=True))
            preds = (exp_x / np.sum(exp_x, axis=1, keepdims=True))[0]

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

@app.route("/favicon.ico")
def favicon():
    if os.path.exists("static/favicon.ico"):
        return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")
    return ("", 204)

# ----------------- API Endpoints -----------------

@app.route("/api/status", methods=["GET"])
def api_status():
    stats, total_samples = get_dataset_stats()
    return jsonify({
        "status": "online",
        "model_loaded": classifier is not None,
        "keras_model_loaded": (keras_model is not None or keras_np_weights is not None),
        "num_classes": len(label_encoder.classes_) if label_encoder is not None else 0,
        "total_dataset_samples": total_samples,
        "total_videos": 203,
        "total_dictionary_signs": len(ISL_CLASSES),
        "raw_images_dataset": 42000,
        "mediapipe_ready": extractor.hands_detector is not None
    })

@app.route("/api/classes", methods=["GET"])
def api_classes():
    stats, total = get_dataset_stats()
    result = {}
    for key, info in ISL_CLASSES.items():
        vfile = info.get("video_file")
        result[key] = {
            "label": key,
            "name": info.get("name", key),
            "category": info.get("category", "alphabet"),
            "hands": info.get("hands", 1),
            "description": info.get("description", ""),
            "tips": info.get("tips", ""),
            "video_url": f"/api/videos/{vfile}" if vfile else None,
            "has_video": bool(info.get("has_video")),
            "image_url": f"/static/assets/signs/{key}.jpg",
            "sample_count": stats.get(key, 0)
        }
    return jsonify({
        "classes": result,
        "total_count": len(result),
        "total_samples": total
    })

@app.route("/api/videos/<path:filename>")
def stream_isl_video(filename):
    """Streams ISL video demonstration clips with HTTP Range support for seeking and looping."""
    videos_dir = os.path.abspath("Images/isl_videos")
    return send_from_directory(videos_dir, filename, mimetype="video/mp4", conditional=True)

@app.route("/research_report")
@app.route("/api/research_report")
def get_research_report():
    """
    Renders the publication-grade comprehensive 16-research-paper survey report.
    Supports ?format=raw or ?format=markdown to retrieve the raw markdown file.
    """
    report_file = os.path.abspath("RESEARCH_PAPERS_COMPREHENSIVE_SURVEY_REPORT.md")
    if not os.path.exists(report_file):
        return jsonify({"error": "Report not found"}), 404

    req_format = request.args.get("format", "").lower()
    if req_format in ("raw", "markdown", "md"):
        return send_from_directory(".", "RESEARCH_PAPERS_COMPREHENSIVE_SURVEY_REPORT.md", mimetype="text/markdown")

    with open(report_file, "r", encoding="utf-8") as f:
        content = f.read()

    response = Response(render_template("research_report.html", report_markdown=content), mimetype="text/html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/research_gallery")
@app.route("/research_gallery/")
def get_research_gallery():
    """Renders the interactive gallery of 189 extracted figures, architectures, and graphs."""
    gallery_dir = os.path.abspath("Research_Paper_images")
    return send_from_directory(gallery_dir, "index.html")

@app.route("/Research_Paper_images/<path:filename>")
@app.route("/research_paper_images/<path:filename>")
@app.route("/research_gallery/<path:filename>")
def serve_research_paper_images(filename):
    """Serves extracted research paper figures, diagrams, and graphs."""
    gallery_dir = os.path.abspath("Research_Paper_images")
    return send_from_directory(gallery_dir, filename)

@app.route("/<folder_name>/<path:filename>")
def serve_paper_folder_fallback(folder_name, filename):
    """Fallback route for relative figure references from root."""
    gallery_dir = os.path.abspath("Research_Paper_images")
    if folder_name.startswith(tuple(f"{i:02d}_" for i in range(1, 25))) or folder_name == "by_category":
        target_dir = os.path.join(gallery_dir, folder_name)
        if os.path.isdir(target_dir):
            return send_from_directory(target_dir, filename)
    return jsonify({"error": "Resource not found"}), 404

@app.route("/notebook")
@app.route("/pipeline_notebook")
def get_pipeline_notebook():
    """Renders the complete pre-executed Jupyter Notebook pipeline in HTML format."""
    return send_from_directory(".", "Indian_Sign_Language_Pipeline.html")

@app.route("/download_notebook")
def download_pipeline_notebook():
    """Downloads the native Jupyter Notebook (.ipynb) file."""
    return send_from_directory(".", "Indian_Sign_Language_Pipeline.ipynb", as_attachment=True)

# ----------------- YouTube & Spoken Video to Sign Translation Engine -----------------
DEFAULT_DEEPGRAM_KEY = os.getenv("DEEPGRAM_API_KEY", "")

def extract_youtube_video_id(url):
    """Extracts 11-char YouTube video ID from various YouTube URL formats."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"embed\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None

def enrich_words_with_isl_assets(words):
    """
    Enriches word timestamp objects with matching ISL full gesture videos,
    static sign vocabulary cards, and alphabet fingerspelling fallback cards.
    """
    enriched = []
    videos_dir = os.path.abspath("Images/isl_videos")
    signs_dir = os.path.abspath("static/assets/signs")
    alpha_dir = os.path.abspath("static/signs")

    for w in words:
        w_text = w.get("word", "").strip()
        clean = re.sub(r"[^a-zA-Z]", "", w_text).upper()
        if not clean:
            continue

        video_filename = f"{clean.lower()}.mp4"
        has_video = os.path.exists(os.path.join(videos_dir, video_filename))
        video_url = f"/api/videos/{video_filename}" if has_video else None

        sign_filename = f"{clean}.jpg"
        has_sign_card = os.path.exists(os.path.join(signs_dir, sign_filename))
        sign_card_url = f"/static/assets/signs/{sign_filename}" if has_sign_card else None

        letters = []
        for char in clean:
            if char.isalpha():
                card_name = f"{char}.jpg"
                has_char = os.path.exists(os.path.join(alpha_dir, card_name))
                img_url = f"/static/signs/{card_name}" if has_char else f"/static/assets/signs/{card_name}"
                letters.append({
                    "char": char,
                    "img_url": img_url
                })

        enriched.append({
            "word": w_text,
            "clean": clean,
            "start": round(float(w.get("start", 0)), 2),
            "end": round(float(w.get("end", 0)), 2),
            "confidence": round(float(w.get("confidence", 1.0)), 2),
            "has_video": has_video,
            "video_url": video_url,
            "has_sign_card": has_sign_card,
            "sign_card_url": sign_card_url,
            "letters": letters
        })
    return enriched

@app.route("/api/youtube_to_sign", methods=["POST"])
def api_youtube_to_sign():
    """
    Downloads audio from YouTube, transcribes with word timestamps via Deepgram API,
    and maps every word to ISL gesture videos and fingerspelling sequences.
    """
    try:
        import yt_dlp
        data = request.get_json(silent=True) or {}
        url = data.get("url", "").strip()
        api_key = data.get("api_key") or DEFAULT_DEEPGRAM_KEY

        if not url:
            return jsonify({"status": "error", "message": "Please provide a valid YouTube URL."}), 400

        video_id = extract_youtube_video_id(url)
        downloads_dir = os.path.abspath("static/downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        audio_filename = f"{video_id or int(time.time()*1000)}.m4a"
        audio_path = os.path.join(downloads_dir, audio_filename)

        title = "YouTube Video"
        if not os.path.exists(audio_path):
            ydl_opts = {
                'format': '140/bestaudio[ext=m4a]/bestaudio',
                'outtmpl': os.path.join(downloads_dir, f"{video_id or int(time.time()*1000)}.%(ext)s"),
                'quiet': True,
                'no_warnings': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "YouTube Video")
                ext = info.get("ext", "m4a")
                audio_path = os.path.join(downloads_dir, f"{video_id or int(time.time()*1000)}.{ext}")

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        ext = os.path.splitext(audio_path)[1].lstrip(".").lower() or "m4a"
        content_type = f"audio/{ext}" if ext != "m4a" else "audio/mp4"

        dg_url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&punctuate=true"
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": content_type
        }
        res = requests.post(dg_url, headers=headers, data=audio_bytes, timeout=60)

        if res.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Deepgram transcription error ({res.status_code}): {res.text}"
            }), 400

        dg_data = res.json()
        alt = dg_data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0]
        transcript = alt.get("transcript", "")
        raw_words = alt.get("words", [])

        enriched_words = enrich_words_with_isl_assets(raw_words)

        return jsonify({
            "status": "success",
            "video_id": video_id,
            "title": title,
            "transcript": transcript,
            "words": enriched_words,
            "total_words": len(enriched_words),
            "audio_url": f"/static/downloads/{os.path.basename(audio_path)}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/youtube_demos", methods=["GET"])
def api_youtube_demos():
    """Returns curated demo clips with pre-computed synchronized word timestamps for instant testing."""
    demos = [
        {
            "id": "demo-welcome",
            "title": "Welcome to Indian Sign Language (Demo)",
            "video_id": "jNQXAC9IVRw",
            "transcript": "Hello and welcome. Here we learn Indian Sign Language together today. Thank you for your work and please help.",
            "words": enrich_words_with_isl_assets([
                {"word": "Hello", "start": 0.5, "end": 1.1},
                {"word": "and", "start": 1.2, "end": 1.4},
                {"word": "welcome.", "start": 1.5, "end": 2.1},
                {"word": "Here", "start": 2.3, "end": 2.8},
                {"word": "we", "start": 2.9, "end": 3.1},
                {"word": "learn", "start": 3.2, "end": 3.7},
                {"word": "Indian", "start": 3.8, "end": 4.4},
                {"word": "Sign", "start": 4.5, "end": 5.0},
                {"word": "Language", "start": 5.1, "end": 5.8},
                {"word": "together", "start": 6.0, "end": 6.6},
                {"word": "today.", "start": 6.7, "end": 7.3},
                {"word": "Thank", "start": 7.5, "end": 7.9},
                {"word": "you", "start": 8.0, "end": 8.4},
                {"word": "for", "start": 8.5, "end": 8.7},
                {"word": "your", "start": 8.8, "end": 9.1},
                {"word": "work", "start": 9.2, "end": 9.8},
                {"word": "and", "start": 9.9, "end": 10.1},
                {"word": "please", "start": 10.2, "end": 10.8},
                {"word": "help.", "start": 11.0, "end": 11.8}
            ])
        }
    ]
    return jsonify({"status": "success", "demos": demos})

@app.route("/api/metrics", methods=["GET"])
def api_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Metrics not found. Train the model first."}), 404

# ----------------- Text to Sign Translation API -----------------

# Initialize WORD_ALIASES with all vocabulary words in ISL_CLASSES
WORD_ALIASES = {k: k for k, v in ISL_CLASSES.items() if v.get("category") == "word"}

# Conversational synonyms & multi-lingual phonetic aliases
WORD_ALIASES.update({
    "HI": "HELLO",
    "HEY": "HELLO",
    "NAMASTE": "HELLO",
    "THANKS": "THANK_YOU",
    "THANK": "THANK_YOU",
    "THANKYOU": "THANK_YOU",
    "DHANYAWAD": "THANK_YOU",
    "YEAH": "YES",
    "YUP": "YES",
    "HAAN": "YES",
    "NOPE": "NO",
    "NAHI": "NO",
    "KRPAYA": "PLEASE",
    "MADAD": "HELP",
    "PANI": "WATER",
    "PAANI": "WATER",
    "KHANA": "FOOD",
    "LOVE": "ILOVEYOU",
    "PYAR": "ILOVEYOU",
    "SWAGAT": "WELCOME",
    "SWAGATAM": "WELCOME",
    "MAAF": "SORRY",
    "APOLOGY": "SORRY",
    "BHARAT": "INDIA",
    "HINDUSTAN": "INDIA",
    "MOM": "MOTHER",
    "MAA": "MOTHER",
    "MATA": "MOTHER",
    "DAD": "FATHER",
    "PAPA": "FATHER",
    "PITA": "FATHER",
    "DOST": "FRIEND",
    "MITRA": "FRIEND",
    "DIDI": "SISTER",
    "BEHEN": "SISTER",
    "PATNI": "WIFE",
    "VIDYALAYA": "SCHOOL",
    "GURU": "TEACHER",
    "SHIKSHAK": "TEACHER",
    "CHATRA": "STUDENT",
    "SIKHO": "LEARN",
    "KAAM": "WORK",
    "KHUSH": "HAPPY",
    "GUSSA": "ANGRY",
    "PEEYO": "DRINK",
    "SONA": "SLEEP",
    "AAJ": "TODAY",
    "KAL": "TOMORROW",
    "KAHAN": "WHERE",
    "KYA": "WHAT",
    "KYUN": "WHY",
    "KAUN": "WHO",
    "KAB": "WHEN",
    "AAP": "YOU",
    "TUM": "YOU",
    "MERA": "MY",
    "TERA": "YOUR",
    "HUM": "WE",
    "ABHI": "RIGHT_NOW",
    "KITNE": "HOW_MANY",
    # 2 and 3 word phrases
    "GOOD_MORNING": "GOOD_MORNING",
    "GOOD_AFTERNOON": "GOOD_AFTERNOON",
    "GOOD_NIGHT": "GOOD_NIGHT",
    "NICE_TO_MEET_YOU": "NICE_TO_MEET_YOU",
    "SEE_YOU_TOMORROW": "SEE_YOU_TOMORROW",
    "HOW_MANY": "HOW_MANY",
    "WHAT_TIME": "WHAT_TIME",
    "WHAT_HAPPENED": "WHAT_HAPPENED",
    "RIGHT_NOW": "RIGHT_NOW",
    "TIME_OUT": "TIME_OUT",
    "BE_BRAVE": "BE_BRAVE",
    "BE_BRAVE_ENOUGH": "BE_BRAVE_ENOUGH",
    "EVERY_TIME": "EVERY_TIME",
    "EXCUSE_ME": "EXCUSE_ME"
})

@app.route("/api/text_to_sign", methods=["POST"])
def api_text_to_sign():
    """
    Translates input text or transcribed voice into Indian Sign Language (ISL) sequence.
    Handles whole-word signs (with HD video demonstration clips) where available
    and finger-spells alphabets & digits.
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
            # Check 3-word phrase
            if i + 2 < len(raw_words):
                three_word = f"{raw_words[i]}_{raw_words[i+1]}_{raw_words[i+2]}"
                if three_word in WORD_ALIASES:
                    sign_key = WORD_ALIASES[three_word]
                    meta = ISL_CLASSES.get(sign_key, {})
                    vfile = meta.get("video_file")
                    sequence.append({
                        "token": f"{raw_words[i]} {raw_words[i+1]} {raw_words[i+2]}",
                        "sign_key": sign_key,
                        "is_word": True,
                        "image_url": f"/static/assets/signs/{sign_key}.jpg",
                        "video_url": f"/api/videos/{vfile}" if vfile else None,
                        "has_video": bool(meta.get("has_video")),
                        "name": meta.get("name", sign_key),
                        "description": meta.get("description", ""),
                        "tips": meta.get("tips", ""),
                        "hands": meta.get("hands", 1)
                    })
                    i += 3
                    continue

            # Check 2-word phrase
            if i + 1 < len(raw_words):
                two_word = f"{raw_words[i]}_{raw_words[i+1]}"
                if two_word in WORD_ALIASES:
                    sign_key = WORD_ALIASES[two_word]
                    meta = ISL_CLASSES.get(sign_key, {})
                    vfile = meta.get("video_file")
                    sequence.append({
                        "token": f"{raw_words[i]} {raw_words[i+1]}",
                        "sign_key": sign_key,
                        "is_word": True,
                        "image_url": f"/static/assets/signs/{sign_key}.jpg",
                        "video_url": f"/api/videos/{vfile}" if vfile else None,
                        "has_video": bool(meta.get("has_video")),
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
                vfile = meta.get("video_file")
                sequence.append({
                    "token": clean_w,
                    "sign_key": sign_key,
                    "is_word": True,
                    "image_url": f"/static/assets/signs/{sign_key}.jpg",
                    "video_url": f"/api/videos/{vfile}" if vfile else None,
                    "has_video": bool(meta.get("has_video")),
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
                        vfile = meta.get("video_file")
                        sequence.append({
                            "token": char,
                            "sign_key": char,
                            "is_word": False,
                            "image_url": f"/static/assets/signs/{char}.jpg",
                            "video_url": f"/api/videos/{vfile}" if vfile else None,
                            "has_video": bool(meta.get("has_video")),
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


def run_isl_inference_engine(hands_list):
    """
    State-of-the-art Multi-Hypothesis Indian Sign Language Inference Engine.
    Handles:
    - Single-hand signs with both direct and horizontally mirrored hypotheses
      (supports left-handed signers and mirrored webcam orientations).
    - Two-handed signs with dual-assignment permutations: evaluates (H0, H1) and (H1, H0)
      to eliminate MediaPipe's erratic handedness label flipping when hands cross/touch.
    - Isolated dominant hand evaluation in 2-hand detections when user signs a 1-hand sign.
    - Deep Neural Network (Keras 5-layer DNN) cross-validation and consensus boosting.
    """
    if not hands_list:
        return {
            "detected": False,
            "prediction": None,
            "confidence": 0.0,
            "message": "No hands detected"
        }

    valid_hands = []
    for h in hands_list:
        raw = h.get("landmarks", []) if isinstance(h, dict) else h
        if raw and len(raw) >= 21:
            lbl = h.get("label", "Right") if isinstance(h, dict) else "Right"
            valid_hands.append({"landmarks": raw[:21], "label": lbl})

    if not valid_hands:
        return {
            "detected": False,
            "prediction": None,
            "confidence": 0.0,
            "message": "Insufficient hand landmarks"
        }

    candidates = []

    if len(valid_hands) == 1:
        pts = valid_hands[0]["landmarks"]
        # Hypothesis 1: Direct hand orientation
        f_dir = build_feature_vector(pts, None)
        p_dir = classifier.predict_proba([f_dir])[0]
        i_dir = int(np.argmax(p_dir))
        candidates.append({
            "label": str(label_encoder.classes_[i_dir]),
            "confidence": float(p_dir[i_dir]),
            "probs": p_dir,
            "hypothesis": "single_direct",
            "dominant_pts": pts
        })

        # Hypothesis 2: Horizontally Mirrored (Left hand or mirror perspective)
        pts_m = [[-p[0], p[1], p[2] if len(p) > 2 else 0.0] for p in pts]
        f_m = build_feature_vector(pts_m, None)
        p_m = classifier.predict_proba([f_m])[0]
        i_m = int(np.argmax(p_m))
        candidates.append({
            "label": str(label_encoder.classes_[i_m]),
            "confidence": float(p_m[i_m]) * 0.96,
            "probs": p_m,
            "hypothesis": "single_mirror",
            "dominant_pts": pts
        })

    elif len(valid_hands) >= 2:
        hA = valid_hands[0]["landmarks"]
        hB = valid_hands[1]["landmarks"]

        # Hypothesis 1: Hand 0 as Dominant, Hand 1 as Secondary
        f_AB = build_feature_vector(hA, hB)
        p_AB = classifier.predict_proba([f_AB])[0]
        i_AB = int(np.argmax(p_AB))
        conf_AB = float(p_AB[i_AB])

        # Hypothesis 2: Hand 1 as Dominant, Hand 0 as Secondary (Hand-swap resolution)
        f_BA = build_feature_vector(hB, hA)
        p_BA = classifier.predict_proba([f_BA])[0]
        i_BA = int(np.argmax(p_BA))
        conf_BA = float(p_BA[i_BA])

        if conf_AB >= conf_BA:
            candidates.append({
                "label": str(label_encoder.classes_[i_AB]),
                "confidence": conf_AB,
                "probs": p_AB,
                "hypothesis": "dual_direct",
                "dominant_pts": hA
            })
        else:
            candidates.append({
                "label": str(label_encoder.classes_[i_BA]),
                "confidence": conf_BA,
                "probs": p_BA,
                "hypothesis": "dual_swapped",
                "dominant_pts": hB
            })

        # Only if both dual hypotheses have low confidence (< 0.25), check if an isolated hand has a confident single-hand sign
        if max(conf_AB, conf_BA) < 0.25:
            for idx, h_pts in enumerate([hA, hB]):
                f_s = build_feature_vector(h_pts, None)
                p_s = classifier.predict_proba([f_s])[0]
                i_s = int(np.argmax(p_s))
                lbl_s = str(label_encoder.classes_[i_s])
                info_s = ISL_CLASSES.get(lbl_s, {})
                if info_s.get("hands", 1) == 1 and p_s[i_s] >= 0.70:
                    candidates.append({
                        "label": lbl_s,
                        "confidence": float(p_s[i_s]) * 0.90,
                        "probs": p_s,
                        "hypothesis": f"dual_isolated_hand_{idx}",
                        "dominant_pts": h_pts
                    })

    candidates.sort(key=lambda c: c["confidence"], reverse=True)
    winner = candidates[0]
    final_conf = winner["confidence"]
    final_label = winner["label"]
    probs = winner["probs"]

    # Top 3 predictions
    top_indices = np.argsort(probs)[::-1][:3]
    top_k = [
        {"label": str(label_encoder.classes_[i]), "confidence": round(float(probs[i]), 3)}
        for i in top_indices if probs[i] > 0.01
    ]

    # Keras 5-Layer Deep Neural Network cross-validation
    keras_res = None
    dom_pts = winner.get("dominant_pts")
    if dom_pts is not None and len(dom_pts) >= 21:
        keras_res = predict_keras_landmarks(dom_pts)
        if keras_res and keras_res.get("label") == final_label:
            # Model agreement consensus boost
            final_conf = min(0.99, round(final_conf * 1.05 + 0.04, 3))

    return {
        "detected": True,
        "prediction": final_label,
        "confidence": round(final_conf, 3),
        "top_k": top_k,
        "hypothesis": winner.get("hypothesis"),
        "keras_model": keras_res,
        "metadata": ISL_CLASSES.get(final_label, {})
    }


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

        # Run unified multi-hypothesis inference
        hands_list = [
            {"landmarks": h["raw_pts"], "label": h["label"]}
            for h in hands_data["hands"]
        ]
        result = run_isl_inference_engine(hands_list)

        # Attach frontend pixel points for overlay rendering
        frontend_hands = []
        for h in hands_data["hands"]:
            frontend_hands.append({
                "label": h["label"],
                "score": round(h["score"], 2),
                "bbox": h["bbox"],
                "pixel_pts": h["pixel_pts"]
            })
        result["hands"] = frontend_hands

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/predict_landmarks", methods=["POST"])
def api_predict_landmarks():
    """
    Accepts raw landmark arrays directly from web client (MediaPipe JS),
    evaluates multi-hypothesis feature vectors, and predicts gesture with ultra-low latency.
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

        result = run_isl_inference_engine(hands_in)
        return jsonify(result)

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
        import importlib
        import ml_pipeline.model_trainer as mt
        importlib.reload(mt)

        data = request.get_json(silent=True) or {}
        model_type = data.get("model_type", "random_forest")

        metrics = mt.train_isl_model(
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

@app.route("/api/reload_models", methods=["GET", "POST"])
def api_reload_models():
    """Reloads model artifacts dynamically without server restart."""
    load_artifacts()
    return jsonify({
        "status": "success",
        "model_loaded": classifier is not None,
        "keras_model_loaded": (keras_model is not None or keras_np_weights is not None),
        "num_classes": len(label_encoder.classes_) if label_encoder is not None else 0
    })

if __name__ == "__main__":
    import socket
    port = int(os.environ.get("PORT", 5000))
    def port_in_use(p):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', p)) == 0

    if port_in_use(port):
        print(f"[*] Port {port} is currently in use by another application.")
        for alt in [5050, 5001, 8080, 8000]:
            if not port_in_use(alt):
                port = alt
                break
        print(f"[*] Assigned ISL Recognition Web Server to port {port}.")

    print("=" * 60)
    print("Indian Sign Language (ISL) Recognition Web Server")
    print(f"Access application at: http://127.0.0.1:{port}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
