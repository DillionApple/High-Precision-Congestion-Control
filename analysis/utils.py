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

