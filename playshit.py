import os
import time
import pygame
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
frames_dir = os.path.join(base_dir, "..", "assets", "frames")
music_path = os.path.join(base_dir, "..", "assets", "badapplemusic.mp3")

frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".txt")])
fps = 30
frame_delay = 1.0 / fps


sys.stdout.write("\033[?25l") 
sys.stdout.flush()

pygame.mixer.init()
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(0)

for frame_file in frames:
    start = time.perf_counter()

    with open(os.path.join(frames_dir, frame_file), "r") as f:
        content = f.read()

    sys.stdout.write("\033[H" + content)
    sys.stdout.flush()

    elapsed = time.perf_counter() - start
    sleep_time = frame_delay - elapsed
    if sleep_time > 0:
        time.sleep(sleep_time)


sys.stdout.write("\033[?25h")
sys.stdout.flush()
pygame.mixer.music.stop()
pygame.mixer.quit()