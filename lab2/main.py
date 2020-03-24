import numpy as np
from math import sqrt, pi, exp, pow, factorial, fabs, ceil


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
specifications = [
    {
        "name": "M",
        "count": lambda x: np.mean(x)
    },
    {
        "name": "med",
        "count": lambda x: np.median(x)
    },
    {
        "name": "D",
        "count": lambda x: np.var(x)
    },
    {
        "name": "zr",
        "count": lambda x: (min(x)+max(x)) / 2
    },
    {
        "name": "zq",
        "count": lambda x: (x[ceil(len(x) * 1/4)] + x[ceil(len(x) * 3 / 4)]) / 2
    },
    {
        "name": "ztr",
        "count": lambda x: np.mean([x[i] for i in range(len(x)) if i > (len(x) / 4) and i < len(x) * 3 / 4])
    }
]

capacities = [10, 100, 1000]
for dist in distributions:
    print(dist["name"])
    for spec in specifications:
        print(spec["name"])
        for cap in capacities:
            print("capacity %s" % cap)
            char = []
            for i in range(1000):
                x = dist["func"](cap)
                char.append(spec["count"](x))
            print("E: %s" % np.mean(char))
            print("D: %s" % np.var(char))