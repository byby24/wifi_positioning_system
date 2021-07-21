from json import load, dump
from AccessPoint import AccessPoint

configuration_path = "configuration.json"


def parse_to_ap_class(aps: dict):
    """
    :param aps: json dict of known access points
    :return: json dict of the access points converted to AccessPoint struct
    """
    for key in aps:
        aps[key] = AccessPoint(aps[key])
    return aps


def get_json_data(requested_environments: str, config_path=configuration_path):
    """
    :param config_path: the path to configuration
    :param requested_environments: the environment that its settings need to be loaded from the json file
    :return: the setting -
                all known aps (dict)
                path loss (int)
    """
    with open(config_path, "r+") as json_file:
        data = load(json_file)
        json_file.close()

    return parse_to_ap_class(data[requested_environments]["aps"]), \
           data[requested_environments]["path_loss"]


def get_all_environments(config_path=configuration_path):
    """
    :param config_path: the path to the configuration
    :return: list containing all environments
    """
    with open(config_path, "r") as json_file:
        data = load(json_file)
        json_file.close()
    return [key for key in data]