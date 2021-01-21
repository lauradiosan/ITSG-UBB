import json
from typing import Dict


def read_config(config_path: str) -> Dict[str, any]:
    """
    Reads a .json config from a given path.
    :param config_path: the config path
    :return: the json dict.
    """
    with open(file=config_path, mode="r") as json_data_file:
        data = json.load(json_data_file)

    return data
