import matplotlib.pyplot as plt
import numpy as np

# Will round up x up to nearest N (e.g. to nearest 100s by N=100)
# By specifying down=True it will round down to nearest instead
def _round_to_nearest(N, x, down=False):
    if not down:
        return x - (x % -N)
    else:
        return x - (x % N)

def degree_distribution_histogram(lengths, bins=20):
    minimum, maximum = min(lengths), max(lengths)
    lower = 0.01 # round_to_nearest(100, minimum, down=True)
    upper = round(maximum*1.1)#_round_to_nearest(max_x, maximum, down=False)
    bins = np.logspace(np.log10(lower), np.log10(upper), bins)
    hist, edges = np.histogram(lengths, bins=bins, density=True)
    x = (edges[1:] + edges[:-1])/2 # midpoints


    xx, yy = zip(*[(i,j) for (i,j) in zip(x, hist) if j>0 ]) #hack to remove 0s from plot
    fig, ax = plt.subplots(figsize=(9,2.5), dpi=600)
    ax.plot(xx, yy, marker='.', color='r', label="pdf")
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel("Probability")
    ax.set_xlabel("Node degree")
    ax.legend()
    plt.plot()