import os
import subprocess
import sys

VIDEO_PATH = "output/short.mp4"

def main():
    print("▶ Generating video...")
    subprocess.run([sys.executable, "generate_short.py"], check=True)

    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError(f"Video not found: {VIDEO_PATH}")

    print("▶ Uploading video...")
    from core.uploader.youtube_uploader import upload_video
    upload_video(VIDEO_PATH)

if __name__ == "__main__":
    main()
