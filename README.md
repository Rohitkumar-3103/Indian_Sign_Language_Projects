# 🤟 Indian Sign Language (ISL) Recognition & Translation System

An end-to-end, real-time Indian Sign Language (ISL) recognition system, dataset studio, interactive dictionary, and bidirectional translation platform built with **Python (Flask, OpenCV, MediaPipe, Scikit-learn)** and a modern **Glassmorphic Web Frontend**.

Designed and synthesized directly based on the research papers located in the repository, with special support for **two-handed ISL gestures**, **single-handed gestures**, **number digits (0-9)**, and **common conversational words/phrases**.

---

## 🌟 Key Features

1. **Sign to Text (& Speech Translation)**
   - Live camera detection with 3D MediaPipe hand landmark tracking.
   - Dual-color skeleton rendering: **Neon Emerald** for right hand, **Electric Cyan** for left hand.
   - Live HUD with recognized sign symbol, gesture name, and dynamic confidence gauge.
   - **Smart Sentence Buffer**: Debounced letter accumulator that builds words without stutter.
   - **Text-to-Speech (TTS)**: One-click natural voice readout of recognized sentences.

2. **Text to Sign (Animated ISL Translation & Player)**
   - Translate any English or Hindi text into standard Indian Sign Language gestures.
   - Recognizes whole-word signs (e.g. `HELLO`, `THANK YOU`, `YES`, `NO`, `PLEASE`, `HELP`, `WATER`, `FOOD`, `I LOVE YOU`) and finger-spells names/words letter-by-letter (`A-Z`, `0-9`).
   - Interactive Sign Player with Play/Pause, step-by-step navigation, adjustable playback speeds (`0.7x`, `1.0x`, `1.5x`), and a scrollable filmstrip carousel.

3. **Voice to Sign (Speech-to-Sign Recognition)**
   - Real-time microphone speech recognition (English `en-IN` & Hindi `hi-IN`).
   - Live pulsating audio visualizer waves.
   - Transcribes spoken speech into text and immediately plays the corresponding Indian Sign Language gesture sequence!

4. **Complete ML Pipeline & Dataset Studio**
   - Interactive web-based and CLI-based dataset collectors.
   - Visual countdown bursts (30 samples @ 11 FPS) for rapid class data collection.
   - Normalized 156-dimensional feature vector invariant to camera distance, translation, and scale.
   - Live **"Retrain Model Now"** button with in-memory model hot-reloading (zero server restart needed).

5. **Interactive ISL Dictionary & Practice Arena**
   - Searchable visual sign dictionary for Alphabets (A-Z), Digits (0-9), and Words.
   - Anatomical posture descriptions and tips based on standard ISLRTC conventions.
   - **"Practice In Camera" Challenge Mode**: Perform the target sign in front of your camera with real-time pose validation and celebratory confetti rewards!

6. **Research Benchmark & Architecture Dashboard**
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
│   ├── js/
│   │   └── app.js              # Live webcam detection, speech synthesis, dataset studio
│   └── assets/signs/           # 45 visual sign cards & user-uploaded ISL images
├── templates/
│   └── index.html              # Modern 6-tab Single Page Application
├── Images/                     # Real user-uploaded ISL images (A-Z, 0-9)
├── Indian-Sign-Language-Detection-main/ # Subproject & Pretrained Keras Model
│   ├── model.h5                # 35-class Keras Feedforward Neural Network (954k params)
│   ├── keypoint.csv            # 42-point landmark dataset (7,669 samples)
│   ├── isl_detection.py        # Standalone OpenCV webcam detector
│   ├── run_standalone.bat      # 1-click standalone desktop launcher
│   └── ISL_classifier.ipynb    # Training notebook
└── Research_Papers/            # 16 research papers on ISL detection
```

---

## 🚀 Quick Start Guide

### 1. Launch the Main Web Application
Simply double-click:
```bat
run.bat
```
Or run in your terminal:
```bash
py -3.12 app.py
```
Open **http://127.0.0.1:5000** in your web browser.

### 2. Launch Standalone OpenCV Desktop Detector (Subproject)
If you wish to run the standalone OpenCV camera window from `Indian-Sign-Language-Detection-main`:
```bat
Indian-Sign-Language-Detection-main\run_standalone.bat
```
Or run:
```bash
python Indian-Sign-Language-Detection-main/isl_detection.py
```

### 3. Using the Web Application Modes
- **Sign to Text**: Click "Start Camera". Perform signs with single or both hands. The AI HUD detects gestures with confidence, top-3 matches, sentence accumulator, and natural voice Text-to-Speech (TTS).
- **Text to Sign**: Type any English or Hindi sentence. The player animates through whole-word ISL signs and letter-by-letter fingerspelling with variable speeds (0.5x - 2.0x) and filmstrip carousel.
- **Voice to Sign**: Click "Start Listening" and speak into your microphone. Real-time speech recognition transcribes your words and immediately triggers the ISL visual player.
- **Dataset Studio**: Capture new samples for any of the 45 classes directly via webcam bursts and retrain the model on-the-fly.
- **ISL Dictionary & Practice**: Search and view detailed anatomical guides for all 45 signs, or test your skills in "Practice with Camera" mode.
- **Research & Benchmarks**: View live confusion matrices, precision/recall/F1 metrics, and comparative analysis of 16 ISL research papers.

