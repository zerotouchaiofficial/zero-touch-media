from moviepy.editor import VideoFileClip, AudioFileClip
from pathlib import Path


def merge_audio_video(
    video_path: Path,
    audio_path: Path,
    output_path: Path,
):
    video = VideoFileClip(str(video_path))
    audio = AudioFileClip(str(audio_path))

    final = video.set_audio(audio).set_duration(audio.duration)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    final.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        fps=video.fps,
        preset="medium",
        threads=4,
        logger=None,
    )

    video.close()
    audio.close()
    final.close()
