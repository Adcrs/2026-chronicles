import cv2
from PIL import Image
import os
import numpy as np

def frame_to_text(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    p = pil_image.load()
    width, height = pil_image.size

    lines = []
    for y in range(height):
        row = ""
        for x in range(width):
            row += pixel_to_char(p[x, y][0], p[x, y][1], p[x, y][2])
        lines.append(row)
    return "\n".join(lines)

def pixel_to_char(r, g, b):
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    if brightness < 64:
        return '@'
    elif brightness < 128:
        return '!'
    elif brightness < 192:
        return '?'
    else:
        return ' '

videoname = '_Bad_Apple_360p'
base_dir = os.path.dirname(os.path.abspath(__file__))
video = cv2.VideoCapture(os.path.join(base_dir, "..", "assets", "{0}.mp4".format(videoname)))
frames_dir = os.path.join(base_dir, "..", "assets", "frames")
os.makedirs(frames_dir, exist_ok=True)

frame_count = 0
while True:
    success, frame = video.read()
    if not success:
        break
    text = frame_to_text(frame)
    with open(os.path.join(frames_dir, "{:05d}.txt".format(frame_count)), "w") as f:
        f.write(text)
    frame_count += 1
    
video.release()
print("done!")