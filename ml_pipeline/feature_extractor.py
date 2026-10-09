"""
Feature Extractor for Indian Sign Language (ISL).
Extracts invariant normalized 1D feature vectors (156 dimensions) supporting
both single-handed and two-handed ISL gestures.
Works with MediaPipe Hands (Python) and direct landmark arrays from Web/JS clients.
"""

import math
import numpy as np
import cv2

LANDMARKS_PER_HAND = 21
FINGERTIP_IDS = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky
MCP_IDS = [2, 5, 9, 13, 17]

def normalize_hand_landmarks(landmarks):
    """
    Normalize 21 3D landmarks of a single hand:
    1. Translation invariance: shift wrist (landmark 0) to origin (0, 0, 0).
    2. Scale invariance: normalize by distance between wrist (0) and middle MCP (9).
    landmarks: list or array of shape (21, 3)
    Returns:
        norm_landmarks (21, 3): normalized coordinates
        palm_scale (float): scale factor
    """
    lms = np.array(landmarks, dtype=np.float32)
    wrist = lms[0]
    shifted = lms - wrist

    # Distance from wrist (0) to middle finger MCP (9)
    palm_dist = float(np.linalg.norm(shifted[9]))
    if palm_dist < 1e-4:
        # Fallback to max spread if wrist-MCP distance is degenerate
        palm_dist = float(np.max(np.abs(shifted)))
        if palm_dist < 1e-4:
            palm_dist = 1.0

    normalized = shifted / palm_dist
    return normalized, palm_dist

def extract_geometric_features(norm_landmarks):
    """
    Extract 12 invariant geometric relationships:
    - 5 Fingertip distances from wrist (0)
    - 4 Thumb-tip to fingertip distances (touching detection for ISL vowels A, E, I, O, U)
    - 3 Inter-finger spread distances between adjacent tips (8-12, 12-16, 16-20)
    """
    features = []

    # 1. Fingertip distances from wrist (wrist is 0,0,0)
    for tip_id in FINGERTIP_IDS:
        dist = float(np.linalg.norm(norm_landmarks[tip_id]))
        features.append(dist)

    # 2. Thumb-tip (4) to other fingertip distances (touches)
    thumb_tip = norm_landmarks[4]
    for tip_id in [8, 12, 16, 20]:
        dist = float(np.linalg.norm(thumb_tip - norm_landmarks[tip_id]))
        features.append(dist)

    # 3. Inter-finger spread among the 4 fingers (8-12, 12-16, 16-20)
    four_fingers = [8, 12, 16, 20]
    for i in range(1, len(four_fingers)):
        t1 = norm_landmarks[four_fingers[i-1]]
        t2 = norm_landmarks[four_fingers[i]]
        dist = float(np.linalg.norm(t1 - t2))
        features.append(dist)

    return np.array(features, dtype=np.float32)

def build_feature_vector(hand1_pts=None, hand2_pts=None):
    """
    Construct complete 156-element feature vector from up to 2 hands:
    - Hand 1 (Right/Dominant): 63 norm coords + 12 geometric features = 75
    - Hand 2 (Left/Secondary): 63 norm coords + 12 geometric features = 75
    - Inter-Hand Dynamics: 6 features (hand1_present, hand2_present, inter_dist, dx, dy, dz)
    Total: 75 + 75 + 6 = 156 features.
    """
    features = np.zeros(156, dtype=np.float32)

    # Hand 1
    if hand1_pts is not None and len(hand1_pts) >= 21:
        norm1, _ = normalize_hand_landmarks(hand1_pts[:21])
        geom1 = extract_geometric_features(norm1)
        features[0:63] = norm1.flatten()
        features[63:75] = geom1
        features[150] = 1.0 # Hand 1 present

    # Hand 2
    if hand2_pts is not None and len(hand2_pts) >= 21:
        norm2, _ = normalize_hand_landmarks(hand2_pts[:21])
        geom2 = extract_geometric_features(norm2)
        features[75:138] = norm2.flatten()
        features[138:150] = geom2
        features[151] = 1.0 # Hand 2 present

    # Inter-Hand Relationship
    if hand1_pts is not None and hand2_pts is not None and len(hand1_pts) >= 21 and len(hand2_pts) >= 21:
        w1 = np.array(hand1_pts[0], dtype=np.float32)
        w2 = np.array(hand2_pts[0], dtype=np.float32)
        diff = w1 - w2
        features[152] = float(np.linalg.norm(diff))
        features[153] = float(diff[0])
        features[154] = float(diff[1])
        features[155] = float(diff[2])

    return features

