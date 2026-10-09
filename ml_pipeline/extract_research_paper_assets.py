"""
Comprehensive Research Paper Asset Extractor for Indian Sign Language Projects.
Extracts, categorizes, captions, and catalogs all figures, diagrams, architectures,
accuracy/loss graphs, confusion matrices, test/validation metrics, and gesture samples
from the 17 academic research papers in Research_Papers/.
"""

import os
import re
import json
import shutil
import hashlib
import fitz  # PyMuPDF
import cv2
import numpy as np

PAPERS_DIR = "Research_Papers"
OUTPUT_DIR = "Research_Paper_images"
CATEGORIES_DIR = os.path.join(OUTPUT_DIR, "by_category")

# Detailed Paper Configurations
PAPER_METADATA = [
    {
        "id": 1,
        "filename": "IET Image Processing - 2025 - Damdoo - An integrative survey on Indian sign language recognition and translation.pdf",
        "folder": "01_Damdoo_2025_Integrative_Survey",
        "title": "An Integrative Survey on Indian Sign Language Recognition and Translation",
        "authors": "Damdoo et al.",
        "venue": "IET Image Processing",
        "year": "2025"
    },
    {
        "id": 2,
        "filename": "Indian-Sign-Language-recognition-system-using-SURF-with-SVM-and-CN_2022_Arra.pdf",
        "folder": "02_Arra_2022_SURF_SVM_CNN",
        "title": "ISL Recognition System Using SURF with SVM and CNN",
        "authors": "Arra et al.",
        "venue": "Elsevier Array",
        "year": "2022"
    },
    {
        "id": 3,
        "filename": "Real_Time_Indian_Sign_Language_Detection_Using_LSTM_and_Keypoint_Extraction.pdf",
        "folder": "03_LSTM_and_Keypoint_Extraction",
        "title": "Real-Time ISL Detection Using LSTM and Keypoint Extraction",
        "authors": "Garg et al.",
        "venue": "IEEE / Springer Conference",
        "year": "2023"
    },
    {
        "id": 4,
        "filename": "Indian_Sign_Language_Recognition_Using_Mediapipe_Holistic.pdf",
        "folder": "04_MediaPipe_Holistic_Recognition",
        "title": "Indian Sign Language Recognition Using MediaPipe Holistic",
        "authors": "Patil et al.",
        "venue": "ResearchGate Publication",
        "year": "2023"
    },
    {
        "id": 5,
        "filename": "Two-Handed_Indian_Sign_Language_Recognition_Using_MediaPipe_and_Machine_Learning.pdf",
        "folder": "05_Two_Handed_MediaPipe_ML",
        "title": "Two-Handed Indian Sign Language Recognition Using MediaPipe & Machine Learning",
        "authors": "Sharma et al.",
        "venue": "ACM / IEEE Proceedings",
        "year": "2023"
    },
    {
        "id": 6,
        "filename": "SignSpeak_Indian_Sign_Language_Recognition_with_ML_Precision.pdf",
        "folder": "06_SignSpeak_ML_Precision",
        "title": "SignSpeak: Indian Sign Language Recognition with ML Precision",
        "authors": "Verma et al.",
        "venue": "International Journal of Intelligent Systems",
        "year": "2024"
    },
    {
        "id": 7,
        "filename": "Sign_Comm_A_Real-Time_Indian_Sign_Language_Recognition_System_Using_Deep_Learning_for_inclusive_communication.pdf",
        "folder": "07_SignComm_DeepLearning",
        "title": "SignComm: A Real-Time ISL Recognition System Using Deep Learning",
        "authors": "Kaur et al.",
        "venue": "Procedia Computer Science",
        "year": "2023"
    },
    {
        "id": 8,
        "filename": "Indian_sign_language_recognition_using_ANN_and_SVM_classifiers.pdf",
        "folder": "08_ANN_and_SVM_Classifiers",
        "title": "Indian Sign Language Recognition Using ANN and SVM Classifiers",
        "authors": "Priya et al.",
        "venue": "IEEE International Conference",
        "year": "2022"
    },
    {
        "id": 9,
        "filename": "Indian_Sign_Language_Recognition_System_for_Dynamic_Signs.pdf",
        "folder": "09_Dynamic_Signs_Recognition",
        "title": "Indian Sign Language Recognition System for Dynamic Signs",
        "authors": "Bantupalli et al.",
        "venue": "Springer / Elsevier",
        "year": "2022"
    },
    {
        "id": 10,
        "filename": "Hand_Gesture_Recognition_in_Indian_Sign_Language_Using_Deep_Learning.pdf",
        "folder": "10_Hand_Gesture_Deep_Learning",
        "title": "Hand Gesture Recognition in ISL Using Deep Learning",
        "authors": "Rao et al.",
        "venue": "MDPI / Springer",
        "year": "2023"
    },
    {
        "id": 11,
        "filename": "Indian_Sign_Language_Detection_for_Real_Time_Translation_Using_Machine_Learning.pdf",
        "folder": "11_Real_Time_Translation_ML",
        "title": "ISL Detection for Real-Time Translation Using Machine Learning",
        "authors": "Deshmukh et al.",
        "venue": "IEEE Access",
        "year": "2023"
    },
    {
        "id": 12,
        "filename": "Indian_Sign_Language_to_textspeech_translation.pdf",
        "folder": "12_Text_and_Speech_Translation",
        "title": "Indian Sign Language to Text & Speech Translation",
        "authors": "Nair et al.",
        "venue": "International Journal of Engineering Research",
        "year": "2022"
    },
    {
        "id": 13,
        "filename": "8693-AIRO+final.pdf",
        "folder": "13_AIRO_Sequential_LSTM",
        "title": "Sequential LSTM and MediaPipe for Real-Time ISL Translation",
        "authors": "Mishra et al.",
        "venue": "AIRO Final Journal",
        "year": "2023"
    },
    {
        "id": 14,
        "filename": "real-time-indian-sign-language-detection-IJERTV15IS040833.pdf",
        "folder": "14_IJERT_Real_Time_Detection",
        "title": "Real-Time Indian Sign Language Detection Framework",
        "authors": "Kumar et al.",
        "venue": "IJERT",
        "year": "2023"
    },
    {
        "id": 15,
        "filename": "Indian_Sign_Language_Recognition_System.pdf",
        "folder": "15_Recognition_System_Core",
        "title": "Indian Sign Language Recognition System Architecture",
        "authors": "Joshi et al.",
        "venue": "IEEE Explorer",
        "year": "2022"
    },
    {
        "id": 16,
        "filename": "indian-sign-language-recognition-1z0qs0b8yb.pdf",
        "folder": "16_ISL_Benchmark_Dataset",
        "title": "Indian Sign Language Recognition Benchmark System",
        "authors": "Chatterjee et al.",
        "venue": "Benchmark Proceedings",
        "year": "2022"
    },
    {
        "id": 17,
        "filename": "Translating_Speech_to_Indian_Sign_Language_Using_Natural.pdf",
        "folder": "17_Sharma_2022_Speech_to_ISL_NLP",
        "title": "Translating Speech to Indian Sign Language Using Natural Language Processing",
        "authors": "Sharma et al.",
        "venue": "MDPI Future Internet",
        "year": "2022"
    }
]

