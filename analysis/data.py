import os
import re
import pickle

from utils import *
from config import *

def lazy_load_node_pkl(node_pkl_filename_template):
    def decorator(func):
        def wrapper(data_reader, node_id):
            node_pkl_filename = node_pkl_filename_template.format(node_id = node_id)
            pkl_path = os.path.join(DATA_PATH, node_pkl_filename)

            try:
                ret = load_pkl(pkl_path)
                print(f"Load data from existing pkl {pkl_path}")
                return ret
            except Exception as e:
                print(f"No existing pkl found in {pkl_path}, will generate it from raw data".format(pkl_path, e))

            ret = func(data_reader, node_id)
            save_pkl(ret, pkl_path)

            return ret
        return wrapper
    return decorator

class DataReader:

    def __init__(self):
        self.data_path = DATA_PATH
        self.tr_filepath = os.path.join(self.data_path, "mix.tr.txt")
        self.simu_stdout_filepath = os.path.join(self.data_path, "stdout.txt")
        self.ts_window = TS_WINDOW

    @lazy_load_node_pkl("node_{node_id}_ts_deque.pkl")
    def get_node_data(self, node_id):

        node_data = []

        f = open(self.tr_filepath, "r")
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

    @lazy_load_node_pkl("node_{node_id}_ts_bw.pkl")
    def get_node_bandwidth(self, node_id):
        bandwidth = {} # {time: size}
        node_data = self.get_node_data(node_id)
        for each_event in node_data:
            if (each_event["event"] != "Dequ"):
                continue
            ts_wrap_down = (each_event["ts"] // self.ts_window) * self.ts_window
            add_to_dict(bandwidth, ts_wrap_down, 0)
            bandwidth[ts_wrap_down] += each_event["pkg_size"]
        
        return bandwidth

    def get_node_running_data(self, node_id):
        pattern = r"(\d+) (\d+) (.*?) ([0-9\.]+)(.*)"
        # {time: data}
        node_stage = {}
        node_alpha = {}
        node_rate = {}
        node_target_rate = {} 
        f = open(self.simu_stdout_filepath, "r")
        for line in f:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                ts = int(match.group(1))
                tmp_node_id = int(match.group(2))
                event_type = match.group(3)
                event_value = match.group(4)
                extra = match.group(5)
                if (tmp_node_id != node_id):
                    continue
                if (event_type == "stage"):
                    node_stage[ts] = int(event_value)
                elif (event_type == "alpha"):
                    node_alpha[ts] = float(event_value)
                elif (event_type == "rate"):
                    node_rate[ts] = int(event_value)
                elif (event_type == "target_rate"):
                    node_target_rate[ts] = int(event_value)

        return node_alpha, node_rate, node_target_rate, node_stage
