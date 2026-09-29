import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

WIDTH = 800
HEIGHT = 600
BOUNDARY_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

sys.setrecursionlimit(200000)

root = tk.Tk()
root.withdraw()
pattern_path = filedialog.askopenfilename(
    title="Выберите изображение для заливки",
    filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Все файлы", "*.*")],
)
if not pattern_path:
    root.destroy()
    raise SystemExit

pattern = Image.open(pattern_path).convert("RGB")
pattern_pixels = pattern.load()
pattern_width, pattern_height = pattern.size

image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
draw = ImageDraw.Draw(image)
visited = [[False] * WIDTH for _ in range(HEIGHT)]
last_point = None

# Маленький файл повторяется, большой используется 1:1 без масштабирования.
tile_pattern = not (pattern_width >= WIDTH and pattern_height >= HEIGHT)

root.deiconify()
root.title("Задание 1б — заливка изображением")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack()
photo = None


def refresh():
    global photo
    photo = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=photo)


def can_fill(x, y, old_color):
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return False
    if visited[y][x]:
        return False
    return image.getpixel((x, y)) == old_color


def pattern_color(x, y):
    if tile_pattern:
        return pattern_pixels[x % pattern_width, y % pattern_height]
    return pattern_pixels[x, y]


def span_fill_pattern(x, y, old_color):
    if not can_fill(x, y, old_color):
        return

    pixels = image.load()

    left = x
    while left - 1 >= 0 and can_fill(left - 1, y, old_color):
        left -= 1

    right = x
    while right + 1 < WIDTH and can_fill(right + 1, y, old_color):
        right += 1

    # Заполняем найденную горизонтальную серию рисунком.
    for px in range(left, right + 1):
        visited[y][px] = True
        pixels[px, y] = pattern_color(px, y)

    # Для каждой соседней серии выполняется один рекурсивный вызов.
    for next_y in (y - 1, y + 1):
        if not (0 <= next_y < HEIGHT):
            continue

        px = left
        while px <= right:
            if can_fill(px, next_y, old_color):
                span_fill_pattern(px, next_y, old_color)
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
    global visited
    if not (0 <= event.x < WIDTH and 0 <= event.y < HEIGHT):
        return
    visited = [[False] * WIDTH for _ in range(HEIGHT)]
    old_color = image.getpixel((event.x, event.y))
    span_fill_pattern(event.x, event.y, old_color)
    refresh()


canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)
canvas.bind("<Button-3>", on_fill)

refresh()
root.mainloop()