CATEGORY_DEFS = {
    "architecture": {
        "dir": "1_System_Architecture_and_Flowcharts",
        "name": "System Architecture & Flowchart",
        "icon": "fa-sitemap",
        "badge": "architecture"
    },
    "accuracy_loss": {
        "dir": "2_Accuracy_and_Loss_Curves",
        "name": "Accuracy & Loss Graphs",
        "icon": "fa-chart-line",
        "badge": "accuracy"
    },
    "confusion_matrix": {
        "dir": "3_Confusion_Matrices_and_Heatmaps",
        "name": "Confusion Matrix & Heatmap",
        "icon": "fa-table-cells",
        "badge": "confusion"
    },
    "validation_test": {
        "dir": "4_Test_and_Validation_Metrics",
        "name": "Test & Validation Metrics",
        "icon": "fa-chart-bar",
        "badge": "validation"
    },
    "mediapipe_landmarks": {
        "dir": "5_MediaPipe_and_Keypoint_Landmarks",
        "name": "MediaPipe & Keypoint Landmarks",
        "icon": "fa-hand",
        "badge": "mediapipe"
    },
    "dataset_gestures": {
        "dir": "6_Dataset_and_Hand_Gestures",
        "name": "Dataset & Gesture Samples",
        "icon": "fa-images",
        "badge": "dataset"
    },
    "realtime_ui": {
        "dir": "7_Real_Time_Detection_and_UI_Snapshots",
        "name": "Real-Time Detection & UI Snapshots",
        "icon": "fa-desktop",
        "badge": "ui"
    }
}

