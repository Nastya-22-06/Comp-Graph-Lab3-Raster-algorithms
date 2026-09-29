import tkinter as tk
from PIL import Image, ImageTk

WIDTH = 1000
HEIGHT = 700
BACKGROUND = (255, 255, 255)
VERTEX_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
vertices = []

root = tk.Tk()
root.title("Задание 3 — градиентное окрашивание произвольного треугольника")
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


def barycentric(px, py, a, b, c):
    denominator = (
        (b[1] - c[1]) * (a[0] - c[0])
        + (c[0] - b[0]) * (a[1] - c[1])
    )
    if denominator == 0:
        return None

    alpha = (
        (b[1] - c[1]) * (px - c[0])
        + (c[0] - b[0]) * (py - c[1])
    ) / denominator
    beta = (
        (c[1] - a[1]) * (px - c[0])
        + (a[0] - c[0]) * (py - c[1])
    ) / denominator
    gamma = 1.0 - alpha - beta
    return alpha, beta, gamma


def rasterize_triangle(a, b, c):
    min_x = max(0, min(a[0], b[0], c[0]))
    max_x = min(WIDTH - 1, max(a[0], b[0], c[0]))
    min_y = max(0, min(a[1], b[1], c[1]))
    max_y = min(HEIGHT - 1, max(a[1], b[1], c[1]))
    pixels = image.load()

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            weights = barycentric(x, y, a, b, c)
            if weights is None:
                return

            alpha, beta, gamma = weights
            if alpha >= 0 and beta >= 0 and gamma >= 0:
                red = round(alpha * 255)
                green = round(beta * 255)
                blue = round(gamma * 255)
                pixels[x, y] = (red, green, blue)


def on_click(event):
    global vertices

    if len(vertices) == 3:
        vertices = []
        clear_image()

    point = (event.x, event.y)
    vertices.append(point)

    size = 4
    pixels = image.load()
    for dx in range(-size, size + 1):
        x = point[0] + dx
        y = point[1]
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            pixels[x, y] = VERTEX_COLORS[len(vertices) - 1]
    for dy in range(-size, size + 1):
        x = point[0]
        y = point[1] + dy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            pixels[x, y] = VERTEX_COLORS[len(vertices) - 1]

    if len(vertices) == 3:
        rasterize_triangle(vertices[0], vertices[1], vertices[2])

    refresh()


canvas.bind("<Button-1>", on_click)
refresh()
root.mainloop()
