import json


def dump_json(save_fpath, data):
    """Dump json

    Args:
        save_fpath (str): [description]
        data (dict): [description]
    """

    with open(save_fpath, "w") as dump_json:
        json.dump(data, dump_json)
    print(f"json has been dumped : {save_fpath}")


def load_json(load_fpath):
    """Load json

    Args:
        load_fpath (str): [description]

    Returns:
        dict: [description]
    """

    with open(load_fpath, "r") as load_json:
        data = json.load(load_json)
    print(f"json has been loaded : {load_fpath}")
    return data