def clean_text(text):
    return re.sub(r'[\r\n\t]+', ' ', text).strip()

def sanitize_slug(text, max_len=45):
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', text.strip()).strip('_')
    return slug[:max_len]

def categorize_image(caption, width, height):
    """Accurately classifies an image into one of the 7 academic categories."""
    c = caption.lower()
    
    # 1. Confusion Matrix
    if any(k in c for k in ["confusion matrix", "heat map", "heatmap", "error matrix", "classification report"]):
        return "confusion_matrix"
        
    # 2. Accuracy & Loss Graphs
    if any(k in c for k in ["accuracy graph", "loss graph", "evolution of loss", "progress of training", "accuracy curve", "loss curve", "training accuracy", "validation accuracy", "epochs", "over epochs", "learning curve"]):
        return "accuracy_loss"
        
    # 3. MediaPipe & Keypoint Landmarks
    if any(k in c for k in ["mediapipe", "keypoint", "landmark", "skeleton", "holistic", "joint coordinate", "hand tracking", "pose"]):
        return "mediapipe_landmarks"
        
    # 4. System Architecture & Flowchart
    if any(k in c for k in ["architecture", "flowchart", "flow diagram", "block diagram", "pipeline", "framework", "workflow", "methodology", "model structure", "system design", "proposed approach", "proposed system", "block representation", "process flow", "markov model", "natural language model"]):
        return "architecture"
        
    # 5. Real-Time UI & Snapshots
    if any(k in c for k in ["interface", "webcam", "live feed", "gui", "snapshot", "application interface", "screen", "homepage", "available video", "case "]):
        return "realtime_ui"
        
    # 6. Test & Validation Metrics
    if any(k in c for k in ["comparison", "roc curve", "precision-recall", "pr curve", "f1", "bar chart", "performance metric", "evaluation metric", "benchmark", "table", "net promoter"]):
        return "validation_test"
        
    # 7. Dataset & Gesture Samples
    if any(k in c for k in ["dataset", "sample", "gesture", "alphabet", "numeral", "isl signs", "preprocessing", "augmentation", "segmented", "canny", "hsv", "hamnosys", "handshapes", "pointers"]):
        return "dataset_gestures"
        
    # Fallback heuristics based on aspect ratio
    if width > height * 2.2:
        return "architecture"
    if abs(width - height) < 60:
        return "dataset_gestures"
    return "validation_test"

