import numpy as np
from numpy import sign
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def minimum_square(x, y):
    xy = [xi * yi for xi, yi in zip(x, y)]

    xy_ = np.mean(xy)
    x_ = np.mean(x)
    y_ = np.mean(y)
    xx_ = np.mean(([xi * xi for xi in x]))

    b1 = (xy_ - x_ * y_) / (xx_ - x_ * x_)
    b0 = y_ - x_ * b1
    return b0, b1


def minimal_modul(x, y):
    n = len(x)
    x_med = np.median(x)
    y_med = np.median(y)
    rq = sum([sign(xi - x_med) * sign(yi - y_med) for xi, yi in zip(x, y)]) / n
    l = (n + 3) // 4
    j = n - l + 1
    sort_y = sorted(y)
    sort_x = sorted(x)
    b1r = rq * ((sort_y[j] - sort_y[l]) / (sort_x[j] - sort_x[l]))
    b0r = y_med - b1r * x_med
    return b0r, b1r


def reference(x):
    return [2 + 2 * e for e in x]


def sample(x):
    e = np.random.uniform(size=len(x))
    e_ = np.mean(e)
    return [2 + 2 * xi + (ei - e_) for xi, ei in zip(x, e)]


def sample_blowout(x):
    e = np.random.uniform(size=len(x))
    e_ = np.mean(e)
    e[0] += 10
    e[19] -= 10
    return [2 + 2 * xi + (ei - e_) for xi, ei in zip(x, e)]


methods = [
    {
        'name': 'minimum square',
        'impl': minimum_square
    },
    {
        'name': 'minimal abs',
        'impl': minimal_modul
    },
    {
        'name': 'reference',
        'impl': lambda x, y: (2, 2)
    }
]


samples = [
    {
        'name': 'simple',
        'sample': lambda x: sample(x)
    },
    {
        'name': 'blowout',
        'sample': lambda x: sample_blowout(x)
    }
]

x = [(-1.8 + i * 0.2) for i in range(20)]
for s in samples:
    i = 1
    y = s['sample'](x)
    plt.plot(x, y, 'm.')
    legends = []
    for method, style, style_names in zip(methods, ['r-', 'b-', 'g-'], ['red', 'blue', 'green']):
        b0, b1 = method['impl'](x, y)
        print('method %s, b0 %f, b1 %f' % (method['name'], b0, b1))
        plt.plot(x, [b0 + b1 * xi for xi in x], style)
        legends.append(mpatches.Patch(color=style_names, label=method['name']))
        i += 1
    plt.legend(handles=legends)
    plt.show()