import os
import math
import numpy as np
from gtts import gTTS
import wikipediaapi
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    VideoClip,
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    concatenate_videoclips
)

# =====================
# CONFIG
# =====================
W, H = 1080, 1920
FPS = 30
TOTAL_DURATION = 60
FACT_COUNT = 6
FACT_DURATION = TOTAL_DURATION / FACT_COUNT
OUT_DIR = "output"
VOICE_FILE = f"{OUT_DIR}/voice.mp3"
VIDEO_FILE = f"{OUT_DIR}/short.mp4"

os.makedirs(OUT_DIR, exist_ok=True)

# =====================
# WIKIPEDIA
# =====================
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="zero-touch-shorts-bot/1.0"
)

TOPICS = [
    "Space",
    "Human brain",
    "Ocean",
    "Ancient Rome",
    "Artificial intelligence",
    "Black hole",
    "Time",
    "Earth",
    "Universe",
]

def get_facts():
    facts = []
    for topic in TOPICS:
        page = wiki.page(topic)
        if page.exists():
            text = page.summary.split(". ")
            for s in text:
                s = s.strip()
                if 40 < len(s) < 140:
                    facts.append(s + ".")
                if len(facts) >= FACT_COUNT:
                    return facts
    return facts[:FACT_COUNT]

# =====================
# AUDIO (LOCKED FIRST)
# =====================
def generate_voice(facts):
    script = " ".join(facts)
    tts = gTTS(script)
    tts.save(VOICE_FILE)
    audio = AudioFileClip(VOICE_FILE)

    if audio.duration < TOTAL_DURATION:
        audio = audio.audio_loop(duration=TOTAL_DURATION)

    return audio.subclip(0, TOTAL_DURATION)

# =====================
# ANIMATED BACKGROUND
# =====================
def animated_bg(seed, duration):
    def make_frame(t):
        np.random.seed(seed)
        frame = np.zeros((H, W, 3), dtype=np.uint8)

        # dark gradient
        for y in range(H):
            shade = int(20 + (y / H) * 40)
            frame[y, :, :] = shade

        # floating circles
        for i in range(5):
            cx = int(W/2 + math.sin(t*0.6 + i) * 300)
            cy = int(H/2 + math.cos(t*0.4 + i) * 500)
            r = 120 + i*15
            color = 60 + i*10

            yy, xx = np.ogrid[:H, :W]
            mask = (xx-cx)**2 + (yy-cy)**2 <= r*r
            frame[mask] = color

        return frame

    return VideoClip(make_frame, duration=duration).set_fps(FPS)

# =====================
# TEXT IMAGE (NO IMAGEMAGICK)
# =====================
def text_image(text):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("Arial.ttf", 72)
    except:
        font = ImageFont.load_default()

    max_width = 900
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = line + word + " "
        w = draw.textlength(test, font=font)
        if w <= max_width:
            line = test
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y = H//2 - (len(lines) * 45)
    for l in lines:
        w = draw.textlength(l, font=font)
        x = (W - w)//2
        draw.text((x, y), l, fill="white", font=font)
        y += 90

    return np.array(img)

# =====================
# BUILD VIDEO
# =====================
def generate_short():
    facts = get_facts()
    if len(facts) < FACT_COUNT:
        raise RuntimeError("Not enough Wikipedia facts")

    audio = generate_voice(facts)

    clips = []
    t = 0

    for i, fact in enumerate(facts):
        bg = animated_bg(i, FACT_DURATION)

        txt_img = text_image(fact)
        txt_clip = (
            ImageClip(txt_img)
            .set_duration(FACT_DURATION)
            .set_start(0)
            .fadein(0.3)
            .fadeout(0.3)
        )

        scene = CompositeVideoClip(
            [bg, txt_clip],
            size=(W, H)
        ).set_duration(FACT_DURATION)

        clips.append(scene)
        t += FACT_DURATION

    video = concatenate_videoclips(clips).set_audio(audio)

    video.write_videofile(
        VIDEO_FILE,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

# =====================
# ENTRY
# =====================
if __name__ == "__main__":
    generate_short()
