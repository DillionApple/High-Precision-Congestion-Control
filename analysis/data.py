import os
import pickle

from utils import *

DATA_ROOT_PATH = "./data"
NODE_PKL_PATH_TEMPLATE = os.path.join(DATA_ROOT_PATH, "node_{node_id}.pkl")
NODE_BW_PKL_PATH_TEMPLATE = os.path.join(DATA_ROOT_PATH, "node_{node_id}_bw.pkl")

TR_RAW_FILEPATH = "../simulation/mix/mix.tr"
TR_TXT_FILEPATH = "./mix.tr.txt"

def get_node_pkl_path(node_id):
    return NODE_PKL_PATH_TEMPLATE.format(node_id=node_id)

def get_node_bw_pkl_path(node_id):
    return NODE_BW_PKL_PATH_TEMPLATE.format(node_id=node_id)

@lazy_load_node_pkl
def get_node_data(node_id, pkl_path):
    """
    node_pkl_path = get_node_pkl_path(node_id)

    try:
        print("Loading saved pkl for node {}".format(node_id))
        node_data = load_pkl(node_pkl_path)
    except Exception as e:
        print(e)
        print("No pkl found, generate node data from raw data")
        node_data = []
    else:
        return node_data
    """

    f = open(TR_TXT_FILEPATH, "r")
    for line in f:
        try:
            line = line.strip().split()
        except:
            print(line)
        if line[1].split(":")[1] != str(node_id):
            continue
        if line[10] != "U":
            continue
        try:
            ts, node_id, intr, qlen, event, ecn, src_ip, dst_ip, src_port, dst_port, pkg_type, seq, tx_ts, pri_group, size = line
        except Exception as e:
            print(line)
        else:
            node_id = int(node_id[2:])
            pkg_size = int(size.split("(")[0])
            elem = {
                "ts": int(ts),
                "intr": intr,
                "qlen": int(qlen),
                "event": event,
                "ecn": int(ecn[4:]),
                "src_ip": src_ip,
                "src_port": int(src_port),
                "dst_ip": dst_ip,
                "dst_port": int(dst_port),
                "pkg_size": pkg_size
            }
            node_data.append(elem)
    
    return node_data

@lazy_load_node_pkl
def get_node_bandwidth(node_id, pkl_path):
    bandwidth = {} # {time: size}
    node_data = get_node_data(2, get_node_pkl_path(2))
    for each_event in node_data:
        if (each_event["event"] != "Dequ"):
            continue
        ts_100ms = each_event["ts"] // 10000000;
        add_to_dict(bandwidth, ts_100ms, 0)
        bandwidth[ts_100ms] += each_event["pkg_size"]
    
    return bandwidth

def main():
    # node_data = get_node_data(2, get_node_pkl_path(2))
    get_bandwidth(2, get_node_bw_pkl_path(2))
    pass

if __name__ == "__main__":
    main()