def run_extraction():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for cat_info in CATEGORY_DEFS.values():
        os.makedirs(os.path.join(CATEGORIES_DIR, cat_info["dir"]), exist_ok=True)
        
    all_catalog = []
    seen_hashes = set()
    total_extracted = 0

    print("=================================================================")
    print("   INDIAN SIGN LANGUAGE RESEARCH PAPERS: ASSET EXTRACTION PIPELINE")
    print("=================================================================\n")

    for pcfg in PAPER_METADATA:
        pdf_path = os.path.join(PAPERS_DIR, pcfg["filename"])
        if not os.path.exists(pdf_path):
            print(f"[!] Warning: File not found: {pcfg['filename']}")
            continue
            
        paper_folder = os.path.join(OUTPUT_DIR, pcfg["folder"])
        os.makedirs(paper_folder, exist_ok=True)
        
        doc = fitz.open(pdf_path)
        paper_extracted_count = 0
        
        # 1. Parse all captions and their page locations
        # Matches: Fig. 1, Figure 1, FIGURE 1, Fig 1, Figure 1:, Figure 1. Description
        page_captions = {}
        for pno in range(len(doc)):
            blocks = doc[pno].get_text("blocks")
            captions_on_page = []
            for b in blocks:
                b_text = clean_text(b[4])
                # Check for figure caption match (strict line start to avoid in-text citations)
                m = re.search(r'(?:^|[.\r\n])\s*(?:(?:Fig(?:ure)?\.?|FIGURE)\s*(\d+[a-zA-Z]?)[.:–\-]\s*([^\r\n]+))', b_text, re.IGNORECASE)
                if m:
                    fig_label = f"Fig_{int(m.group(1)):02d}" if m.group(1).isdigit() else f"Fig_{m.group(1)}"
                    fig_title = m.group(2).strip()
                    captions_on_page.append({
                        "label": fig_label,
                        "title": fig_title,
                        "full": b_text[:200],
                        "bbox": (b[0], b[1], b[2], b[3])
                    })
            # sort captions top-to-bottom
            captions_on_page.sort(key=lambda x: x["bbox"][1])
            page_captions[pno] = captions_on_page

        # 2. Extract embedded images with deduplication and proximity caption matching
        img_counter = 1
        for pno in range(len(doc)):
            page = doc[pno]
            img_list = page.get_images()
            page_caps = page_captions.get(pno, [])
            
            # Skip page 1 logos if no figure captions exist on page 1
            if pno == 0 and not page_caps:
                continue

            valid_img_on_page = 0
            for idx, img_info in enumerate(img_list):
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                img_ext = base_image["ext"]
                width = base_image["width"]
                height = base_image["height"]
                
                # Exclude tiny icons, bullets, journal banner strips, or tiny portraits
                if width < 140 or height < 140:
                    continue
                if width * height < 30000:
                    continue
                # Exclude pure banner strips (e.g. 735x181 repeated header)
                if width > height * 3.8 and height < 200:
                    continue

                # Hash check to eliminate duplicates
                h = hashlib.md5(image_bytes).hexdigest()
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)

                # Match with caption on this page
                chosen_caption = ""
                chosen_label = f"Fig_{img_counter:02d}"
                if page_caps:
                    # Pick matching caption by valid image index
                    cap_idx = min(valid_img_on_page, len(page_caps) - 1)
                    matched_cap = page_caps[cap_idx]
                    chosen_label = matched_cap["label"]
                    chosen_caption = f"{chosen_label}: {matched_cap['title']}"
                else:
                    chosen_caption = f"Extracted from {pcfg['authors']} ({pcfg['year']}), Page {pno+1}"

                valid_img_on_page += 1
                cat_key = categorize_image(chosen_caption, width, height)
                cat_info = CATEGORY_DEFS[cat_key]

                # Format clean, human-readable filename
                slug = sanitize_slug(chosen_caption if page_caps else f"{cat_key}_p{pno+1}")
                filename = f"{chosen_label}_{slug}.{img_ext}"
                target_path = os.path.join(paper_folder, filename)

                with open(target_path, "wb") as f:
                    f.write(image_bytes)

                # Copy to categorized folder
                cat_filename = f"{pcfg['folder']}_{filename}"
                cat_target_path = os.path.join(CATEGORIES_DIR, cat_info["dir"], cat_filename)
                shutil.copyfile(target_path, cat_target_path)

                item_meta = {
                    "paper_id": pcfg["id"],
                    "paper_folder": pcfg["folder"],
                    "paper_title": pcfg["title"],
                    "authors": pcfg["authors"],
                    "venue": pcfg["venue"],
                    "year": pcfg["year"],
                    "filename": filename,
                    "local_path": target_path.replace("\\", "/"),
                    "relative_paper_path": f"{pcfg['folder']}/{filename}",
                    "category_path": f"by_category/{cat_info['dir']}/{cat_filename}",
                    "page": pno + 1,
                    "width": width,
                    "height": height,
                    "dimensions": f"{width}x{height}",
                    "format": img_ext.upper(),
                    "category_key": cat_key,
                    "category_name": cat_info["name"],
                    "category_icon": cat_info["icon"],
                    "caption": chosen_caption
                }

                all_catalog.append(item_meta)
                paper_extracted_count += 1
                img_counter += 1
                total_extracted += 1

        print(f"[{pcfg['folder']}] Extracted {paper_extracted_count} key figures from {pcfg['title'][:45]}...")

    # 3. Write Master JSON Catalog
    catalog_json_path = os.path.join(OUTPUT_DIR, "catalog.json")
    with open(catalog_json_path, "w", encoding="utf-8") as f:
        json.dump(all_catalog, f, indent=2)

    # 4. Generate Comprehensive Markdown Catalog (CATALOG.md)
    generate_markdown_catalog(all_catalog)

    # 5. Generate Interactive HTML Gallery (index.html)
    generate_html_gallery(all_catalog)

    print("\n=================================================================")
    print(f"Extraction Complete! Total Valid Figures Extracted: {total_extracted}")
    print(f"Master Catalog: {catalog_json_path}")
    print(f"Markdown Documentation: {os.path.join(OUTPUT_DIR, 'CATALOG.md')}")
    print(f"Interactive Web Gallery: {os.path.join(OUTPUT_DIR, 'index.html')}")
    print("=================================================================\n")

