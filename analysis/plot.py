from matplotlib import pyplot as plt

from data import *
from utils import *

plt.rcParams["figure.figsize"] = [15, 7]
plt.rcParams["figure.autolayout"] = True

def main():
    bandwidth = get_node_bandwidth(2, get_node_bw_pkl_path(2))
    print(bandwidth)
    items = bandwidth.items()
    items = sorted(items, key=lambda x: x[0])
    X = [each[0] for each in items]
    Y = [each[1] for each in items]

    fig, ax = plt.subplots(1, 1)
    plt.plot(X, Y)
    plt.savefig("a.png")

if __name__== "__main__":
    main()