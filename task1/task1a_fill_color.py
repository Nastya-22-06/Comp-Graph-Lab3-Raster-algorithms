import sys
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

WIDTH = 800
HEIGHT = 600
BOUNDARY_COLOR = (0, 0, 0)
FILL_COLOR = (70, 130, 180)
BACKGROUND_COLOR = (255, 255, 255)

sys.setrecursionlimit(200000)

image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
draw = ImageDraw.Draw(image)
last_point = None

root = tk.Tk()
root.title("Задание 1а — заливка цветом")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack()
photo = None


def refresh():
    global photo
    photo = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=photo)


def span_fill(x, y, old_color, new_color):
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return

    pixels = image.load()
    if pixels[x, y] != old_color or old_color == new_color:
        return

    left = x
    while left - 1 >= 0 and pixels[left - 1, y] == old_color:
        left -= 1

    right = x
    while right + 1 < WIDTH and pixels[right + 1, y] == old_color:
        right += 1

    # Закрашиваем найденную горизонтальную серию.
    for px in range(left, right + 1):
        pixels[px, y] = new_color

    # Для каждой соседней серии выполняется один рекурсивный вызов.
    for next_y in (y - 1, y + 1):
        if not (0 <= next_y < HEIGHT):
            continue

        px = left
        while px <= right:
            if pixels[px, next_y] == old_color:
                span_fill(px, next_y, old_color, new_color)
            px += 1


def on_press(event):
    global last_point
    last_point = (event.x, event.y)


def on_drag(event):
    global last_point
    if last_point is None:
        return
    current = (event.x, event.y)
    draw.line([last_point, current], fill=BOUNDARY_COLOR, width=1)
    last_point = current
    refresh()


def on_release(_event):
    global last_point
    last_point = None


def on_fill(event):
    if not (0 <= event.x < WIDTH and 0 <= event.y < HEIGHT):
        return
    old_color = image.getpixel((event.x, event.y))
    span_fill(event.x, event.y, old_color, FILL_COLOR)
    refresh()


canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)
canvas.bind("<Button-3>", on_fill)

refresh()
root.mainloop()
