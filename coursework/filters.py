from math import fabs
import numpy as np

liner_filters = {
    "copy": {
        "size": 0,
        "frac": 1,
        "bias": 0,
        "A": [[1]]
    },
    "grad": {
        "size": 1,
        "frac": 1,
        "bias": 128,
        "A": [[-1, -1, -1],
              [-1, 8, -1],
              [-1, -1, -1]]
    },
    "blur": {
        "size": 1,
        "frac": 16,
        "bias": 0,
        "A": [[1, 2, 1],
              [2, 4, 2],
              [1, 2, 1]]
    },
    "max blur": {
        "size": 2,
        "frac": 25,
        "bias": 0,
        "A": [[1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1],
              ]
    }
}


def clamp(val, min, max):
    if val > max:
        return max
    if val < min:
        return min
    return val


def liner_filter_apply(pic_dst, pic_src, width, height, filter):

    aperture_size = filter['size']

    for i in range(width):
        for j in range(height):
            rgb = [0, 0, 0]
            for c in range(3):
                sum = 0
                for offset_x in range(0, 2 * aperture_size + 1):
                    for offset_y in range(0, 2 * aperture_size + 1):
                        x = i + offset_x - aperture_size
                        y = j + offset_y - aperture_size
                        if x < 0 or x >= width:
                            continue
                        if y < 0 or y >= height:
                            continue
                        sum += filter['A'][offset_x][offset_y] * pic_src[x, y][c]
                rgb[c] = clamp(int(sum / filter["frac"] + filter["bias"]), 0, 255)
            pic_dst.point((i, j), tuple(rgb))


def red_filter(pic_dst, pix_src, width, height):
    for i in range(width):
        for j in range(height):
            r = pix_src[i, j][0]
            g = pix_src[i, j][1]
            b = pix_src[i, j][2]
            if r == max(r, g, b):
                pic_dst.point((i, j), (255, 255, 255))


def mono_filter(pic_dst, pix_src, width, height):
    for i in range(width):
        for j in range(height):
            r = pix_src[i, j][0]
            g = pix_src[i, j][1]
            b = pix_src[i, j][2]
            s = (r + g + b) // 3
            pic_dst.point((i, j), (s, s, s))


def isGray(rgb):
    diff = max(fabs(128 - rgb[0]), fabs(128 - rgb[1]), fabs(128 - rgb[2]))
    if diff < 20:
        return True
    return False


def no_gray_filter(pic_dst, pix_gray, width, height):
    for i in range(width):
        for j in range(height):
            rgb1 = (pix_gray[i, j][0], pix_gray[i, j][1], pix_gray[i, j][2])
            if not isGray(rgb1):
                pic_dst.point((i, j), (255, 255, 255))


def median_filter(pic_dst, pix_gray, width, height, aper_size):
    for i in range(width):
        for j in range(height):
            color = [255, 255, 255]
            for c in range(3):
                buf = []
                for offset_x in range(0, 2 * aper_size + 1):
                    for offset_y in range(0, 2 * aper_size + 1):
                        x = i + offset_x - aper_size
                        y = j + offset_y - aper_size
                        if x < 0 or x >= width:
                            continue
                        if y < 0 or y >= height:
                            continue
                        buf.append(pix_gray[x, y][c])
                med = sorted(buf)[len(buf) // 2]
                color[c] = med
            pic_dst.point((i, j), tuple(color))


def swap_color_filter(pic_dst, pix_gray, width, height, c1, c2):
    for i in range(width):
        for j in range(height):
            rgb1 = (pix_gray[i, j][0], pix_gray[i, j][1], pix_gray[i, j][2])
            if rgb1 == c1:
                pic_dst.point((i, j), c2)

def green_filter(pic_dst, pix_src, width, height, c):
    for i in range(width):
        for j in range(height):
            r = pix_src[i, j][0]
            g = pix_src[i, j][1]
            b = pix_src[i, j][2]
            if g == max(r, g, b) and r != max(r, g, b)  and b != max(r, g, b):
                pic_dst.point((i, j), c)