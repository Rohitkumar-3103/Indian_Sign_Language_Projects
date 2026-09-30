"""
Synthetic Bootstrap & Template Generator for Indian Sign Language (ISL).
Generates anatomically consistent baseline MediaPipe hand landmarks for ISL classes
(Alphabets A-Z, Numbers 0-9, and common phrases) with realistic perturbations,
enabling out-of-the-box real-time recognition before user-collected data is recorded.
"""

import os
import csv
import math
import numpy as np
from ml_pipeline.isl_dictionary import ISL_CLASSES
from ml_pipeline.feature_extractor import build_feature_vector

def create_base_hand(finger_states, is_left=False):
    """
    Generate 21 3D landmarks for a hand with specified finger states.
    finger_states: dict with keys 'thumb', 'index', 'middle', 'ring', 'pinky'
    values: 'extended', 'curled', 'half_curled', 'hooked', 'c_curved', 'upright'
    """
    landmarks = np.zeros((21, 3), dtype=np.float32)
    # 0: Wrist
    landmarks[0] = [0.0, 0.0, 0.0]

    # Hand direction multiplier
    x_sign = -1.0 if is_left else 1.0

    # Base MCP positions (relative to wrist)
    landmarks[1] = [x_sign * 0.35, 0.25, 0.05]   # Thumb CMC
    landmarks[2] = [x_sign * 0.55, 0.50, 0.05]   # Thumb MCP
    landmarks[5] = [x_sign * 0.35, 0.95, 0.0]    # Index MCP
    landmarks[9] = [0.0, 1.00, 0.0]              # Middle MCP (defines scale)
    landmarks[13] = [-x_sign * 0.30, 0.92, -0.02]# Ring MCP
    landmarks[17] = [-x_sign * 0.55, 0.80, -0.05]# Pinky MCP

    # Chains
    finger_chains = {
        'thumb': [(1, 2), (2, 3), (3, 4)],
        'index': [(5, 6), (6, 7), (7, 8)],
        'middle': [(9, 10), (10, 11), (11, 12)],
        'ring': [(13, 14), (14, 15), (15, 16)],
        'pinky': [(17, 18), (18, 19), (19, 20)]
    }

    lengths = {
        'thumb': [0.28, 0.25, 0.22],
        'index': [0.38, 0.26, 0.20],
        'middle': [0.42, 0.28, 0.22],
        'ring': [0.38, 0.25, 0.20],
        'pinky': [0.30, 0.20, 0.18]
    }

    for finger, state in finger_states.items():
        if finger == 'thumb':
            if state == 'extended':
                landmarks[3] = landmarks[2] + np.array([x_sign * 0.22, 0.22, 0.05])
                landmarks[4] = landmarks[3] + np.array([x_sign * 0.20, 0.20, 0.05])
            elif state == 'curled':
                landmarks[3] = landmarks[2] + np.array([-x_sign * 0.10, 0.15, -0.15])
                landmarks[4] = landmarks[3] + np.array([-x_sign * 0.15, 0.05, -0.20])
            elif state == 'upright': # Thumbs up
                landmarks[3] = landmarks[2] + np.array([0.0, 0.25, 0.10])
                landmarks[4] = landmarks[3] + np.array([0.0, 0.25, 0.10])
            else: # neutral
                landmarks[3] = landmarks[2] + np.array([x_sign * 0.15, 0.18, 0.0])
                landmarks[4] = landmarks[3] + np.array([x_sign * 0.12, 0.15, 0.0])
            continue

        mcp_idx = finger_chains[finger][0][0]
        p_prev = landmarks[mcp_idx]
        l1, l2, l3 = lengths[finger]
        f_x = landmarks[mcp_idx][0] * 0.2

        if state == 'extended':
            p1 = p_prev + np.array([f_x, l1, 0.0])
            p2 = p1 + np.array([f_x * 0.5, l2, 0.0])
            p3 = p2 + np.array([0.0, l3, 0.0])
        elif state == 'curled':
            p1 = p_prev + np.array([0.0, l1 * 0.5, -l1 * 0.7])
            p2 = p1 + np.array([0.0, -l2 * 0.4, -l2 * 0.5])
            p3 = p2 + np.array([0.0, -l3 * 0.8, l3 * 0.2])
        elif state == 'c_curved':
            p1 = p_prev + np.array([0.0, l1 * 0.7, 0.3])
            p2 = p1 + np.array([0.0, l2 * 0.3, 0.4])
            p3 = p2 + np.array([0.0, -l3 * 0.4, 0.3])
        elif state == 'hooked':
            p1 = p_prev + np.array([0.0, l1 * 0.2, 0.4])
            p2 = p1 + np.array([0.0, -l2 * 0.6, 0.3])
            p3 = p2 + np.array([0.0, -l3 * 0.5, 0.0])
        else: # half_curled
            p1 = p_prev + np.array([0.0, l1 * 0.6, -0.2])
            p2 = p1 + np.array([0.0, 0.0, -0.3])
            p3 = p2 + np.array([0.0, -l3 * 0.4, -0.2])

        p1_idx = finger_chains[finger][0][1]
        p2_idx = finger_chains[finger][1][1]
        p3_idx = finger_chains[finger][2][1]

        landmarks[p1_idx] = p1
        landmarks[p2_idx] = p2
        landmarks[p3_idx] = p3

    return landmarks

