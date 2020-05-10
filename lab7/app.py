import numpy as np
from math import sqrt, pi, exp, log10 as lg
from scipy.special import erf


def maximum_likelihood_estimation(sample):
    mean = np.mean(sample)
    var = np.var(sample)
    return mean, var


def distribution(x, a=0, b=1):
    return 1 / 2 * (1 + erf((x - a) / (sqrt(2) * b)))
    # return 1 / (sqrt(2 * pi) * b) * exp(- (x - a) ** 2 / (2 * b ** 2))


def get_xsi(k, a):
    return 12.6


def divide_sample(sample, k, mean, step):
    deltas = []
    ni = []
    point = min(sample) - 1
    print("delta i")
    print("-inf", end=' ')
    for i in range(int(-k / 2), k - int(k / 2)):
        prev_point = point
        point = mean + i * step
        deltas.append(point)
        print(str(point), end=' ')
        ni.append(len([_ for _ in sample if prev_point < _ < point]))
    ni.append(len([_ for _ in sample if point < _]))
    print("inf")
    return ni, deltas


def count_pi(deltas, distribution):
    summ = 0
    n = len(deltas)
    # print("pi:")
    pi = [distribution(deltas[0])]
    print('distrib')
    print(distribution(deltas[0]), end=' ')
    # print(str(pi[0]), end=' ')
    summ += pi[0]
    for i in range(1, n):
        pi.append(distribution(deltas[i]) - distribution(deltas[i - 1]))
        print(f"{distribution(deltas[i])}-{distribution(deltas[i - 1])}", end=' ')
        # print(str(pi[i]), end=' ')
        summ += pi[i]
    pi.append(1 - distribution(deltas[n - 1]))
    print(f"1-{distribution(deltas[n - 1])}", end=' ')
    summ += pi[n - 1]
    # print(f"{str(pi[n - 1])} summ: {summ}")
    return pi


def count_xsi_b(ns, ps, n):
    print("n * pi")
    summ = 0
    for ni, pi in zip(ns, ps):
        summ += n * pi
        print(n * pi, end=' ')
    print(f"sum {summ}\nni - n * pi")

    summ = 0
    for ni, pi in zip(ns, ps):
        summ += ni - n * pi
        print(ni - n * pi, end=' ')
    print(f"sum: {summ}\n(ni - n * pi) ** 2 / (n * pi):")

    for ni, pi in zip(ns, ps):
        print((ni - n * pi) ** 2 / (n * pi), end=' ')
    xsi = sum([(ni - n * pi) ** 2 / (n * pi) for ni, pi in zip(ns, ps)])
    print(f"\nxsi {xsi}")
    return xsi


def pearson_criterion(sample, distribution, mean, var):
    a = 0.05
    n = len(sample)
    # k = int(1.72 * n ** (1 / 3))
    k = int(1 + 3.3 * lg(n))
    xsi = get_xsi(k - 1, 1 - a)
    ns, deltas = divide_sample(sample, k, mean, 0.3)
    print(f"ni: {str(ns)}")
    ps = count_pi(deltas, distribution)
    print(f"pi: {str(ps)}")
    xsi_b = count_xsi_b(ns, ps, n)
    if xsi_b < xsi:
        return True
    return False



sample = np.random.normal(size=100)
a, b = maximum_likelihood_estimation(sample)
print(f"{a}, {b}")
mle_dist = lambda x: distribution(x, a, b)
pearson_criterion(sample, mle_dist, a, b)
