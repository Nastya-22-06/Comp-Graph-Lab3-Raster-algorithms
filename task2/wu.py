import math
import tkinter as tk
from PIL import Image, ImageTk

WIDTH = 800
HEIGHT = 600
BACKGROUND = (255, 255, 255)

image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
first_point = None

root = tk.Tk()
root.title("Задание 2 — алгоритм Ву")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack()
photo = None


def refresh():
    global photo
    photo = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=photo)


def clear_image():
    global image
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)


def ipart(x):
    return math.floor(x)


def fpart(x):
    return x - math.floor(x)


def rfpart(x):
    return 1 - fpart(x)


def round_pixel(x):
    return math.floor(x + 0.5)


def plot(x, y, intensity, steep):
    if steep:
        x, y = y, x
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return

    intensity = max(0.0, min(1.0, intensity))
    value = round(255 * (1.0 - intensity))
    current = image.getpixel((x, y))[0]
    value = min(current, value)
    image.putpixel((x, y), (value, value, value))


def wu_line(x0, y0, x1, y1):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    if dx == 0:
        y_start, y_end = sorted((y0, y1))
        for y in range(y_start, y_end + 1):
            plot(x0, y, 1.0, steep)
        return

    gradient = dy / dx

    xend = round_pixel(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend
    ypxl1 = ipart(yend)
    plot(xpxl1, ypxl1, rfpart(yend) * xgap, steep)
    plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap, steep)
    intery = yend + gradient

    xend = round_pixel(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend
    ypxl2 = ipart(yend)
    plot(xpxl2, ypxl2, rfpart(yend) * xgap, steep)
    plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap, steep)

    # Два соседних пиксела получают интенсивность по расстоянию до линии.
    for x in range(xpxl1 + 1, xpxl2):
        plot(x, ipart(intery), rfpart(intery), steep)
        plot(x, ipart(intery) + 1, fpart(intery), steep)
        intery += gradient


def on_click(event):
    global first_point
    point = (event.x, event.y)

    if first_point is None:
        clear_image()
        first_point = point
        image.putpixel(point, (0, 0, 0))
    else:
        wu_line(first_point[0], first_point[1], point[0], point[1])
        first_point = None

    refresh()


canvas.bind("<Button-1>", on_click)
refresh()
root.mainloop()
