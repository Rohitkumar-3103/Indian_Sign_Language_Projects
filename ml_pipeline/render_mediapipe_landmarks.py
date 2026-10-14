"""
Generates publication-grade, high-resolution (300 DPI) diagrams of the
MediaPipe Hands 21 3D Landmark Keypoints Hierarchy for:
1. Academic Thesis Report (White background, LaTeX-ready) -> thesis_template_0.1/Figures/mediapipe_landmarks.png
2. Widescreen Presentation (Dark Cyberpunk background, PPT-ready) -> thesis_template_0.1/Figures/mediapipe_landmarks_dark.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Anatomically calibrated 2D coordinates
LANDMARKS = {
    0:  {"name": "WRIST",       "group": "Wrist",  "pos": (0.00, 0.06),  "ha": "center", "va": "top",    "offset": (0.00, -0.045)},
    # Thumb chain
    1:  {"name": "THUMB_CMC",   "group": "Thumb",  "pos": (-0.17, 0.19), "ha": "right",  "va": "center", "offset": (-0.038, 0.00)},
    2:  {"name": "THUMB_MCP",   "group": "Thumb",  "pos": (-0.32, 0.31), "ha": "right",  "va": "center", "offset": (-0.038, 0.00)},
    3:  {"name": "THUMB_IP",    "group": "Thumb",  "pos": (-0.44, 0.43), "ha": "right",  "va": "center", "offset": (-0.038, 0.00)},
    4:  {"name": "THUMB_TIP",   "group": "Thumb",  "pos": (-0.54, 0.54), "ha": "right",  "va": "bottom", "offset": (-0.038, 0.01)},
    # Index finger chain
    5:  {"name": "INDEX_MCP",   "group": "Index",  "pos": (-0.21, 0.48), "ha": "right",  "va": "top",    "offset": (-0.038, -0.01)},
    6:  {"name": "INDEX_PIP",   "group": "Index",  "pos": (-0.24, 0.65), "ha": "right",  "va": "center", "offset": (-0.038, 0.00)},
    7:  {"name": "INDEX_DIP",   "group": "Index",  "pos": (-0.26, 0.79), "ha": "right",  "va": "center", "offset": (-0.038, 0.00)},
    8:  {"name": "INDEX_TIP",   "group": "Index",  "pos": (-0.27, 0.91), "ha": "right",  "va": "bottom", "offset": (-0.038, 0.015)},
    # Middle finger chain
    9:  {"name": "MIDDLE_MCP",  "group": "Middle", "pos": (0.00, 0.51),  "ha": "center", "va": "top",    "offset": (0.00, -0.045)},
    10: {"name": "MID_PIP",     "group": "Middle", "pos": (0.00, 0.69),  "ha": "left",   "va": "center", "offset": (0.038, 0.00)},
    11: {"name": "MID_DIP",     "group": "Middle", "pos": (0.00, 0.84),  "ha": "left",   "va": "center", "offset": (0.038, 0.00)},
    12: {"name": "MID_TIP",     "group": "Middle", "pos": (0.00, 0.97),  "ha": "center", "va": "bottom", "offset": (0.00, 0.035)},
    # Ring finger chain
    13: {"name": "RING_MCP",    "group": "Ring",   "pos": (0.20, 0.48),  "ha": "left",   "va": "top",    "offset": (0.038, -0.01)},
    14: {"name": "RING_PIP",    "group": "Ring",   "pos": (0.23, 0.65),  "ha": "left",   "va": "center", "offset": (0.038, 0.00)},
    15: {"name": "RING_DIP",    "group": "Ring",   "pos": (0.25, 0.79),  "ha": "left",   "va": "center", "offset": (0.038, 0.00)},
    16: {"name": "RING_TIP",    "group": "Ring",   "pos": (0.26, 0.90),  "ha": "left",   "va": "bottom", "offset": (0.038, 0.015)},
    # Pinky finger chain
    17: {"name": "PINKY_MCP",   "group": "Pinky",  "pos": (0.37, 0.42),  "ha": "left",   "va": "top",    "offset": (0.038, -0.01)},
    18: {"name": "PINKY_PIP",   "group": "Pinky",  "pos": (0.43, 0.57),  "ha": "left",   "va": "center", "offset": (0.038, 0.00)},
    19: {"name": "PINKY_DIP",   "group": "Pinky",  "pos": (0.47, 0.69),  "ha": "left",   "va": "center", "offset": (0.038, 0.00)},
    20: {"name": "PINKY_TIP",   "group": "Pinky",  "pos": (0.50, 0.79),  "ha": "left",   "va": "bottom", "offset": (0.038, 0.015)}
}

# Kinematic bone linkages
BONES = [
    # Thumb chain
    (0, 1), (1, 2), (2, 3), (3, 4),
    # Index finger chain
    (0, 5), (5, 6), (6, 7), (7, 8),
    # Middle finger chain
    (0, 9), (9, 10), (10, 11), (11, 12),
    # Ring finger chain
    (0, 13), (13, 14), (14, 15), (15, 16),
    # Pinky finger chain
    (0, 17), (17, 18), (18, 19), (19, 20)
]

# Transverse palmar arch linkages
PALM_BONES = [
    (5, 9), (9, 13), (13, 17)
]

PALM_POLYGON = [0, 1, 5, 9, 13, 17]

# Distinct, professional color palettes
PALETTES = {
    "light": {
        "bg": "#FFFFFF",
        "card_bg": "#F8FAFC",
        "border": "#E2E8F0",
        "bone": "#94A3B8",
        "palm_bone": "#3B82F6",
        "palm_fill": "#EFF6FF",
        "banner_bg": "#1E3A8A", # Deep Academic Navy
        "banner_txt": "#FFFFFF",
        "sub_txt": "#93C5FD",
        "text_main": "#0F172A",
        "legend_border": "#CBD5E1",
        "colors": {
            "Wrist":  {"node": "#0F172A", "text": "#0F172A", "halo": "rgba(15, 23, 42, 0.12)"},
            "Thumb":  {"node": "#EA580C", "text": "#C2410C", "halo": "rgba(234, 88, 12, 0.12)"},
            "Index":  {"node": "#059669", "text": "#047857", "halo": "rgba(5, 150, 105, 0.12)"},
            "Middle": {"node": "#2563EB", "text": "#1D4ED8", "halo": "rgba(37, 99, 235, 0.12)"},
            "Ring":   {"node": "#7C3AED", "text": "#6D28D9", "halo": "rgba(124, 58, 237, 0.12)"},
            "Pinky":  {"node": "#E11D48", "text": "#BE123C", "halo": "rgba(225, 29, 72, 0.12)"}
        }
    },
    "dark": {
        "bg": "#0B0F19",
        "card_bg": "#131C2E",
        "border": "#1E293B",
        "bone": "#475569",
        "palm_bone": "#06B6D4",
        "palm_fill": "rgba(6, 182, 212, 0.08)",
        "banner_bg": "#1E293B",
        "banner_txt": "#F8FAFC",
        "sub_txt": "#38BDF8",
        "text_main": "#F8FAFC",
        "legend_border": "#334155",
        "colors": {
            "Wrist":  {"node": "#F8FAFC", "text": "#F8FAFC", "halo": "rgba(248, 250, 252, 0.18)"},
            "Thumb":  {"node": "#FB923C", "text": "#FDBA74", "halo": "rgba(251, 146, 60, 0.22)"},
            "Index":  {"node": "#10B981", "text": "#34D399", "halo": "rgba(16, 185, 129, 0.22)"},
            "Middle": {"node": "#38BDF8", "text": "#7DD3FC", "halo": "rgba(56, 189, 248, 0.22)"},
            "Ring":   {"node": "#A78BFA", "text": "#C4B5FD", "halo": "rgba(167, 139, 250, 0.22)"},
            "Pinky":  {"node": "#FB7185", "text": "#FDA4AF", "halo": "rgba(251, 113, 133, 0.22)"}
        }
    }
}

def render_diagram(theme="light", output_path="mediapipe_landmarks.png"):
    palette = PALETTES[theme]
    
    fig, ax = plt.subplots(figsize=(14.0, 11.2), dpi=300)
    fig.patch.set_facecolor(palette["bg"])
    ax.set_facecolor(palette["bg"])

    # 1. Background Translucent Palm Mesh Polygon
    poly_pts = [LANDMARKS[i]["pos"] for i in PALM_POLYGON]
    poly = patches.Polygon(
        poly_pts,
        closed=True,
        facecolor=palette["palm_fill"] if theme == "light" else palette["palm_bone"],
        alpha=0.65 if theme == "light" else 0.12,
        edgecolor=palette["palm_bone"],
        linestyle="--",
        linewidth=1.8,
        zorder=1
    )
    ax.add_patch(poly)

    # 2. Draw Kinematic Bone Linkages
    for (start, end) in BONES:
        p1 = LANDMARKS[start]["pos"]
        p2 = LANDMARKS[end]["pos"]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=palette["bone"], linewidth=4.2, solid_capstyle='round', zorder=2)

    # Transverse palmar arch
    for (start, end) in PALM_BONES:
        p1 = LANDMARKS[start]["pos"]
        p2 = LANDMARKS[end]["pos"]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=palette["palm_bone"], linewidth=2.6, linestyle=":", zorder=3)

    # 3. Draw Joint Nodes and Outer Glow Rings
    for idx, data in LANDMARKS.items():
        x, y = data["pos"]
        grp = data["group"]
        c_info = palette["colors"][grp]
        
        # Outer glow ring
        glow = patches.Circle((x, y), radius=0.024, facecolor=c_info["node"], alpha=0.25, edgecolor='none', zorder=4)
        ax.add_patch(glow)

        # Main node
        node_radius = 0.016 if idx != 0 else 0.019
        node = patches.Circle(
            (x, y),
            radius=node_radius,
            facecolor=c_info["node"],
            edgecolor=palette["bg"],
            linewidth=2.2,
            zorder=5
        )
        ax.add_patch(node)

        # Center core white highlight
        core = patches.Circle((x, y), radius=0.005, facecolor="#FFFFFF", edgecolor='none', zorder=6)
        ax.add_patch(core)

    # 4. Render Non-Overlapping Labels with Crisp Badges
    for idx, data in LANDMARKS.items():
        x, y = data["pos"]
        ox, oy = data["offset"]
        grp = data["group"]
        c_info = palette["colors"][grp]
        label_text = f"{idx}: {data['name']}"

        target_x = x + ox
        target_y = y + oy

        # Subtly stylized label badge
        bbox_props = dict(
            boxstyle="round,pad=0.32,rounding_size=0.2",
            fc=palette["card_bg"],
            ec=palette["border"],
            lw=1.1,
            alpha=0.94
        )

        ax.text(
            target_x,
            target_y,
            label_text,
            color=c_info["text"],
            fontsize=10.2,
            fontweight="bold",
            family="DejaVu Sans",
            ha=data["ha"],
            va=data["va"],
            bbox=bbox_props,
            zorder=7
        )

    # 5. Top Header Banner (Positioned with clear headroom above 12: MID_TIP)
    banner = patches.FancyBboxPatch(
        (-0.76, 1.10),
        1.52,
        0.13,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        facecolor=palette["banner_bg"],
        edgecolor=palette["border"],
        linewidth=1.5,
        zorder=8
    )
    ax.add_patch(banner)

    ax.text(
        0.00,
        1.18,
        "MediaPipe Hands: 21 3D Landmark Keypoints Hierarchy",
        color=palette["banner_txt"],
        fontsize=16.5,
        fontweight="bold",
        family="DejaVu Sans",
        ha="center",
        va="center",
        zorder=9
    )

    ax.text(
        0.00,
        1.13,
        "Skeletal Topological Ordering & Kinematic Joint Chain Architecture for Indian Sign Language (ISL)",
        color=palette["sub_txt"],
        fontsize=10.2,
        family="DejaVu Sans",
        ha="center",
        va="center",
        zorder=9
    )


    # 7. Bottom Legend / Anatomical Breakdown Box
    legend_box = patches.FancyBboxPatch(
        (-0.76, -0.22),
        1.52,
        0.18,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=palette["card_bg"],
        edgecolor=palette["legend_border"],
        linewidth=1.2,
        zorder=8
    )
    ax.add_patch(legend_box)

    legend_cols = [
        ("WRIST (0)", palette["colors"]["Wrist"]["node"], "Root Carpal Origin (0, 0, 0)"),
        ("THUMB (1-4)", palette["colors"]["Thumb"]["node"], "CMC -> MCP -> IP -> TIP"),
        ("INDEX (5-8)", palette["colors"]["Index"]["node"], "MCP -> PIP -> DIP -> TIP"),
        ("MIDDLE (9-12)", palette["colors"]["Middle"]["node"], "MCP -> PIP -> DIP -> TIP"),
        ("RING (13-16)", palette["colors"]["Ring"]["node"], "MCP -> PIP -> DIP -> TIP"),
        ("PINKY (17-20)", palette["colors"]["Pinky"]["node"], "MCP -> PIP -> DIP -> TIP")
    ]

    col_w = 1.52 / 6.0
    for i, (grp_name, grp_color, grp_desc) in enumerate(legend_cols):
        cx = -0.76 + (i + 0.5) * col_w
        # Color indicator pill
        pill = patches.Circle((cx - 0.08, -0.11), radius=0.014, facecolor=grp_color, edgecolor=palette["border"], lw=1, zorder=9)
        ax.add_patch(pill)
        ax.text(cx - 0.05, -0.11, grp_name, color=palette["text_main"], fontsize=9.2, fontweight="bold", va="center", ha="left", zorder=9)
        ax.text(cx, -0.165, grp_desc, color=palette["bone"], fontsize=7.2, va="center", ha="center", zorder=9)

    # Mathematical normalization specification label
    math_text = "Feature Invariance Formulation: Translation L'_i = L_i - L_0  |  Scale L^_i = L'_i / ||L_9 - L_0||  |  Total Dims: 21 x 3 = 63 / Hand"
    ax.text(0.00, -0.205, math_text, color=palette["palm_bone"], fontsize=8.2, fontweight="bold", ha="center", va="center", zorder=9)

    # Set coordinate limits
    ax.set_xlim(-0.85, 0.85)
    ax.set_ylim(-0.25, 1.28)
    ax.axis("off")
    plt.tight_layout()

    # Save high-resolution graphic
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=palette["bg"], edgecolor="none", bbox_inches="tight")
    plt.close()
    print(f"Successfully generated [{theme.upper()}] landmark diagram at: {output_path}")

if __name__ == "__main__":
    thesis_dir = r"d:\code\Web Development\Project\Indian_Sign_Language_Projects\thesis_template_0.1\Figures"
    
    # 1. Report version (White academic background for LaTeX Thesis)
    report_fig = os.path.join(thesis_dir, "mediapipe_landmarks.png")
    render_diagram("light", report_fig)

    # 2. Dark version (Widescreen 16:9 for Presentation Slides)
    dark_fig = os.path.join(thesis_dir, "mediapipe_landmarks_dark.png")
    render_diagram("dark", dark_fig)

    # 3. Also copy to root project Figures or Images if needed
    images_dir = r"d:\code\Web Development\Project\Indian_Sign_Language_Projects\Images"
    os.makedirs(images_dir, exist_ok=True)
    render_diagram("light", os.path.join(images_dir, "mediapipe_landmarks.png"))
