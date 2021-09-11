import json


def dump_json(save_fpath, data):
    """Dump json.

    Args:
        save_fpath (str): json file path to dump data
        data (dict): data to dump
    """

    with open(save_fpath, "w") as write_f:
        json.dump(data, write_f)
    print(f"json has been dumped : {save_fpath}")


def load_json(load_fpath):
    """Load json.

    Args:
        load_fpath (str): json file path to load

    Returns:
        dict: json data
    """

    with open(load_fpath, "r") as read_f:
        data = json.load(read_f)
    print(f"json has been loaded : {load_fpath}")
    return data