def generate_pose_for_class(label):
    info = ISL_CLASSES.get(label, {})
    is_two_handed = info.get("hands", 1) == 2

    all_open = {'thumb': 'extended', 'index': 'extended', 'middle': 'extended', 'ring': 'extended', 'pinky': 'extended'}
    all_closed = {'thumb': 'curled', 'index': 'curled', 'middle': 'curled', 'ring': 'curled', 'pinky': 'curled'}
    point_index = {'thumb': 'curled', 'index': 'extended', 'middle': 'curled', 'ring': 'curled', 'pinky': 'curled'}
    v_peace = {'thumb': 'curled', 'index': 'extended', 'middle': 'extended', 'ring': 'curled', 'pinky': 'curled'}
    thumbs_up = {'thumb': 'upright', 'index': 'curled', 'middle': 'curled', 'ring': 'curled', 'pinky': 'curled'}
    c_shape = {'thumb': 'extended', 'index': 'c_curved', 'middle': 'c_curved', 'ring': 'c_curved', 'pinky': 'c_curved'}
    l_shape = {'thumb': 'extended', 'index': 'extended', 'middle': 'curled', 'ring': 'curled', 'pinky': 'curled'}

    h1_states = all_open
    h2_states = None

    if label == "A":
        h1_states = point_index
        h2_states = all_open
    elif label == "B":
        h1_states = c_shape
        h2_states = c_shape
    elif label == "C":
        h1_states = c_shape
    elif label == "D":
        h1_states = c_shape
        h2_states = point_index
    elif label == "E":
        h1_states = point_index
        h2_states = all_open
    elif label == "F":
        h1_states = v_peace
        h2_states = v_peace
    elif label == "G":
        h1_states = all_closed
        h2_states = all_closed
    elif label == "H":
        h1_states = all_open
        h2_states = all_open
    elif label == "I":
        h1_states = point_index
        h2_states = all_open
    elif label == "J":
        h1_states = {'thumb': 'curled', 'index': 'hooked', 'middle': 'curled', 'ring': 'curled', 'pinky': 'curled'}
        h2_states = all_open
    elif label == "K":
        h1_states = {'thumb': 'curled', 'index': 'hooked', 'middle': 'curled', 'ring': 'curled', 'pinky': 'curled'}
        h2_states = point_index
    elif label == "L":
        h1_states = l_shape
    elif label == "M":
        h1_states = {'thumb': 'curled', 'index': 'extended', 'middle': 'extended', 'ring': 'extended', 'pinky': 'curled'}
        h2_states = all_open
    elif label == "N":
        h1_states = v_peace
        h2_states = all_open
    elif label == "O":
        h1_states = point_index
        h2_states = all_open
    elif label == "P":
        h1_states = c_shape
        h2_states = point_index
    elif label == "Q":
        h1_states = c_shape
        h2_states = point_index
    elif label == "R":
        h1_states = {'thumb': 'curled', 'index': 'hooked', 'middle': 'curled', 'ring': 'curled', 'pinky': 'curled'}
        h2_states = all_open
    elif label == "S":
        h1_states = {'thumb': 'curled', 'index': 'curled', 'middle': 'curled', 'ring': 'curled', 'pinky': 'extended'}
        h2_states = {'thumb': 'curled', 'index': 'curled', 'middle': 'curled', 'ring': 'curled', 'pinky': 'extended'}
    elif label == "T":
        h1_states = point_index
        h2_states = point_index
    elif label == "U":
        h1_states = point_index
        h2_states = all_open
    elif label == "V":
        h1_states = v_peace
    elif label == "W":
        h1_states = all_open
        h2_states = all_open
    elif label == "X":
        h1_states = point_index
        h2_states = point_index
    elif label == "Y":
        h1_states = point_index
        h2_states = l_shape
    elif label == "Z":
        h1_states = point_index
        h2_states = all_open
    # Numbers
    elif label == "0":
        h1_states = {'thumb': 'curled', 'index': 'c_curved', 'middle': 'c_curved', 'ring': 'c_curved', 'pinky': 'c_curved'}
    elif label == "1":
        h1_states = point_index
    elif label == "2":
        h1_states = v_peace
    elif label == "3":
        h1_states = {'thumb': 'curled', 'index': 'extended', 'middle': 'extended', 'ring': 'extended', 'pinky': 'curled'}
    elif label == "4":
        h1_states = {'thumb': 'curled', 'index': 'extended', 'middle': 'extended', 'ring': 'extended', 'pinky': 'extended'}
    elif label == "5":
        h1_states = all_open
    elif label == "6":
        h1_states = point_index
        h2_states = all_open
    elif label == "7":
        h1_states = v_peace
        h2_states = all_open
    elif label == "8":
        h1_states = {'thumb': 'curled', 'index': 'extended', 'middle': 'extended', 'ring': 'extended', 'pinky': 'curled'}
        h2_states = all_open
    elif label == "9":
        h1_states = {'thumb': 'curled', 'index': 'extended', 'middle': 'extended', 'ring': 'extended', 'pinky': 'extended'}
        h2_states = all_open
    # Words
    elif label == "HELLO":
        h1_states = all_open
    elif label == "THANK_YOU":
        h1_states = all_open
    elif label == "YES":
        h1_states = thumbs_up
    elif label == "NO":
        h1_states = {'thumb': 'extended', 'index': 'extended', 'middle': 'extended', 'ring': 'curled', 'pinky': 'curled'}
    elif label == "PLEASE":
        h1_states = all_open
    elif label == "HELP":
        h1_states = thumbs_up
        h2_states = all_open
    elif label == "ILOVEYOU":
        h1_states = {'thumb': 'extended', 'index': 'extended', 'middle': 'curled', 'ring': 'curled', 'pinky': 'extended'}
    elif label == "WATER":
        h1_states = {'thumb': 'curled', 'index': 'extended', 'middle': 'extended', 'ring': 'extended', 'pinky': 'curled'}
    elif label == "FOOD":
        h1_states = {'thumb': 'curled', 'index': 'half_curled', 'middle': 'half_curled', 'ring': 'half_curled', 'pinky': 'half_curled'}
    else:
        h1_states = all_open

    h1_pts = create_base_hand(h1_states, is_left=False)
    h2_pts = None
    if is_two_handed or h2_states is not None:
        h2_pts = create_base_hand(h2_states or all_open, is_left=True)

    return h1_pts, h2_pts

