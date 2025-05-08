import pyautogui
import random
import time
import math
import keyboard
from threading import Event
# Screen size
screen_width, screen_height = pyautogui.size()
MARGIN = 50  # Stay 10px away from screen corners

def clamp(val, min_val, max_val):
    return max(min_val, min(max_val, val))

# Start from current mouse position, clamped within safe screen area
last_x, last_y = pyautogui.position()
last_x = clamp(last_x, MARGIN, screen_width - MARGIN)
last_y = clamp(last_y, MARGIN, screen_height - MARGIN)

def random_mouse_move():
    global last_x, last_y

    x_end = random.randint(MARGIN, screen_width - MARGIN)
    y_end = random.randint(MARGIN, screen_height - MARGIN)

    # Clamp all coordinates
    last_x = clamp(last_x, MARGIN, screen_width - MARGIN)
    last_y = clamp(last_y, MARGIN, screen_height - MARGIN)
    x_end = clamp(x_end, MARGIN, screen_width - MARGIN)
    y_end = clamp(y_end, MARGIN, screen_height - MARGIN)

    pyautogui.moveTo(last_x, last_y)

    base_speed = random.uniform(0.01, 0.03) * 0.3
    move_duration = random.randint(15, 30)
    movement_type = random.choice(['line', 'parabola', 'reverse_parabola', 'oval'])

    start_time = time.time()

    if movement_type == 'line':
        steps = random.randint(50, 100)
        for i in range(steps):
            random_variation_x = random.uniform(-3, 3)
            random_variation_y = random.uniform(-3, 3)

            x = last_x + (x_end - last_x) * i / steps + random_variation_x
            y = last_y + (y_end - last_y) * i / steps + random_variation_y

            x = clamp(x, MARGIN, screen_width - MARGIN)
            y = clamp(y, MARGIN, screen_height - MARGIN)

            speed_variation = random.uniform(0.005, 0.01) * 0.3
            duration = base_speed + speed_variation
            pyautogui.moveTo(x, y, duration=duration)
            time.sleep(random.uniform(0.02, 0.05))

            if random.random() < 0.1:
                base_speed *= 1.4

            if time.time() - start_time > move_duration:
                break

    elif movement_type in ['parabola', 'reverse_parabola']:
        steps = random.randint(50, 100)
        a = random.uniform(-0.05, 0.05)
        b = random.uniform(-0.05, 0.05)
        c = random.uniform(0, screen_height)

        for i in range(steps):
            t = i / steps
            x = last_x + (x_end - last_x) * t
            y = a * (x - last_x)**2 + b * (x - last_x) + c

            if movement_type == 'reverse_parabola':
                y = -y + screen_height

            x = clamp(x, MARGIN, screen_width - MARGIN)
            y = clamp(y, MARGIN, screen_height - MARGIN)

            speed_variation = random.uniform(0.005, 0.01) * 0.3
            duration = base_speed + speed_variation
            pyautogui.moveTo(x, y, duration=duration)
            time.sleep(random.uniform(0.02, 0.05))

            if random.random() < 0.1:
                base_speed *= 1.4

            if time.time() - start_time > move_duration:
                break

    elif movement_type == 'oval':
        a = random.randint(100, 300)
        b = random.randint(50, 150)

        x_center = clamp(last_x + random.randint(-50, 50), MARGIN + a, screen_width - MARGIN - a)
        y_center = clamp(last_y + random.randint(-50, 50), MARGIN + b, screen_height - MARGIN - b)

        for angle in range(0, 360, random.randint(10, 20)):
            x = x_center + int(a * math.cos(math.radians(angle)))
            y = y_center + int(b * math.sin(math.radians(angle)))

            x = clamp(x, MARGIN, screen_width - MARGIN)
            y = clamp(y, MARGIN, screen_height - MARGIN)

            speed_variation = random.uniform(0.005, 0.01) * 0.3
            duration = base_speed + speed_variation
            pyautogui.moveTo(x, y, duration=duration)
            time.sleep(random.uniform(0.02, 0.05))

            if random.random() < 0.1:
                base_speed *= 1.4

            if time.time() - start_time > move_duration:
                break

    # Save last mouse position for next movement
    last_x, last_y = pyautogui.position()

# Loop forever with random delays between movements
stop_event = Event()

keyboard.add_hotkey('esc', lambda: stop_event.set())

print("Running. Press ESC to stop.")

while not stop_event.is_set():
    random_mouse_move()
    time.sleep(random.uniform(0.5, 1.5))
