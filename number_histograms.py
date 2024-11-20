import numpy as np
import matplotlib.pyplot as plt
import functions.reading as rd
import functions.numbering as nd
import scipy.stats as scs

def pval_to_sigma(pval):
    '''
    https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
    https://en.wikipedia.org/wiki/Standard_score

    Alternative: np.sqrt(2)*(special.erfinv(1-pval))
    '''

    temp = (1 - pval + 1) / 2
    sigma = scs.norm.ppf(temp)
    return sigma


# region Set Up
slow_bars, fast_bars = rd.slow_and_fast_setup()

slow_bulge_num = nd.bulge_number(slow_bars)
fast_bulge_num = nd.bulge_number(fast_bars)

slow_spiral_num = nd.spiral_tightness_number(slow_bars)
fast_spiral_num = nd.spiral_tightness_number(fast_bars)
# endregion

# region Histograms

plt.figure()
plt.title("Bulge Number Distributions for Slow and Fast Bars")
plt.xlabel("Bulge Number")
plt.ylabel("Frequency (# of Counts)")
plt.hist(slow_bulge_num, density=True, label="Slow", bins=8, alpha=0.7) #, edgecolor="black") histtype='step', color="black")
plt.hist(fast_bulge_num, density=True, label="Fast", bins=8, alpha=0.7) #, edgecolor="black") histtype='step', color="red")
plt.legend()
plt.savefig("plots/histograms/bulge_intensity/bulge_number")

plt.figure()
plt.title("Spiral Tightness Number Distributions for Slow and Fast Bars")
plt.xlabel("Tightness Number")
plt.ylabel("Frequency (# of Counts)")
plt.hist(slow_spiral_num, density=True, label="Slow", bins=8, alpha=0.7) #, edgecolor="black") histtype='step', color="black")
plt.hist(fast_spiral_num, density=True, label="Fast", bins=8, alpha=0.7) #, edgecolor="black") histtype='step', color="red")
plt.legend()
plt.savefig("plots/histograms/spiral_tightness/spiral_tightness_number")


stat, crit_val, p_val = scs.anderson_ksamp([slow_bulge_num, fast_bulge_num])
print(f"Bulge Number: {pval_to_sigma(p_val)}")

stat, crit_val, p_val = scs.anderson_ksamp([slow_spiral_num, fast_spiral_num])
print(f"Spiral Tightness Number: {pval_to_sigma(p_val)}")