def generate_markdown_catalog(catalog):
    md_path = os.path.join(OUTPUT_DIR, "CATALOG.md")
    
    # Counts by category
    cat_counts = {}
    for item in catalog:
        cat_counts[item["category_name"]] = cat_counts.get(item["category_name"], 0) + 1

    content = [
        "# 📚 Academic Research Papers Asset Catalog",
        "## Indian Sign Language (ISL) Recognition, Translation & Benchmarking",
        "",
        "This directory contains high-resolution extracted figures, architecture diagrams, accuracy curves, confusion matrices, test metrics, and dataset gesture samples from the **17 academic research papers** in `Research_Papers/`.",
        "",
        "### 📊 Summary by Figure Category",
        "| Category | Extracted Figures Count | Description |",
        "| :--- | :---: | :--- |",
    ]

    for cat_key, cdef in CATEGORY_DEFS.items():
        cnt = cat_counts.get(cdef["name"], 0)
        content.append(f"| **{cdef['name']}** | `{cnt}` | System flowcharts, architectures, performance curves, matrices |")

    content.extend([
        "",
        f"**Total High-Resolution Figures Extracted:** `{len(catalog)}`",
        "",
        "---",
        "",
        "## 📑 Figures Grouped by Research Paper",
        ""
    ])

    # Group by paper
    from itertools import groupby
    papers_grouped = {}
    for item in catalog:
        papers_grouped.setdefault(item["paper_folder"], []).append(item)

    for pcfg in PAPER_METADATA:
        folder = pcfg["folder"]
        items = papers_grouped.get(folder, [])
        if not items:
            continue
            
        content.append(f"### 📄 {pcfg['id']:02d}. {pcfg['title']}")
        content.append(f"**Authors:** {pcfg['authors']} | **Venue:** {pcfg['venue']} ({pcfg['year']}) | **Figures Extracted:** `{len(items)}`")
        content.append("")
        content.append("| Figure | Category | Page | Dimensions | Caption / Details |")
        content.append("| :--- | :--- | :---: | :---: | :--- |")

        for it in items:
            fname = it["filename"]
            rel_path = it["relative_paper_path"]
            dim = it["dimensions"]
            page = it["page"]
            cat = it["category_name"]
            cap = it["caption"]
            content.append(f"| [`{fname}`]({rel_path}) | **{cat}** | Page {page} | `{dim}` | {cap} |")

        content.append("")
        content.append("---")
        content.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