class ISLFeatureExtractor:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.hands_detector = None
        self._init_mediapipe()

    def _init_mediapipe(self):
        try:
            import mediapipe as mp
            if hasattr(mp, 'solutions') and hasattr(mp.solutions, 'hands'):
                self.mp_hands = mp.solutions.hands
                self.mp_draw = mp.solutions.drawing_utils
                self.hands_detector = self.mp_hands.Hands(
                    static_image_mode=self.static_image_mode,
                    max_num_hands=self.max_num_hands,
                    min_detection_confidence=self.min_detection_confidence,
                    min_tracking_confidence=self.min_tracking_confidence
                )
                print("MediaPipe Hands initialized successfully.")
            else:
                print("MediaPipe Solutions not available in this build; using direct landmark processor.")
        except Exception as e:
            print(f"Warning: MediaPipe Hands initialization deferred: {e}")

    def extract_features_from_image(self, bgr_image):
        """Processes BGR image and returns (156,) feature vector and hands_data dict."""
        h, w = bgr_image.shape[:2]
        if self.hands_detector is None:
            return np.zeros(156, dtype=np.float32), {"num_hands": 0, "hands": []}

        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        results = self.hands_detector.process(rgb_image)

        hands_data = {"num_hands": 0, "hands": []}
        if not results.multi_hand_landmarks:
            return np.zeros(156, dtype=np.float32), hands_data

        detected_hands = []
        for idx, hand_lms in enumerate(results.multi_hand_landmarks):
            raw_pts = []
            pixel_pts = []
            for lm in hand_lms.landmark:
                raw_pts.append([lm.x, lm.y, lm.z])
                pixel_pts.append([int(lm.x * w), int(lm.y * h)])

            handedness_label = "Right"
            score = 1.0
            if results.multi_handedness and idx < len(results.multi_handedness):
                handedness_label = results.multi_handedness[idx].classification[0].label
                score = results.multi_handedness[idx].classification[0].score

            xs = [p[0] for p in pixel_pts]
            ys = [p[1] for p in pixel_pts]
            bbox = [max(0, min(xs) - 10), max(0, min(ys) - 10), min(w, max(xs) + 10), min(h, max(ys) + 10)]

            norm_pts, palm_scale = normalize_hand_landmarks(raw_pts)
            geom_feats = extract_geometric_features(norm_pts)

            detected_hands.append({
                "label": handedness_label,
                "score": float(score),
                "raw_pts": raw_pts,
                "pixel_pts": pixel_pts,
                "norm_pts": norm_pts,
                "geom_feats": geom_feats,
                "bbox": bbox
            })

        hands_data["num_hands"] = len(detected_hands)
        hands_data["hands"] = detected_hands

        # Sort hands: Hand 1 is Right/Dominant, Hand 2 is Left
        hand1 = None
        hand2 = None
        if len(detected_hands) == 1:
            hand1 = detected_hands[0]
        elif len(detected_hands) >= 2:
            if detected_hands[0]["label"] == "Right":
                hand1 = detected_hands[0]
                hand2 = detected_hands[1]
            elif detected_hands[1]["label"] == "Right":
                hand1 = detected_hands[1]
                hand2 = detected_hands[0]
            else:
                if detected_hands[0]["raw_pts"][0][0] < detected_hands[1]["raw_pts"][0][0]:
                    hand1 = detected_hands[0]
                    hand2 = detected_hands[1]
                else:
                    hand1 = detected_hands[1]
                    hand2 = detected_hands[0]

        h1_pts = hand1["raw_pts"] if hand1 else None
        h2_pts = hand2["raw_pts"] if hand2 else None
        features = build_feature_vector(h1_pts, h2_pts)

        return features, hands_data

    def draw_landmarks_on_frame(self, frame, hands_data):
        """Draws upgraded cyberpunk skeleton on OpenCV frame with dual-hand styling and bimanual links."""
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),        # Index
            (0, 9), (5, 9), (9, 10), (10, 11), (11, 12), # Middle & Palm
            (9, 13), (13, 14), (14, 15), (15, 16), # Ring
            (0, 17), (13, 17), (17, 18), (18, 19), (19, 20) # Pinky & Palm Outer
        ]

        hands = hands_data.get("hands", [])
        for hand in hands:
            pts = hand["pixel_pts"]
            label = hand["label"]
            score = hand["score"]
            bbox = hand["bbox"]

            color = (129, 185, 16) if label == "Right" else (212, 182, 6) # BGR
            light_color = (180, 235, 100) if label == "Right" else (240, 215, 100)
            joint_color = (255, 255, 255)

            # Translucent Palm Polygon
            if len(pts) >= 21:
                palm_pts = np.array([pts[0], pts[1], pts[5], pts[9], pts[13], pts[17]], dtype=np.int32)
                overlay = frame.copy()
                cv2.fillPoly(overlay, [palm_pts], color)
                cv2.addWeighted(overlay, 0.18, frame, 0.82, 0, frame)

            # Sci-Fi Corner Brackets
            bx1, by1, bx2, by2 = bbox
            c_len = 14
            # Top-left
            cv2.line(frame, (bx1, by1), (bx1 + c_len, by1), color, 2, cv2.LINE_AA)
            cv2.line(frame, (bx1, by1), (bx1, by1 + c_len), color, 2, cv2.LINE_AA)
            # Top-right
            cv2.line(frame, (bx2, by1), (bx2 - c_len, by1), color, 2, cv2.LINE_AA)
            cv2.line(frame, (bx2, by1), (bx2, by1 + c_len), color, 2, cv2.LINE_AA)
            # Bottom-left
            cv2.line(frame, (bx1, by2), (bx1 + c_len, by2), color, 2, cv2.LINE_AA)
            cv2.line(frame, (bx1, by2), (bx1, by2 - c_len), color, 2, cv2.LINE_AA)
            # Bottom-right
            cv2.line(frame, (bx2, by2), (bx2 - c_len, by2), color, 2, cv2.LINE_AA)
            cv2.line(frame, (bx2, by2), (bx2, by2 - c_len), color, 2, cv2.LINE_AA)

            # Floating Tag Badge
            tag_text = f"{label.upper()} ({int(score*100)}%)"
            (tw, th), _ = cv2.getTextSize(tag_text, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            cv2.rectangle(frame, (bx1, max(18, by1 - 20)), (bx1 + tw + 10, max(18, by1)), (20, 24, 30), -1)
            cv2.rectangle(frame, (bx1, max(18, by1 - 20)), (bx1 + tw + 10, max(18, by1)), color, 1)
            cv2.putText(frame, tag_text, (bx1 + 5, max(14, by1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.42, light_color, 1, cv2.LINE_AA)

            # Glow bone lines + Core lines
            for conn in connections:
                if conn[0] < len(pts) and conn[1] < len(pts):
                    p1 = tuple(pts[conn[0]])
                    p2 = tuple(pts[conn[1]])
                    cv2.line(frame, p1, p2, color, 4, cv2.LINE_AA)
                    cv2.line(frame, p1, p2, light_color, 2, cv2.LINE_AA)

            # Differentiated Radiant Joints
            tip_indices = [4, 8, 12, 16, 20]
            for i, pt in enumerate(pts):
                pt_t = tuple(pt)
                if i in tip_indices:
                    cv2.circle(frame, pt_t, 8, color, 1, cv2.LINE_AA)
                    cv2.circle(frame, pt_t, 4, joint_color, -1, cv2.LINE_AA)
                elif i == 0:
                    cv2.circle(frame, pt_t, 7, light_color, 2, cv2.LINE_AA)
                    cv2.circle(frame, pt_t, 3, color, -1, cv2.LINE_AA)
                else:
                    cv2.circle(frame, pt_t, 4, joint_color, -1, cv2.LINE_AA)
                    cv2.circle(frame, pt_t, 4, color, 1, cv2.LINE_AA)

        # Bimanual Inter-Wrist Connection Link
        if len(hands) >= 2 and len(hands[0]["pixel_pts"]) > 0 and len(hands[1]["pixel_pts"]) > 0:
            w1 = tuple(hands[0]["pixel_pts"][0])
            w2 = tuple(hands[1]["pixel_pts"][0])
            dist = int(np.hypot(w1[0] - w2[0], w1[1] - w2[1]))
            cv2.line(frame, w1, w2, (200, 200, 200), 1, cv2.LINE_AA)
            mid = ((w1[0] + w2[0]) // 2, (w1[1] + w2[1]) // 2)
            cv2.putText(frame, f"d={dist}px", mid, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1, cv2.LINE_AA)

        return frame

    def close(self):
        if self.hands_detector:
            self.hands_detector.close()
