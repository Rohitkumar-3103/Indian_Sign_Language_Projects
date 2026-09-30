# 🤟 Indian Sign Language (ISL) Recognition & Translation System

An end-to-end, real-time Indian Sign Language (ISL) recognition system, dataset studio, interactive dictionary, and bidirectional translation platform built with **Python (Flask, OpenCV, MediaPipe, Scikit-learn)** and a modern **Glassmorphic Web Frontend**.

Designed and synthesized directly based on the research papers located in the repository, with special support for **two-handed ISL gestures**, **single-handed gestures**, **number digits (0-9)**, and **common conversational words/phrases**.

---

## 🌟 Key Features

1. **Real-Time ISL Translation (Sign-to-Text & Speech)**
   - Live camera detection with 3D MediaPipe hand landmark tracking.
   - Dual-color skeleton rendering: **Neon Emerald** for right hand, **Electric Cyan** for left hand.
   - Live HUD with recognized sign symbol, gesture name, and dynamic confidence gauge.
   - **Smart Sentence Buffer**: Debounced letter accumulator that builds words without stutter.
   - **Text-to-Speech (TTS)**: One-click natural voice readout of recognized sentences.

2. **Complete ML Pipeline & Dataset Studio**
   - Interactive web-based and CLI-based dataset collectors.
   - Visual countdown bursts (30 samples @ 11 FPS) for rapid class data collection.
   - Normalized 156-dimensional feature vector invariant to camera distance, translation, and scale.
   - Live **"Retrain Model Now"** button with in-memory model hot-reloading (zero server restart needed).

3. **Interactive ISL Dictionary & Practice Arena**
   - Searchable visual sign dictionary for Alphabets (A-Z), Digits (0-9), and Words.
   - Anatomical posture descriptions and tips based on standard ISLRTC conventions.
   - **"Practice In Camera" Challenge Mode**: Perform the target sign in front of your camera with real-time pose validation and celebratory confetti rewards!

4. **Research Benchmark & Architecture Dashboard**
   - Synthesis of 16 peer-reviewed ISL research papers in the repository.
   - Architectural comparisons across MediaPipe, CNNs, LSTMs, and Random Forest classifiers.
   - Stratified evaluation metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrix).

---

## 📐 Architecture & Feature Extraction

Unlike American Sign Language (ASL) which is largely single-handed, **Indian Sign Language (ISL) is predominantly two-handed** (e.g. A, B, D, E, F, G, H, M, N, P, Q, R, S, T, W, X, Y, Z, vowels where the right index touches left fingertips).

### 156-Dimensional Invariant Feature Layout:
- **Hand 1 (Right / Dominant Hand - 75 dimensions):**
  - $21 \times 3 = 63$ normalized 3D coordinates (shifted relative to wrist $(0,0,0)$ and scaled by wrist-to-middle-MCP distance).
  - 5 fingertip-to-wrist distances.
  - 4 thumb-tip to fingertip touching distances (crucial for ISL vowels A, E, I, O, U).
  - 3 adjacent fingertip spread distances (8-12, 12-16, 16-20).
- **Hand 2 (Left / Secondary Hand - 75 dimensions):**
  - $21 \times 3 = 63$ normalized 3D coordinates.
  - 12 invariant geometric distances.
- **Inter-Hand Relationship (6 dimensions):**
  - Hand 1 presence flag (`1.0` or `0.0`).
  - Hand 2 presence flag (`1.0` or `0.0`).
  - Inter-wrist 3D Euclidean distance.
  - Inter-wrist $\Delta x, \Delta y, \Delta z$ displacement vector.

---

## 📁 Repository Structure

```
Indian_Sign_Language_Projects/
├── app.py                      # Flask Application with REST APIs & real-time routes
├── run.bat                     # Windows 1-click launcher
├── requirements.txt            # Python dependencies
├── ml_pipeline/
│   ├── __init__.py
│   ├── feature_extractor.py    # MediaPipe 3D Landmark Extractor & Normalizer
│   ├── isl_dictionary.py       # ISL Gesture Definitions, Categories, Descriptions & Tips
│   ├── synthetic_bootstrap.py  # Anatomical baseline dataset generator for immediate use
│   ├── model_trainer.py        # Random Forest / MLP Trainer & Metrics Evaluator
│   └── dataset_collector.py    # CLI OpenCV interactive webcam dataset recorder
├── data/
│   └── isl_landmarks.csv       # Extracted 156-dim feature dataset (2,925+ samples)
├── models/
│   ├── isl_classifier.pkl      # Trained Random Forest ensemble model
│   ├── label_encoder.pkl       # Scikit-learn LabelEncoder
│   ├── isl_classes.json        # Class metadata & index mapping
│   └── model_metrics.json      # Validation accuracy, precision, recall & F1
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphic dark-mode CSS design system
│   └── js/
│       └── app.js              # Live webcam detection, speech synthesis, dataset studio
├── templates/
│   └── index.html              # Modern 4-tab Single Page Application
├── Images/                     # Raw image storage organized by A-Z, 0-9, Words
└── Research_Papers/            # 16 research papers on ISL detection
```

---

## 🚀 Quick Start Guide

### 1. Launch the Application
Simply double-click:
```bat
run.bat
```
Or run in your terminal:
```bash
py -3.10 app.py
```

### 2. Open in Browser
Navigate to:
```
http://127.0.0.1:5000
```

### 3. Using the Live Translator
1. Click **"Start Camera"** to grant webcam access.
2. Show any ISL sign (e.g. **'A'**, **'V'**, **'L'**, **'1'**, **'HELLO'**, **'THANK_YOU'**).
3. The HUD displays real-time prediction and confidence score.
4. Holding a sign adds it to the **Sentence Buffer**.
5. Click **"Speak Aloud (TTS)"** to hear the translated sentence!

### 4. Collecting Custom Dataset & Retraining
1. Switch to the **"Dataset Studio"** tab.
2. Choose a sign from the 45 available classes.
3. Align hands and press `SPACE` or click **"3s Burst Capture (30)"**.
4. Click **"Retrain Model Now"** to update your model with zero downtime!

### 5. Running the Standalone CLI Collector (Optional)
If you prefer recording samples directly from a native OpenCV desktop window:
```bash
py -3.10 -m ml_pipeline.dataset_collector --class_label A --samples 40
```
- `[SPACE]` to trigger countdown & capture burst.
- `[C]` to switch gesture class.
- `[T]` to retrain model.
- `[Q]` to exit.
