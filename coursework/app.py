from PIL import Image, ImageDraw
from coursework.filters import clamp
import numpy as np
from math import sqrt, fabs

pic_name = "pic4"
pic_prepared_name = pic_name + "_prepared"

image = Image.open(pic_name + ".png")
prepared_image = Image.open(pic_prepared_name + ".png")
rgb_image = image.convert('RGB')
rgb_prepared_image = prepared_image.convert('RGB')


def euclid_metrics(v1, v2):
    return sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)


def manhattan_metrics(v1, v2):
    return max(fabs(v1[0] - v2[0]), fabs(v1[1] - v2[1]))


def clear_sample(sample, get_key, f):
    sample.sort(key=lambda x: get_key(x))
    l = len(sample)

    Q1 = get_key(sample[int(1 / 4 * l)])
    Q3 = get_key(sample[int(3 / 4 * l)])
    X1 = Q1 - 3 / 2 * (Q3 - Q1)
    X2 = Q3 + 3 / 2 * (Q3 - Q1)
    return list(filter(lambda x: f(x, X1, X2), sample))


def handle_image(image, image_map):
    image_draw = ImageDraw.Draw(image)
    buf_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    buf_draw = ImageDraw.Draw(buf_image)

    pix = image_map.load()
    width = image_map.size[0]  # Определяем ширину.
    height = image_map.size[1]  # Определяем высоту.
    sum = [0, 0]
    size = (width - 10) * (height - 10)
    sample = []
    for i in range(5, width - 5):
        for j in range(5, height - 5):
            c = pix[i, j][0]
            if c != (0, 0, 0):
                sum[0] += i
                sum[1] += j
    mean = [sum[0] / size, sum[1] / size]

    sum = 0
    for j in range(5, height - 5):
        for i in range(5, width - 5):
            c = pix[i, j][0]
            if c != 0:
                d = manhattan_metrics((i, j), mean)
                sum += d
                sample.append({"d": d, "pos": (i, j)})

    sample = clear_sample(sample, lambda x: x['d'], lambda x, X1, X2: X1 < x['d'] < X2)
    sample = clear_sample(sample, lambda x: x['pos'][0], lambda x, X1, X2: X1 < x['pos'][0] < X2)
    sample = clear_sample(sample, lambda x: x['pos'][1], lambda x, X1, X2: X1 < x['pos'][1] < X2)

    for _ in sample:
        buf_draw.point(_["pos"], (0, 255, 0))

    buf_image.show()

    buf_pix = buf_image.load()
    borders_up_down = set()
    for i in range(width):
        min = height
        max = 0
        for j in range(height):
            c = buf_pix[i, j]
            if c != (0, 0, 0, 0):
                if j < min:
                    min = j
                if j > max:
                    max = j
        if min > max:
            continue
        borders_up_down.add((i, max))
        borders_up_down.add((i, min))

    borders_left_right = set()
    for i in range(height):
        min = width
        max = 0
        for j in range(width):
            c = buf_pix[j, i]
            if c != (0, 0, 0, 0):
                if j < min:
                    min = j
                if j > max:
                    max = j
        if min > max:
            continue
        borders_left_right.add((max, i))
        borders_left_right.add((min, i))

    borders = set.intersection(borders_up_down, borders_left_right)

    for p in borders:
        image_draw.point(p, (0, 0, 0))
    image.show()

    return borders


def pop_closer(points, target):
    LIMIT_D = 50
    min = -1
    p = None
    for point in points:
        d = manhattan_metrics(point, target)
        if min > d or min == -1:
            min = d
            p = point

    if p:
        # if min > LIMIT_D:
        #     return None
        print(min)
        points.remove(p)
        return p


def build_broken_line(points):
    # points = points.copy()
    broken_line = []
    start = points.pop()
    current = start
    while len(points) != 0:
        p = pop_closer(points, current)
        if p == None:
            return broken_line
        broken_line.append(p)
        current = p
    # broken_line.append(start)
    return broken_line


def pop_closer_end(ends, target):
    min = -1
    deleted = None
    nearest = None
    remnant = None
    for el in ends:
        (start, end) = el
        d1 = manhattan_metrics(start, target)
        d2 = manhattan_metrics(end, target)
        if min > d1 or min == -1:
            min = d1
            deleted = el
            nearest = start
            remnant = end
        if min > d2 or min == -1:
            deleted = el
            min = d2
            nearest = end
            remnant = start

    if nearest and remnant:
        ends.remove(deleted)
        return nearest, remnant


def connect_ends(ends):
    connections = []
    (end, start) = ends.pop()
    current = start
    while len(ends) != 0:
        nearest, new_current = pop_closer_end(ends, current)
        connections.append((current, nearest))
        current = new_current
    connections.append((end, current))
    return connections


borders_points = handle_image(rgb_image, rgb_prepared_image)
image_draw = ImageDraw.Draw(image)


border_broken_line_ends = []
while len(borders_points) != 0:
    broken_line = build_broken_line(borders_points)
    l = len(broken_line)
    if l < 3:
        continue
    border_broken_line_ends.append(((broken_line[0], broken_line[l-1])))

    for i in range(l-1):
        p1 = broken_line[i]
        p2 = broken_line[i + 1]
        image_draw.line((p1[0], p1[1], p2[0], p2[1]), fill=128, width=3)

connections = connect_ends(border_broken_line_ends)
l = len(connections)
# for i in range(l):
#     p1 = connections[i]
#     image_draw.line((p1[0][0], p1[0][1], p1[1][0], p1[1][1]), fill=128, width=3)


for p in borders_points:
    image_draw.point(p, (0, 0, 0))

image.show()
image.save(pic_name + "_handled.png")
