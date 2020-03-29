import numpy as np
from math import sqrt, pi, exp, pow, factorial, fabs, ceil
import matplotlib.pyplot as plt

distributions = [
    {
        'name': 'normal',
        'func': lambda size: np.random.normal(size=size),
        'destiny': lambda x: 1 / sqrt(2 * pi) * exp(-x * x / 2)
    },
    {
        'name': 'poisson',
        'func': lambda size: np.random.poisson(10, size=size),
        'destiny': lambda x: (pow(10, round(x)) / factorial(round(x))) * exp(-10)
    },
    {
        'name': 'cauchy',
        'func': lambda size: np.random.standard_cauchy(size=size),
        'destiny': lambda x: 1 / pi * (1 / (x * x + 1))
    },
    {
        'name': 'laplace',
        'func': lambda size: np.random.laplace(0, 1 / sqrt(2), size=size),
        'destiny': lambda x: (1 / sqrt(2)) * exp(-sqrt(2) * fabs(x))
    },
    {
        'name': 'uniform',
        'func': lambda size: np.random.uniform(-sqrt(3), sqrt(3), size=size),
        'destiny': lambda x: 1 / (2 * sqrt(3)) if (fabs(x) <= sqrt(3)) else 0
    },
]

capacities = [20, 1000]
for dis in distributions:
    _,ax = plt.subplots()
    ax.boxplot([dis['func'](20), dis['func'](1000)], vert=False, showfliers=False)
    ax.set_title("%s" % (dis["name"]))
    ax.set_yticklabels(['20', '1000'])
    plt.show()

    for cap in capacities:
        sum = 0
        for _ in range(1000):
            sample = sorted(dis['func'](cap))
            l = len(sample)
            Q1 = sample[int(1 / 4 * l)]
            Q3 = sample[int(3 / 4 * l)]
            X1 = Q1 - 3 / 2 * (Q3 - Q1)
            X2 = Q3 + 3 / 2 * (Q3 - Q1)
            discharge = list(filter(lambda x: x < X1 or x > X2, sample))
            discharges = len(list(filter(lambda x: x < X1 or x > X2, sample)))
            sum += discharges
        print("%s-%s average discharges proportion %s" % (dis['name'], cap, sum / 1000 / cap))