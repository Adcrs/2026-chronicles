import pygame
import threading
import time
import random
import math
import tween

def bounce(textitem, textdata):
    maxrotate     = textdata["MaxRotate"]
    rotationspeed = textdata["Speed"]
    tween_style   = textdata["EasingStyle"]
    step          = tween.tween(tween_style, maxrotate / rotationspeed)
    
    if textdata["Total"] < 3:
        if textdata["RRot"] == False:
            textdata["Rotation"] += step
            if textdata["Rotation"] >= maxrotate:
                textdata["Rotation"] = maxrotate  # clamp to exact max
                textdata["RRot"] = True
                textdata["Total"] += 1
        else:
            textdata["Rotation"] -= step
            if textdata["Rotation"] <= -maxrotate:
                textdata["Rotation"] = -maxrotate  # clamp to exact max
                textdata["LRot"] = True
                textdata["RRot"] = False
                textdata["Total"] += 1
    else:
        # Return to 0 — clamp the step so we don't overshoot
        if abs(textdata["Rotation"]) <= step:
            textdata["Rotation"] = 0  # close enough, snap to 0
        elif textdata["Rotation"] < 0:
            textdata["Rotation"] += step
        elif textdata["Rotation"] > 0:
            textdata["Rotation"] -= step

def create_text(data):
	text        = data["Text"]
	text_colour = data["Colour"]
	style       = data["Style"]
	text_font   = pygame.font.SysFont(data["Font"], 24)
	text_surface = text_font.render(text, True, text_colour)
	if style == "bounce":
		bounce(text_surface, data)
	rotated = pygame.transform.rotate(text_surface, data["Rotation"])
	return rotated