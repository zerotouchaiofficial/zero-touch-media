from moviepy.editor import TextClip, CompositeVideoClip
from typing import Dict


def render_text_segment(
    base_clip,
    segment: Dict,
    video_size=(1080, 1920),
    font="DejaVu-Sans",
    color="white",
    shadow=True,
    safe_margin_percent=8,
):
    width, height = video_size
    safe_margin = int(width * safe_margin_percent / 100)
    max_text_width = width - (safe_margin * 2)

    text = segment["text"]

    fontsize = 80
    txt_clip = None

    while fontsize > 20:
        try:
            txt_clip = TextClip(
                text,
                fontsize=fontsize,
                font=font,
                color=color,
                method="caption",
                size=(max_text_width, None),
                align="center",
            )
            if txt_clip.w <= max_text_width:
                break
        except Exception:
            pass

        fontsize -= 2

    if txt_clip is None:
        raise RuntimeError("Failed to render text")

    y_position = int(height * 0.65)

    txt_clip = (
        txt_clip.set_start(segment["start"])
        .set_duration(segment["duration"])
        .set_position(("center", y_position))
        .fadein(0.4)
        .fadeout(0.4)
    )

    if shadow:
        shadow_clip = (
            txt_clip.copy()
            .set_color("black")
            .set_opacity(0.6)
            .set_position(("center", y_position + 3))
        )
        return CompositeVideoClip([base_clip, shadow_clip, txt_clip])

    return CompositeVideoClip([base_clip, txt_clip])
