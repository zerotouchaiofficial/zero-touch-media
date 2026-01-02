from moviepy.editor import CompositeVideoClip
from pathlib import Path
from typing import List, Dict

from core.visuals.motion_engine import build_background_video
from core.visuals.text_renderer import render_text_segment


def compose_video(
    images: List[Path],
    text_segments: List[Dict],
    total_duration: float,
    output_path: Path,
    video_size=(1080, 1920),
    fps=30,
):
    # Background video
    base_clip = build_background_video(
        images=images,
        total_duration=total_duration,
        video_size=video_size,
    )

    composed = base_clip

    # Overlay text segments
    for segment in text_segments:
        composed = render_text_segment(
            base_clip=composed,
            segment=segment,
            video_size=video_size,
        )

    final_clip = composed.set_duration(total_duration)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    final_clip.write_videofile(
        str(output_path),
        fps=fps,
        codec="libx264",
        audio=False,
        preset="medium",
        threads=4,
        logger=None,
    )
