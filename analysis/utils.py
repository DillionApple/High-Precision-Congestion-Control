import pickle

def add_to_dict(data, key, default):
    if data.get(key) == None:
        data[key] = default

def save_pkl(data, path):
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_pkl(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def lazy_load_node_pkl(func):
    def wrapper(node_id, pkl_path):
        try:
            ret = load_pkl(pkl_path)
            return ret
        except Exception as e:
            print("Error while loading pickle from {}, {}".format(pkl_path, e))

        ret = func(node_id, pkl_path)

        save_pkl(ret, pkl_path)

        return ret

    return wrapper
