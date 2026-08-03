import asyncio
import os
import whisper
import edge_tts
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    afx,
)

async def generate_voiceover(
    text: str, output_audio_path: str, voice: str = "en-US-ChristopherNeural"
):
    print("🎙️ Generating AI voiceover...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio_path)

def generate_subtitles_whisper(audio_path: str):
    print("🧠 Transcribing audio with Whisper for auto-captions...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)

    captions = []
    for segment in result["segments"]:
        for word in segment["words"]:
            captions.append(
                {
                    "word": word["word"].strip().upper(),
                    "start": word["start"],
                    "end": word["end"],
                }
            )
    return captions

def build_short_video(
    input_video_path: str,
    voiceover_path: str,
    music_path: str,
    captions: list,
    output_path: str,
):
    print("🎬 Editing video & syncing audio...")

    voice_clip = AudioFileClip(voiceover_path)
    video_duration = voice_clip.duration

    raw_video = VideoFileClip(input_video_path)
    if raw_video.duration < video_duration:
        raw_video = raw_video.loop(duration=video_duration)
    else:
        raw_video = raw_video.subclip(0, video_duration)

    w, h = raw_video.size
    target_width = int(h * (9 / 16))

    if w > target_width:
        x1 = (w - target_width) // 2
        cropped_video = raw_video.crop(x1=x1, width=target_width, height=h)
    else:
        cropped_video = raw_video.resize(height=1920)

    cropped_video = cropped_video.resize((1080, 1920))

    if os.path.exists(music_path):
        bg_music = AudioFileClip(music_path)
        if bg_music.duration < video_duration:
            bg_music = bg_music.loop(duration=video_duration)
        else:
            bg_music = bg_music.subclip(0, video_duration)

        bg_music = bg_music.filter(afx.volumex, 0.12)
        final_audio = CompositeAudioClip([voice_clip, bg_music])
    else:
        final_audio = voice_clip

    cropped_video = cropped_video.set_audio(final_audio)

    text_clips = []
    for cap in captions:
        duration = cap["end"] - cap["start"]
        if duration <= 0:
            continue

        txt = TextClip(
            cap["word"],
            fontsize=70,
            color="yellow",
            font="Impact",
            stroke_color="black",
            stroke_width=4,
            method="caption",
            size=(900, None),
        )
        txt = (
            txt.set_position(("center", 1300))
            .set_start(cap["start"])
            .set_duration(duration)
        )
        text_clips.append(txt)

    final_render = CompositeVideoClip([cropped_video] + text_clips)

    print("🚀 Exporting final Short...")
    final_render.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4,
    )
    print(f"✨ Done! Short saved to {output_path}")

async def main():
    script_text = (
        "This top tier doctor received a most peculiar patient. "
        "A basketball-sized malformed cyst had grown from her abdomen, and whenever anyone "
        "tried to remove it, something bizarre occurred. "
        "They called upon Black Jack to perform the impossible surgery."
    )

    voice_audio = "voiceover.mp3"
    bg_music = "background_music.mp3"
    raw_anime_video = "raw_anime_clip.mp4"
    final_output = "anime_short_output.mp4"

    await generate_voiceover(script_text, voice_audio)
    captions = generate_subtitles_whisper(voice_audio)

    if os.path.exists(raw_anime_video):
        build_short_video(
            raw_anime_video, voice_audio, bg_music, captions, final_output
        )
    else:
        print(f"\n⚠️ Please place a sample video at '{raw_anime_video}' first!")

if __name__ == "__main__":
    asyncio.run(main())
