

from sense_hat import SenseHat
import time

s = SenseHat()
s.low_light = True

# ------------------ COLOR DEFINITIONS ------------------
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
R = (255, 0, 0)           # Red (heart)
O = (255, 100, 0)         # Orange (heart)

# Sun colors
B1 = (0, 170, 255)
B2 = (0, 140, 240)
B3 = (0, 90, 200)
Y1 = (255, 200, 0)
Y2a = (255, 160, 0)
Y2b = (255, 180, 30)
Y2c = (255, 130, 0)

# Battery colors
W = WHITE
B = BLACK
G = GREEN

# Cloud colors
SKY = (0, 100, 255)
CLOUD = (200, 200, 200)

# FLOWER COLOR
M = (255, 105, 180)

# ------------------ SUN FUNCTION ------------------
def sun_frame(cycle):
    glow = [Y2a, Y2b, Y2c]
    g = lambda i: glow[(i + cycle) % len(glow)]
    return [
        B1, B3, B1, B2, B1, B3, B3, B2,
        B3, g(0), B2, g(1), Y1, B2, g(2), B3,
        B1, B2, g(1), Y1, Y1, g(0), B2, B3,
        B3, Y1, Y1, Y1, Y1, Y1, g(2), B2,
        B2, g(1), Y1, Y1, Y1, Y1, Y1, B3,
        B1, B2, g(2), Y1, Y1, g(0), B2, B3,
        B3, g(0), B2, Y1, g(1), B2, g(2), B3,
        B2, B3, B1, B3, B2, B1, B3, B2,
    ]

# ------------------ HEART SCROLL ------------------
heart_grid = [
    [B, B, B, B, B, B, B, B],
    [B, R, R, B, R, R, B, B],
    [R, W, O, R, R, R, R, B],
    [R, O, R, R, R, O, R, B],
    [B, R, R, R, O, R, B, B],
    [B, B, R, R, R, B, B, B],
    [B, B, B, R, B, B, B, B],
    [B, B, B, B, B, B, B, B],
]

def scroll_icon_left_to_center_and_out(grid):
    frames = []
    padded = [[B]*8 + row + [B]*8 for row in grid]
    for shift in range(len(padded[0]) - 7):
        frame = []
        for row in padded:
            frame += row[shift:shift+8]
        frames.append(frame)
    return frames

# ------------------ BATTERY CHARGE ------------------
def battery_charge_stage(stage):
    bars = [False, False, False]
    for i in range(stage):
        bars[i] = True

    return [
        W, W, W, W, W, W, W, W,
        W, W, W, W, W, W, W, W,
        B, B, B, B, B, B, B, W,
        B, G if bars[0] else W, B, G if bars[1] else W, B, G if bars[2] else W, B, B,
        B, G if bars[0] else W, B, G if bars[1] else W, B, G if bars[2] else W, B, B,
        B, B, B, B, B, B, B, W,
        W, W, W, W, W, W, W, W,
        W, W, W, W, W, W, W, W,
    ]

# ------------------ CLOUD ANIMATION ------------------
cloud_large = [(3, 0), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]
cloud_medium = [(2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
cloud_small = [(2, 0), (0, 1), (1, 1), (2, 1), (3, 1)]

sky_width = 64
sky = [[SKY for _ in range(sky_width)] for _ in range(8)]
clouds = [
    (cloud_large, 4, 2),
    (cloud_medium, 14, 0),
    (cloud_small, 22, 3),
    (cloud_medium, 30, 4),
    (cloud_large, 40, 1),
    (cloud_small, 48, 0),
    (cloud_medium, 54, 2),
]
for shape, x_offset, y_offset in clouds:
    for x, y in shape:
        xi, yi = x + x_offset, y + y_offset
        if 0 <= xi < sky_width and 0 <= yi < 8:
            sky[yi][xi] = CLOUD

cloud_frames = []
for shift in range(sky_width - 7):
    frame = []
    for row in sky:
        frame += row[shift:shift + 8]
    cloud_frames.append(frame)

# ------------------ TEXT FUNCTION ------------------
def show_text(msg):
    s.show_message(msg.upper(), scroll_speed=0.05, text_colour=GREEN, back_colour=BLACK)
    time.sleep(0.3)

# ------------------ MAIN LOOP ------------------
while True:
    # 1. TEXT
    show_text("RE-ROUTING...")

    # 2. SUN animation (9 seconds)
    for i in range(23):
        s.set_pixels(sun_frame(i))
        time.sleep(0.4)

    # 3. TEXT
    show_text("PROTOCOL: ACTIVE")

    # 4. BATTERY CHARGE ANIMATION (3 cycles)
    for _ in range(3):
        for i in range(3):
            s.set_pixels(battery_charge_stage(i + 1))
            time.sleep(1)
        s.set_pixels(battery_charge_stage(0))
        time.sleep(0.5)

    # 5. TEXT
    show_text("TUVALU: ONLINE")

    # 6. HEART SCROLL TO CENTER AND BLINK
    heart_frames = scroll_icon_left_to_center_and_out(heart_grid)
    center_index = len(heart_frames) // 2
    for i, frame in enumerate(heart_frames):
        s.set_pixels(frame)
        time.sleep(0.2)
        if i == center_index:
            for _ in range(3):
                s.set_pixels([BLACK]*64)
                time.sleep(0.2)
                s.set_pixels(frame)
                time.sleep(0.2)

    # 7. TEXT
    show_text("WEATHER: PARTLY CLOUDY, 64F")

    # 8. CLOUDS (~9s total)
    for frame in cloud_frames:
        s.set_pixels(frame)
        time.sleep(0.3)

    # 9. TEXT
    show_text("DEFINING HOST...")

    # 10. FLOWER SCROLL
    flower_grid = [
        [B, B, B, B, B, B, B, B],
        [B, B, M, B, B, B, B, B],
        [B, M, W, M, B, B, B, B],
        [B, B, M, B, B, M, B, B],
        [B, B, B, B, M, W, M, B],
        [B, B, M, B, B, M, B, B],
        [B, M, W, M, B, B, B, B],
        [B, B, M, B, B, B, B, B],
    ]
    flower_frames = scroll_icon_left_to_center_and_out(flower_grid)
    for _ in range(2):
        for frame in flower_frames:
            s.set_pixels(frame)
            time.sleep(0.2)

    # 11. TEXT
    show_text("RE-ROUTING...")
