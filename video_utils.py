import subprocess
import os
import uuid

def convert_to_circle(input_path: str) -> str:
    output_path = f"{uuid.uuid4().hex}.mp4"

    # Обрезаем видео до квадрата и сжимаем для кружка
    command = [
        "ffmpeg", "-i", input_path,
        "-vf", r"crop='min(in_w\,in_h)':min(in_w\,in_h),scale=240:240",
        "-c:v", "libx264", "-preset", "veryfast", "-t", "60",
        "-y", output_path
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path