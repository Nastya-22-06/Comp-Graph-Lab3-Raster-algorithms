import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.withdraw()
image_path = filedialog.askopenfilename(
    title="Выберите исходное изображение",
    filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Все файлы", "*.*")],
)
if not image_path:
    root.destroy()
    raise SystemExit

source = Image.open(image_path).convert("RGB")
result = source.copy()
width, height = source.size
contour = []

root.deiconify()
root.title("Задание 1в — выделение границы")
canvas = tk.Canvas(root, width=width, height=height, highlightthickness=0)
canvas.pack()
photo = None

# Нумерация соседей как на схеме из лекции: 0 справа, 6 снизу.
OFFSETS = [
    (1, 0), (1, -1), (0, -1), (-1, -1),
    (-1, 0), (-1, 1), (0, 1), (1, 1),
]


def refresh():
    global photo
    photo = ImageTk.PhotoImage(result)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=photo)


def is_inside(point):
    x, y = point
    return 0 <= x < width and 0 <= y < height


def same_color(point, boundary_color):
    return is_inside(point) and source.getpixel(point) == boundary_color


def is_start_boundary(point, boundary_color):
    if not same_color(point, boundary_color):
        return False

    x, y = point
    for dx, dy in OFFSETS:
        neighbor = (x + dx, y + dy)
        if is_inside(neighbor) and source.getpixel(neighbor) != boundary_color:
            return True
    return False


def direction_index(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    try:
        return OFFSETS.index((dx, dy))
    except ValueError:
        return None


def find_next(current, search_from, boundary_color):
    # Ищем против часовой стрелки, начиная с заданного направления.
    x, y = current
    for step in range(8):
        index = (search_from + step) % 8
        dx, dy = OFFSETS[index]
        candidate = (x + dx, y + dy)
        if same_color(candidate, boundary_color):
            return candidate
    return None


def trace_boundary(start, boundary_color):
    points = [start]

    # Для первой точки первая попытка — вниз (направление 6).
    first_next = find_next(start, 6, boundary_color)
    if first_next is None or first_next == start:
        return points

    points.append(first_next)
    previous = start
    current = first_next

    for _ in range(width * height * 8):
        incoming = direction_index(previous, current)
        if incoming is None:
            break

        # Начинаем с направления на 90 градусов по часовой стрелке
        # относительно направления, по которому пришли.
        search_from = (incoming - 2) % 8
        nxt = find_next(current, search_from, boundary_color)
        if nxt is None:
            break

        if current == start and nxt == first_next:
            break

        previous, current = current, nxt
        points.append(current)

        if current == start:
            incoming = direction_index(previous, current)
            if incoming is not None:
                search_from = (incoming - 2) % 8
                check = find_next(current, search_from, boundary_color)
                if check == first_next:
                    points.pop()
                    break

    # В экранных координатах положительная площадь соответствует обходу по часовой стрелке.
    if len(points) >= 3:
        area2 = 0
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            area2 += x1 * y2 - x2 * y1

        if area2 < 0:
            points = [points[0]] + list(reversed(points[1:]))

    return points


def on_click(event):
    global result, contour
    start = (event.x, event.y)
    if not is_inside(start):
        return

    boundary_color = source.getpixel(start)
    if not is_start_boundary(start, boundary_color):
        return

    contour = trace_boundary(start, boundary_color)

    result = source.copy()
    pixels = result.load()
    for x, y in contour:
        pixels[x, y] = (255, 0, 0)
    refresh()


canvas.bind("<Button-1>", on_click)
refresh()
root.mainloop()
