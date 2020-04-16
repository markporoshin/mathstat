import numpy as np
from math import sqrt, pi, exp, pow, factorial, fabs, ceil
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


distributions = [
    {
        'name': 'normal',
        'sample': lambda size: np.random.normal(size=size),
        'destiny': lambda x: 1 / sqrt(2 * pi) * exp(-x * x / 2),
        'limits': [-4, 4]
    },
    {
        'name': 'poisson',
        'sample': lambda size: np.random.poisson(10, size=size),
        'destiny': lambda x: (pow(10, round(x)) / factorial(round(x))) * exp(-10),
        'limits': [6, 14]
    },
    {
        'name': 'cauchy',
        'sample': lambda size: np.random.standard_cauchy(size=size),
        'destiny': lambda x: 1 / pi * (1 / (x * x + 1)),
        'limits': [-4, 4]
    },
    {
        'name': 'laplace',
        'sample': lambda size: np.random.laplace(0, 1 / sqrt(2), size=size),
        'destiny': lambda x: (1 / sqrt(2)) * exp(-sqrt(2) * fabs(x)),
        'limits': [-4, 4]
    },
    {
        'name': 'uniform',
        'sample': lambda size: np.random.uniform(-sqrt(3), sqrt(3), size=size),
        'destiny': lambda x: 1 / (2 * sqrt(3)) if (fabs(x) <= sqrt(3)) else 0,
        'limits': [-4, 4]
    },
]


def empirical_distributions(x, sample):
    return len([_ for _ in sample if _ < x]) / len(sample)


def kernel(u):
    return 1 / sqrt(2 * pi) * exp(-u * u / 2)


def empirical_density(x, sample):
    n = len(sample)
    sum = 0
    hn = 1.06 * sqrt(np.var(sample)) * pow(n, -1 / 5)
    for xi in sample:
        sum += kernel((x-xi) / hn)
    return sum / n / hn


capacities = [20, 60, 1000]
for dist in distributions:
    i = 1
    for cap in capacities:
        plt.subplot(1, 3, i)
        plt.title(dist['name'])
        plt.ylabel("")
        plt.xlabel("capacity - %s" % cap)
        plt.grid()
        sample = sorted(dist['sample'](size=cap))
        limited_sample = [_ for _ in sample if dist['limits'][1] >= _ >= dist['limits'][0]]
        plt.plot(limited_sample, [empirical_distributions(_, limited_sample) for _ in limited_sample], 'r-')
        plt.plot(limited_sample, [empirical_density(_, limited_sample) for _ in limited_sample], 'g-')
        i += 1
    destiny = mpatches.Patch(color='red', label='эмпирическая ф-ция распределения')
    kde = mpatches.Patch(color='green', label='эмпирическая плотность')
    plt.legend(handles=[destiny, kde])
    plt.show()