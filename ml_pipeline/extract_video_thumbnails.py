import os
import cv2
import json

VIDEOS_DIR = "Images/isl_videos"
STATIC_SIGNS_DIR = "static/assets/signs"

def inspect_and_generate_thumbnails(overwrite=False):
    os.makedirs(STATIC_SIGNS_DIR, exist_ok=True)
    if not os.path.exists(VIDEOS_DIR):
        print(f"Error: {VIDEOS_DIR} not found.")
        return

    video_files = [f for f in os.listdir(VIDEOS_DIR) if f.lower().endswith(".mp4")]
    print(f"Found {len(video_files)} video files in {VIDEOS_DIR}.")

    extracted = 0
    skipped = 0
    failed = 0

    video_meta = {}

    # Real photos in 0-9 and A-Z should not be overwritten
    protected_keys = set([str(i) for i in range(10)] + [chr(c) for c in range(ord('A'), ord('Z') + 1)])

    for vfile in sorted(video_files):
        base_name = os.path.splitext(vfile)[0].upper()
        vpath = os.path.join(VIDEOS_DIR, vfile)
        
        cap = cv2.VideoCapture(vpath)
        if not cap.isOpened():
            print(f"Failed to open video: {vfile}")
            failed += 1
            continue

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        duration = round(frame_count / fps, 2) if fps > 0 else 0

        # Pick a frame around 40-50% through the video where gesture is formed
        target_frame = max(0, min(frame_count - 1, int(frame_count * 0.45)))
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, frame = cap.read()
        cap.release()

        video_meta[base_name] = {
            "filename": vfile,
            "frames": frame_count,
            "fps": round(fps, 1),
            "duration_sec": duration,
            "video_url": f"/api/videos/{vfile}"
        }

        # Save thumbnail to static/assets/signs/<NAME>.jpg
        thumb_path = os.path.join(STATIC_SIGNS_DIR, f"{base_name}.jpg")
        
        if ret and frame is not None:
            # Overwrite if forced, or if it doesn't exist, or if existing is a small placeholder
            should_write = overwrite or not os.path.exists(thumb_path)
            if not should_write and os.path.exists(thumb_path) and base_name not in protected_keys:
                existing_size = os.path.getsize(thumb_path)
                if existing_size < 25000:  # Small text box placeholder
                    should_write = True

            if should_write:
                cv2.imwrite(thumb_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
                extracted += 1
            else:
                skipped += 1

    print(f"Thumbnails: {extracted} newly extracted, {skipped} already existed, {failed} failed.")
    return video_meta

if __name__ == "__main__":
    meta = inspect_and_generate_thumbnails()
    print("Done. Sample metadata keys:", list(meta.keys())[:15] if meta else [])
