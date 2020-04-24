import numpy as np
from scipy.stats.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

ro = 1
mean = [0, 0]
cov = [[1, ro], [ro, 1]]
x, y = np.random.multivariate_normal(mean, cov, 5000).T


def quadran_coef_cor(x, y):
    mx = np.mean(x)
    my = np.mean(y)
    n1 = 0
    n2 = 0
    n3 = 0
    n4 = 0
    for xi in x:
        for yi in y:
            if xi >= mx and yi >= my:
                n1 += 1
            elif xi < mx and yi >= my:
                n1 += 1
            elif xi < mx and yi < my:
                n1 += 1
            elif xi >= mx and yi < my:
                n1 += 1
    return ((n1 + n3) - (n2 + n4)) / (len(x) * len(y))


chars = [
    {
        "name": "коеффициент пирсона",
        "count": lambda x, y: pearsonr(x, y)[0]
    },
    {
        "name": "коеффициент спирмана",
        "count": lambda x, y: spearmanr(x, y)[0]
    },
    {
        "name": "квдрантный коеф корел",
        "count": lambda x, y: quadran_coef_cor(x, y)
    },
]


for ro in [0, 0.5, 0.9]:
    mean = [0, 0]
    cov = [[1, ro], [ro, 1]]
    for cap in [20, 60, 100]:
        chars_values = {
            "коеффициент пирсона": [],
            "коеффициент спирмана": [],
            "квдрантный коеф корел": [],
        }
        for exp in range(1000):
            x, y = np.random.multivariate_normal(mean, cov, cap).T
            for char in chars:
                chars_values[char['name']].append(char['count'](x, y))
        for char in chars:
            m = np.mean(chars_values[char['name']])
            v = np.var(chars_values[char['name']])
            print("ro:%s\t\t\tname:%s\t\t\tcapacity:%s\t\t\tmean-%s\t\t\tvar-%s" % (ro, char['name'], cap, m, v))
