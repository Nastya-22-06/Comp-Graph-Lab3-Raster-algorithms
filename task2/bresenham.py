import tkinter as tk
from PIL import Image, ImageTk

WIDTH = 800
HEIGHT = 600
BACKGROUND = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
first_point = None

root = tk.Tk()
root.title("Задание 2 — целочисленный алгоритм Брезенхема")
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


def bresenham(x0, y0, x1, y1):
    pixels = image.load()
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy

    while True:
        if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
            pixels[x0, y0] = LINE_COLOR
        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * error
        if e2 >= dy:
            error += dy
            x0 += sx
        if e2 <= dx:
            error += dx
            y0 += sy


def on_click(event):
    global first_point
    point = (event.x, event.y)

    if first_point is None:
        clear_image()
        first_point = point
        image.putpixel(point, LINE_COLOR)
    else:
        bresenham(first_point[0], first_point[1], point[0], point[1])
        first_point = None

    refresh()


canvas.bind("<Button-1>", on_click)
refresh()
root.mainloop()
