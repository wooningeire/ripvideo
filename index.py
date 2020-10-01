import os, subprocess, base64, eel

eel.init("./web")
eel.start("index.html",
    block=False,
    size=(600, 500),
)

@eel.expose
def extract(video_data_base64: str, do_extract_visual: bool, do_extract_audio: bool, speed_factor: float) -> None:
    """Receives video data and settings from the JavaScript GUI and operates on the video."""

    video_data = base64.b64decode(video_data_base64)

    print(f"[PY] Video data received ({len(video_data)} bytes)")
    eel.polo()()

    save_video(video_data)

    speed_factor = float(speed_factor)

    if do_extract_visual:
        extract_visual(speed_factor)

    if do_extract_audio:
        extract_audio(speed_factor)

    print("[PY] Extraction complete")
    os.unlink("./tmp/video.mp4")

def save_video(video_data: str):
    """Saves the video data on the disk for FFmpeg to work on."""

    print(len(video_data))
    file = open("./tmp/video.mp4", "w+b")
    file.write(video_data)
    file.close()

def extract_visual(speed_factor: float) -> None:
    """Queries FFmpeg on the command line with settings to extract the visual stream."""

    if speed_factor == 1:
        # Do not reencode the video stream.
        subprocess.call("""ffmpeg -i "./tmp/video.mp4" -an -vcodec copy "./output/visual.mp4" -y""")
    else:
        # Reencode the video stream to the new speed.
        subprocess.call(f"""ffmpeg -i "./tmp/video.mp4" -an -filter:v "setpts=PTS/{speed_factor}" ./output/visual.mp4 -y""")

def extract_audio(speed_factor: float) -> None:
    """Queries FFmpeg on the command line with settings to extract the audio stream."""

    if speed_factor == 1:
        # Do not reencode the audio stream.
        subprocess.call("""ffmpeg -i "./tmp/video.mp4" -vn -acodec copy "./output/audio.aac" -y""")
    else:
        # Reencode the audio stream to the new speed.
        subprocess.call(f"""ffmpeg -i "./tmp/video.mp4" -vn -filter:a "atempo={speed_factor}" ./output/audio.aac -y""")

while True:
    eel.sleep(10)