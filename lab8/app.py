import numpy as np
from math import sqrt, pi, exp, log10 as lg
from scipy.special import erf
import scipy.stats as st


capacities = [20, 100]
alpha = 0.05

for n in capacities:
    print(f"capacity {n}")
    sample = np.random.normal(size=n)
    m = np.mean(sample)
    v = np.var(sample)
    s = sqrt(v)

    left_m = m - s * (st.t.ppf(1 - alpha / 2, n - 1)) / np.sqrt(n - 1)
    right_m = m + s * (st.t.ppf(1 - alpha / 2, n - 1)) / np.sqrt(n - 1)

    print(f"mean confidence interval [{left_m}, {right_m}]")

    left_s = s * np.sqrt(n) / np.sqrt(st.chi2.ppf(1 - alpha / 2, n - 1))
    right_s = s * np.sqrt(n) / np.sqrt(st.chi2.ppf(alpha / 2, n - 1))

    print(f"sqrt var confidence interval [{left_s}, {right_s}]")

    async_left_m = m - st.norm.ppf(1 - alpha / 2) / np.sqrt(n)
    async_right_m = m + st.norm.ppf(1 - alpha / 2)/np.sqrt(n)

    print(f"async mean confidence interval [{async_left_m}, {async_right_m}]")

    e = (sum(list(map(lambda el: (el - m) ** 4, sample))) / n) / s ** 4 - 3
    async_left_sigma = s/np.sqrt(1+st.norm.ppf(1-alpha / 2)*np.sqrt((e+2)/n))
    async_right_sigma = s/np.sqrt(1-st.norm.ppf(1-alpha / 2)*np.sqrt((e+2)/n))

    print(f"async sigma confidence interval [{async_left_sigma}, {async_right_sigma}]")

    pass