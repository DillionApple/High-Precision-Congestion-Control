import os
import sys
from matplotlib import pyplot as plt

from data import *
from utils import *
from config import *

plt.rcParams["figure.figsize"] = [50, 7]
plt.rcParams["figure.autolayout"] = True

def get_X_Y_from_ts_dict(data):
    items = data.items()
    items = sorted(items, key=lambda x: x[0])
    X = [each[0] for each in items]
    Y = [each[1] for each in items]

    return X, Y

def main(data_reader, node_id):
    data_reader.node_id = node_id
    bandwidth = data_reader.get_node_bandwidth(node_id)

    ts_list = sorted(bandwidth.keys())
    X, Y = get_X_Y_from_ts_dict(bandwidth)
    X = [each / 1000000 for each in X]
    Y = [(each * BW_MULTIPLY_UNDER_TS_WINDOW) * 8 / 1000000000 for each in Y]

    fig, ax = plt.subplots(1, 1)
    ax.plot(X, Y, color="blue", label = "Deliver Rate")
    plt.xlabel("timestamp (ms)")
    plt.ylabel("Delivery Rate (Gbps)")

    alpha, rate, target_rate, stage = data_reader.get_node_running_data(node_id)

    # plot rate
    ts_list = sorted(rate.keys())
    last_rate = 200000000000
    for ts in ts_list:
        rate[ts-1] = last_rate
        last_rate = rate[ts]
    X, Y = get_X_Y_from_ts_dict(rate)
    X = [each // TS_WINDOW * TS_WINDOW / 1000000 for each in X]
    Y = [each / 1000000000 for each in Y]
    ax.plot(X, Y, color="red", label = "Current Rate")

    # plot target rate
    ts_list = sorted(target_rate.keys())
    last_rate = 200000000000
    for ts in ts_list:
        target_rate[ts-1] = last_rate
        last_rate = target_rate[ts]
    X, Y = get_X_Y_from_ts_dict(target_rate)
    X = [each // TS_WINDOW * TS_WINDOW / 1000000 for each in X]
    Y = [each / 1000000000 for each in Y]
    plt.plot(X, Y, color="gray", label = "Target Rate")

    leg = plt.legend(loc='upper left')

    # plot alpha
    X, Y = get_X_Y_from_ts_dict(alpha)
    X = [each // TS_WINDOW * TS_WINDOW / 1000000 for each in X]
    ax2 = ax.twinx()
    plt.plot(X, Y, color="green", label = "Alpha")

    # plot stage
    ts_list = sorted(stage.keys())
    last_stage = 0
    for ts in ts_list:
        stage[ts-1] = last_stage
        last_stage = stage[ts]
    X, Y = get_X_Y_from_ts_dict(stage)
    X = [each // TS_WINDOW * TS_WINDOW / 1000000 for each in X]
    plt.plot(X, Y, "--", color="orange", label = "Stage")

    plt.ylim((0, 6.2))
    plt.xlim((PLOT_ST_MS, PLOT_EN_MS))
    
    leg2 = plt.legend(loc='upper right')

    img_save_filepath = os.path.join(DATA_PATH, "node_{}_bw.png".format(node_id))
    plt.savefig(img_save_filepath)

if __name__== "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 plot.py <node_id>")
        exit(-1)

    node_id = int(sys.argv[1])
    data_reader = DataReader()
    main(data_reader, node_id)