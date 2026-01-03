import os
from core.uploader.youtube_uploader import upload_video

def run():
    os.system("python generate_short.py")

    video_path = "output/short.mp4"

    video_id = upload_video(
        video_path,
        title="Mind-Blowing Facts #shorts",
        description="Did you know this? 🤯 #shorts"
    )

    print("UPLOADED:", video_id)

if __name__ == "__main__":
    run()

