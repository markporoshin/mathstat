import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from math import sqrt, pi, exp, pow, factorial, fabs


def show(description, values, cap, i):
    ax = plt.subplot(1, 3, i)
    sns.distplot(values)
    x = sorted(set(values))
    y = [description['destiny'](_) for _ in x]
    plt.plot(x, y, 'r-')
    plt.title(description['name'])
    plt.ylabel("destiny")
    plt.xlabel("number - %s" % cap)
    plt.grid()
    destiny = mpatches.Patch(color='red', label='плотность')
    kde = mpatches.Patch(color='blue', label='ядерная оценка')
    plt.legend(handles=[destiny, kde])


capacities = [10, 50, 1000]
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
        'destiny': lambda x: 1 / pi * ( 1 / (x*x + 1))
    },
    {
        'name': 'laplace',
        'func': lambda size: np.random.laplace(0, 1/sqrt(2), size=size),
        'destiny': lambda x: (1 / sqrt(2)) * exp(-sqrt(2) * fabs(x))
    },
    {
        'name': 'uniform',
        'func': lambda size: np.random.uniform(-sqrt(3), sqrt(3),size=size),
        'destiny': lambda x: 1 / (2 * sqrt(3)) if (fabs(x) <= sqrt(3)) else 0
    },
]

for dis in distributions:
    i = 1
    plt.subplot(1, 3, 1)
    for cap in capacities:
        show(dis, dis['func'](cap), cap, i)
        i += 1
    plt.show()



