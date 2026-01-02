from moviepy.editor import ImageClip, CompositeVideoClip
from typing import List
from pathlib import Path


def ken_burns_clip(
    image_path: Path,
    duration: float,
    video_size=(1080, 1920),
):
    clip = ImageClip(str(image_path)).set_duration(duration)

    clip = clip.resize(height=video_size[1])

    start_scale = 1.0
    end_scale = 1.08

    def zoom(t):
        return start_scale + (end_scale - start_scale) * (t / duration)

    clip = clip.resize(zoom)

    # Subtle vertical pan
    y_start = 0
    y_end = -30

    def pos(t):
        y = y_start + (y_end - y_start) * (t / duration)
        return ("center", y)

    clip = clip.set_position(pos)

    return clip


def build_background_video(
    images: List[Path],
    total_duration: float,
    video_size=(1080, 1920),
):
    per_image_duration = total_duration / len(images)

    clips = [
        ken_burns_clip(img, per_image_duration, video_size)
        for img in images
    ]

    return CompositeVideoClip(clips, size=video_size)