def generate_synthetic_dataset(output_csv_path, samples_per_class=65):
    """
    Generates realistic perturbation samples for all ISL classes and writes to CSV.
    """
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    header = [f"f_{i}" for i in range(156)] + ["label"]
    rows = []

    print(f"Generating synthetic baseline dataset for {len(ISL_CLASSES)} ISL classes...")

    for label in sorted(ISL_CLASSES.keys()):
        base_h1, base_h2 = generate_pose_for_class(label)

        for s in range(samples_per_class):
            noise_scale = 0.025
            h1_perturbed = base_h1 + np.random.normal(0, noise_scale, base_h1.shape).astype(np.float32)

            h2_perturbed = None
            if base_h2 is not None:
                h2_perturbed = base_h2 + np.random.normal(0, noise_scale, base_h2.shape).astype(np.float32)

            # Random slight 3D rotation
            angle_x = np.radians(np.random.uniform(-8, 8))
            angle_y = np.radians(np.random.uniform(-8, 8))
            angle_z = np.radians(np.random.uniform(-10, 10))

            Rx = np.array([[1, 0, 0], [0, np.cos(angle_x), -np.sin(angle_x)], [0, np.sin(angle_x), np.cos(angle_x)]], dtype=np.float32)
            Ry = np.array([[np.cos(angle_y), 0, np.sin(angle_y)], [0, 1, 0], [-np.sin(angle_y), 0, np.cos(angle_y)]], dtype=np.float32)
            Rz = np.array([[np.cos(angle_z), -np.sin(angle_z), 0], [np.sin(angle_z), np.cos(angle_z), 0], [0, 0, 1]], dtype=np.float32)
            R = Rz @ Ry @ Rx

            h1_perturbed = h1_perturbed @ R.T
            if h2_perturbed is not None:
                h2_perturbed = h2_perturbed @ R.T

            feat_vec = build_feature_vector(h1_perturbed, h2_perturbed)
            rows.append(list(feat_vec) + [label])

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} samples across {len(ISL_CLASSES)} classes into {output_csv_path}")
    return len(rows)

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), "..", "data", "isl_landmarks.csv")
    generate_synthetic_dataset(os.path.abspath(target))
