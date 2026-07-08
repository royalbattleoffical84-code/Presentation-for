import turtle
import json
import time
import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_FILE = os.path.join(BASE_DIR, "mahakal_paths.json")
FINAL_IMAGE = os.path.join(BASE_DIR, "mahakal_exact.gif")

PENCIL_DELAY = 0
NEON_DELAY = 0
PATH_DELAY = 0
UPDATE_EVERY_POINTS = 120

# RGB colors, safer than hex in turtle
BLACK = (0, 0, 0)
PENCIL_DARK = (77, 77, 77)
PENCIL_WHITE = (255, 255, 255)
BLUE_GLOW = (0, 109, 255)
BLUE_MAIN = (0, 183, 255)
BLUE_BRIGHT = (143, 243, 255)


screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.bgcolor("black")
screen.title("Mahakal Sketch Making Exact Final - DcodeVerse")
screen.colormode(255)
screen.tracer(0, 0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

brand = turtle.Turtle()
brand.hideturtle()
brand.speed(0)


def clean_point(point):
    """
    Converts one point into valid turtle coordinates.
    Supports: [x, y] or (x, y)
    Skips bad values safely.
    """
    try:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            return None

        x = float(point[0])
        y = float(point[1])

        if not math.isfinite(x) or not math.isfinite(y):
            return None

        return x, y

    except Exception:
        return None


def clean_path(path):
    """
    Cleans one full path.
    """
    if not isinstance(path, list):
        return []

    cleaned = []

    for point in path:
        fixed = clean_point(point)
        if fixed is not None:
            cleaned.append(fixed)

    return cleaned


def load_paths():
    """
    Loads and cleans paths from mahakal_paths.json.
    """
    if not os.path.exists(PATH_FILE):
        raise FileNotFoundError(f"File not found: {PATH_FILE}")

    with open(PATH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "paths" not in data:
        raise KeyError("JSON file must contain a 'paths' key.")

    raw_paths = data["paths"]

    if not isinstance(raw_paths, list):
        raise ValueError("'paths' must be a list.")

    paths = []

    for path in raw_paths:
        cleaned = clean_path(path)
        if len(cleaned) >= 2:
            paths.append(cleaned)

    if not paths:
        raise ValueError("No valid paths found in mahakal_paths.json")

    return paths


def fit_screen_to_paths(paths):
    """
    Automatically fits turtle screen coordinates according to drawing size.
    """
    all_x = []
    all_y = []

    for path in paths:
        for x, y in path:
            all_x.append(x)
            all_y.append(y)

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    padding_x = 100
    padding_y_top = 100
    padding_y_bottom = 180

    screen.setworldcoordinates(
        min_x - padding_x,
        min_y - padding_y_bottom,
        max_x + padding_x,
        max_y + padding_y_top
    )

    return min_y


def draw_path(path, color, width, delay):
    """
    Draws one path safely.
    """
    if len(path) < 2:
        return

    t.pencolor(color)
    t.pensize(width)

    t.penup()
    t.goto(path[0][0], path[0][1])
    t.pendown()

    for i, (x, y) in enumerate(path[1:], start=1):
        try:
            t.goto(x, y)
        except turtle.TurtleGraphicsError:
            continue

        if i % UPDATE_EVERY_POINTS == 0:
            screen.update()
            if delay > 0:
                time.sleep(delay)

    t.penup()
    screen.update()

    if PATH_DELAY > 0:
        time.sleep(PATH_DELAY)


def branding(brand_y):
    """
    Adds Dcodeverse branding at bottom.
    """
    brand.clear()
    brand.penup()

    brand.goto(0, brand_y - 70)
    brand.color(BLUE_MAIN)
    brand.write("DCODEVERSE", align="center", font=("Arial", 28, "bold"))

    brand.goto(0, brand_y - 105)
    brand.color(BLUE_BRIGHT)
    brand.write("CODE • CREATE • CONQUER", align="center", font=("Arial", 12, "bold"))

    screen.update()


def draw_all_paths(paths, color, width, delay, phase_name):
    """
    Draws all paths in one phase.
    """
    print(f"Starting: {phase_name}")

    for index, path in enumerate(paths, start=1):
        draw_path(path, color, width, delay)

        if index % 50 == 0:
            print(f"{phase_name}: {index}/{len(paths)} paths done")

    print(f"Completed: {phase_name}")


def reveal_exact():
    """
    Final exact image reveal in Turtle window.
    Works only if mahakal_exact.gif exists.
    """
    t.clear()
    brand.clear()

    if not os.path.exists(FINAL_IMAGE):
        brand.penup()
        brand.goto(0, 0)
        brand.color(BLUE_BRIGHT)
        brand.write(
            "Final GIF not found: mahakal_exact.gif",
            align="center",
            font=("Arial", 20, "bold")
        )
        screen.update()
        print("Warning: mahakal_exact.gif not found. Neon sketch is shown instead.")
        return

    try:
        screen.bgpic(FINAL_IMAGE)
        screen.update()
        print("Final exact GIF image revealed.")

    except turtle.TurtleGraphicsError as e:
        brand.penup()
        brand.goto(0, 0)
        brand.color(BLUE_BRIGHT)
        brand.write(
            "Could not load final GIF image",
            align="center",
            font=("Arial", 20, "bold")
        )
        screen.update()
        print("GIF reveal error:", e)


def main():
    try:
        paths = load_paths()
        print(f"Loaded {len(paths)} valid paths.")

        brand_y = fit_screen_to_paths(paths)
        branding(brand_y)

        # Phase 1: pencil sketch
        draw_all_paths(paths, PENCIL_DARK, 5, PENCIL_DELAY, "Dark pencil sketch")
        draw_all_paths(paths, PENCIL_WHITE, 1, PENCIL_DELAY, "White pencil sketch")

        time.sleep(0.5)

        # Phase 2: neon blue sketch
        draw_all_paths(paths, BLUE_GLOW, 7, NEON_DELAY, "Blue glow sketch")
        draw_all_paths(paths, BLUE_MAIN, 3, NEON_DELAY, "Blue main sketch")
        draw_all_paths(paths, BLUE_BRIGHT, 1, NEON_DELAY, "Blue bright sketch")

        time.sleep(0.7)

        # Phase 3: final exact image
        reveal_exact()

        print("Done: sketch-making completed.")

    except Exception as e:
        screen.clear()
        screen.bgcolor("black")

        error_turtle = turtle.Turtle()
        error_turtle.hideturtle()
        error_turtle.penup()
        error_turtle.color("white")
        error_turtle.goto(0, 0)
        error_turtle.write(
            f"Error:\n{e}",
            align="center",
            font=("Arial", 16, "bold")
        )

        print("Error:", e)

    turtle.done()


if __name__ == "__main__":
    main()