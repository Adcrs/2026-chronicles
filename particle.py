import pygame
import threading
import time
import random
import math
import tween
particledata = {}



# ------------------ REMOVE PARTICLE ------------------
def removeparticle(uid, timev):
    time.sleep(timev)
    if uid in particledata:
        del particledata[uid]

# ------------------ EMIT ------------------
def emit_particle(uid, window):
    if uid not in particledata:
        return

    data = particledata[uid]
    emitdata = data[1]

    for i in range(data[0]["Number"]):
        emitdata[i] = {}

        position = data[0]["Position"]
        spread = data[0]["Spread"]

        distance = random.uniform(-data[0]["MaxDistance"], data[0]["MaxDistance"])

    
        angle = math.radians(random.uniform(-spread, spread))

        goalx = position['x'] + math.sin(angle) * distance
        goaly = position['y'] - math.cos(angle) * distance  # UPWARD

        emitdata[i].update({
            "X": position['x'],
            "Y": position['y'],
            "InitialPositions": position,
            "GoalX": goalx,
            "GoalY": goaly,
            "Colour": data[0]["Colour"],
            "Size": data[0]["Size"],
            "Shape": data[0]["Shape"],
            "Speed": random.uniform(data[0]["Speed"]/2,data[0]["Speed"]),
            "LiveSpeed":data[0]["Speed"],
            "Time":random.uniform(0,data[0]["Time"]),
            "Drag": 1.5,
            "Alpha": 255,
            "BirthTime":time.time(),
            "Decay": 255 / (data[0]["Time"] * 60),
            "Style": data[0].get("Style") or "linear"
        })

# ------------------ CREATE ------------------
def create_particle(data, window):
    uniqueid = data["Id"]

    particledata[uniqueid] = [data, {}]

    threading.Thread(
        target=removeparticle,
        args=(uniqueid, data["Time"]),
        daemon=True
    ).start()

    emit_particle(uniqueid, window)

# ------------------ MOVE ------------------
def move(window):

    def movethread(data, window):

        for key in list(data.keys()):
            p = data[key]

            X = p["X"]
            Y = p["Y"]
            GoalX = p["GoalX"]
            GoalY = p["GoalY"]
            Time=p["Time"]
            speed = p["Speed"]
            IpX=p['InitialPositions']["x"]
            IpY=p['InitialPositions']["y"]
            # direction
            dx = GoalX - X
            dy = GoalY - Y
            dist = math.sqrt(dx*dx + dy*dy)
          
            if dist != 0:
                dx /= dist
                dy /= dist

            # move
            if p["Drag"]!=None:
                if p["LiveSpeed"]<=0:
                    p["LiveSpeed"]= 0
                else:
                    p["LiveSpeed"] = speed-p["Drag"]*(time.time()-p["BirthTime"])
                #v = u + at
            X += dx * p["LiveSpeed"]
            Y += dy * p["LiveSpeed"]

            p["X"] = X
            p["Y"] = Y

            
            p["Alpha"] -=tween.tween(p["Style"],(255 * p["Speed"]) / dist)
            if p["Alpha"] <= 0:
                del data[key]
                continue

      
            r, g, b = p["Colour"]
            alpha = int(max(0, min(255, p["Alpha"])))
            color = (int(r), int(g), int(b), alpha)

      
            if p["Shape"] == "rect":
                w = p["Size"]["w"]
                h = p["Size"]["h"]

                surf = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.rect(surf, color, (0, 0, w, h), border_radius=6)
                window.blit(surf, (X, Y))

            elif p["Shape"] == "circle":
                rsize = p["Size"]["r"]

                surf = pygame.Surface((rsize*2, rsize*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, (rsize, rsize), rsize)
                window.blit(surf, (X - rsize, Y - rsize))

            # remove if reached goal
            if abs(X - GoalX) < 1 and abs(Y - GoalY) < 1:
                del data[key]

   
    for key, values in list(particledata.items()):
        movethread(values[1], window)

PRESETS = {
    "fire": {
        "Id": "fire_burst",
        "Number": 40,
        "Position": {"x": 400, "y": 500},
        "Spread": 25,
        "MaxDistance": 160,
        "Colour": (255, 120, 20),
        "Size": {"w": 6, "h": 6},
        "Shape": "rect",
        "Speed": 4,
        "Time": 1.5,
    },
    "water": {
        "Id": "water_burst",
        "Number": 35,
        "Position": {"x": 400, "y": 500},
        "Spread": 40,
        "MaxDistance": 130,
        "Colour": (30, 180, 255),
        "Size": {"r": 5},
        "Shape": "circle",
        "Speed": 3,
        "Time": 1.8,
    },
    "beam": {
        "Id": "white_beam",
        "Number": 20,
        "Position": {"x": 400, "y": 500},
        "Spread": 5,           # very tight
        "MaxDistance": 220,
        "Colour": (240, 240, 255),
        "Size": {"r": 3},
        "Shape": "circle",
        "Speed": 5,
        "Time": 1.2,
    },
    "confetti": {
        "Id": "confetti",
        "Number": 60,
        "Position": {"x": 400, "y": 500},
        "Spread": 90,          # wide fan
        "MaxDistance": 180,
        "Colour": (255, 80, 160),
        "Size": {"w": 5, "h": 5},
        "Shape": "rect",
        "Speed": 3,
        "Time": 2.0,
    },
}