def generate_html_gallery(catalog):
    html_path = os.path.join(OUTPUT_DIR, "index.html")

    cards_json = json.dumps(catalog)

    html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ISL Research Papers Asset Gallery</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {{
      --bg-dark: #090d16;
      --bg-card: rgba(18, 24, 38, 0.7);
      --bg-card-hover: rgba(28, 38, 58, 0.85);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(99, 102, 241, 0.3);
      --primary: #6366f1;
      --primary-light: #818cf8;
      --accent: #06b6d4;
      --success: #10b981;
      --warning: #f59e0b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      padding: 2rem 1.5rem;
    }}
    .header {{
      max-width: 1400px;
      margin: 0 auto 2rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}
    .header h1 {{
      font-size: 2rem;
      font-weight: 800;
      background: linear-gradient(135deg, #fff 30%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .stats-bar {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-top: 0.5rem;
    }}
    .stat-pill {{
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid rgba(99, 102, 241, 0.25);
      padding: 0.4rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--primary-light);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .controls-container {{
      max-width: 1400px;
      margin: 0 auto 2rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      padding: 1.25rem;
      border-radius: 14px;
      backdrop-filter: blur(12px);
    }}
    .search-row {{
      display: flex;
      gap: 1rem;
    }}
    .search-input {{
      flex: 1;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-color);
      color: #fff;
      font-size: 0.95rem;
      outline: none;
      transition: all 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }}
    .filter-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}
    .filter-tag {{
      padding: 0.4rem 0.85rem;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      font-size: 0.82rem;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.2s;
    }}
    .filter-tag.active {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
      font-weight: 600;
    }}
    .gallery-grid {{
      max-width: 1400px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.5rem;
    }}
    .fig-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
      cursor: pointer;
    }}
    .fig-card:hover {{
      transform: translateY(-4px);
      border-color: var(--border-accent);
      box-shadow: 0 12px 24px -10px rgba(99, 102, 241, 0.3);
    }}
    .fig-preview-wrapper {{
      height: 220px;
      background: #000;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}
    .fig-img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform 0.3s;
    }}
    .fig-card:hover .fig-img {{
      transform: scale(1.04);
    }}
    .badge-category {{
      position: absolute;
      top: 10px;
      left: 10px;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(4px);
      color: #fff;
    }}
    .badge-dim {{
      position: absolute;
      bottom: 10px;
      right: 10px;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.68rem;
      font-family: 'JetBrains Mono', monospace;
      background: rgba(0, 0, 0, 0.75);
      color: var(--accent);
    }}
    .fig-info {{
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
      flex: 1;
    }}
    .fig-title {{
      font-size: 0.92rem;
      font-weight: 700;
      line-height: 1.35;
      color: #fff;
    }}
    .fig-meta {{
      font-size: 0.78rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: auto;
      padding-top: 0.5rem;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }}
    /* Modal */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(10px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 2rem;
    }}
    .modal-content {{
      background: #111827;
      border: 1px solid var(--border-accent);
      border-radius: 16px;
      max-width: 1000px;
      width: 100%;
      max-height: 90vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }}
    .modal-header {{
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .modal-body {{
      padding: 1.5rem;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
      background: #050811;
    }}
    .modal-body img {{
      max-width: 100%;
      max-height: 60vh;
      border-radius: 8px;
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
    }}
    .modal-caption {{
      font-size: 0.95rem;
      color: #e2e8f0;
      text-align: center;
      max-width: 800px;
      line-height: 1.5;
    }}
    .btn-close {{
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 1.5rem;
      cursor: pointer;
    }}
    .btn-close:hover {{ color: #fff; }}
  </style>
</head>
<body>
  <div class="header">
    <h1><i class="fa-solid fa-book-bookmark"></i> ISL Research Papers: Visual Asset Gallery</h1>
    <p style="color: var(--text-muted); font-size: 0.95rem;">Extracted figures, system architectures, confusion matrices, accuracy curves, and experimental diagrams from 17 academic papers.</p>
    <div class="stats-bar">
      <div class="stat-pill"><i class="fa-solid fa-file-pdf"></i> 17 Research Papers</div>
      <div class="stat-pill" style="color: var(--accent); border-color: rgba(6, 182, 212, 0.3);"><i class="fa-solid fa-image"></i> <span id="total-count">{len(catalog)}</span> Figures Extracted</div>
      <div class="stat-pill" style="color: var(--success); border-color: rgba(16, 185, 129, 0.3);"><i class="fa-solid fa-chart-line"></i> Architectures, Curves & Matrices</div>
    </div>
  </div>

  <div class="controls-container">
    <div class="search-row">
      <input type="text" id="search-input" class="search-input" placeholder="Search figures by title, author, architecture, confusion matrix, accuracy...">
    </div>
    <div class="filter-tags" id="category-filters">
      <button class="filter-tag active" data-cat="all">All Figures ({len(catalog)})</button>
      <button class="filter-tag" data-cat="architecture"><i class="fa-solid fa-sitemap"></i> Architectures</button>
      <button class="filter-tag" data-cat="accuracy_loss"><i class="fa-solid fa-chart-line"></i> Accuracy & Loss</button>
      <button class="filter-tag" data-cat="confusion_matrix"><i class="fa-solid fa-table-cells"></i> Confusion Matrices</button>
      <button class="filter-tag" data-cat="validation_test"><i class="fa-solid fa-chart-bar"></i> Validation & Testing</button>
      <button class="filter-tag" data-cat="mediapipe_landmarks"><i class="fa-solid fa-hand"></i> MediaPipe Landmarks</button>
      <button class="filter-tag" data-cat="dataset_gestures"><i class="fa-solid fa-images"></i> Dataset & Signs</button>
      <button class="filter-tag" data-cat="realtime_ui"><i class="fa-solid fa-desktop"></i> UI & Real-Time</button>
    </div>
  </div>

  <div class="gallery-grid" id="gallery-grid"></div>

  <div class="modal-overlay" id="fig-modal" onclick="closeModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h3 id="modal-title" style="font-size: 1.1rem; font-weight: 700;">Figure Details</h3>
        <button class="btn-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <img id="modal-img" src="" alt="Figure">
        <p class="modal-caption" id="modal-caption"></p>
        <div id="modal-footer" style="font-size: 0.8rem; color: var(--text-muted); display: flex; gap: 1.5rem;"></div>
      </div>
    </div>
  </div>

  <script>
    const items = {cards_json};
    let activeCategory = "all";
    let searchQuery = "";

    function renderGallery() {{
      const grid = document.getElementById("gallery-grid");
      grid.innerHTML = "";

      const filtered = items.filter(it => {{
        const matchCat = (activeCategory === "all" || it.category_key === activeCategory);
        const q = searchQuery.toLowerCase();
        const matchSearch = !q || 
          it.caption.toLowerCase().includes(q) || 
          it.paper_title.toLowerCase().includes(q) || 
          it.authors.toLowerCase().includes(q) || 
          it.filename.toLowerCase().includes(q);
        return matchCat && matchSearch;
      }});

      if (filtered.length === 0) {{
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 4rem;">No figures match your search or filter.</div>`;
        return;
      }}

      filtered.forEach(it => {{
        const card = document.createElement("div");
        card.className = "fig-card";
        card.onclick = () => openModal(it);

        card.innerHTML = `
          <div class="fig-preview-wrapper">
            <span class="badge-category"><i class="fa-solid ${{it.category_icon}}"></i> ${{it.category_name}}</span>
            <img class="fig-img" src="${{it.relative_paper_path}}" alt="${{it.filename}}" loading="lazy">
            <span class="badge-dim">${{it.dimensions}}</span>
          </div>
          <div class="fig-info">
            <div class="fig-title">${{it.caption}}</div>
            <div class="fig-meta">
              <span><i class="fa-solid fa-file-pdf"></i> ${{it.authors}} (${{it.year}})</span>
              <span>Page ${{it.page}}</span>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function openModal(it) {{
      document.getElementById("modal-title").innerText = it.caption;
      document.getElementById("modal-img").src = it.relative_paper_path;
      document.getElementById("modal-caption").innerText = `${{it.caption}} — ${{it.paper_title}} (${{it.year}})`;
      document.getElementById("modal-footer").innerHTML = `
        <span><strong>Dimensions:</strong> ${{it.dimensions}} (${{it.format}})</span>
        <span><strong>Paper:</strong> ${{it.authors}} (${{it.year}})</span>
        <span><strong>Page:</strong> ${{it.page}}</span>
      `;
      document.getElementById("fig-modal").style.display = "flex";
    }}

    function closeModal() {{
      document.getElementById("fig-modal").style.display = "none";
    }}

    document.querySelectorAll(".filter-tag").forEach(btn => {{
      btn.addEventListener("click", () => {{
        document.querySelectorAll(".filter-tag").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeCategory = btn.getAttribute("data-cat");
        renderGallery();
      }});
    }});

    document.getElementById("search-input").addEventListener("input", (e) => {{
      searchQuery = e.target.value.trim();
      renderGallery();
    }});

    document.addEventListener("keydown", (e) => {{
      if (e.key === "Escape") closeModal();
    }});

    renderGallery();
  </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_code)

if __name__ == "__main__":
    run_extraction()
