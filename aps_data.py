from wifi import Cell
from time import sleep
from subprocess import call
from re import sub

wifi_interface = 'wlp3s0'


def get_available_aps(interface=wifi_interface):
    """
    :param interface: the interface to scan for, by default is the wifi_interface variable
    :return: a list of all the access points in the area, as a Cell objects from the wifi lib
    """
    scan = []
    while len(scan) == 0:
        scan = list(Cell.all(interface))
    # get list of aps-scan
    return scan


def filter_known_aps(known_aps, scan):
    """
    :param known_aps: a dict loaded from the json configuration file, containing data about the access points.
    the mac address of each cell is a key of its object in the dict
    :param scan: scan of all known aps
    :return: a list of dicts containing only the known aps
    """
    print("searching for known access points.\nthe known access points are: " + " , ".join(
        [known_aps[ap].ssid for ap in known_aps]))

    ret = [known_aps[cell.ssid] for cell in scan if cell.ssid in known_aps]

    if len(ret) == 0:
        print("scan failed")

    print(str(len(ret)) + " aps in range; " + " , ".join([ret[x].ssid for x in range(len(ret))]))

    return ret


def choose_access_points(ap_list):
    """
    :param ap_list: a list of known aps
    :return: a list of dicts, containing 3 dicts of access points
    """
    return ap_list[0:3]


def get_access_points(known_aps: dict):
    """
    :param known_aps: the dict loaded from the configuration file containing all known access points
    :return: list of 3 access points which are in the wifi range
    """
    try:
        scan = get_available_aps()
    except Exception as e:
        print("wifi is turend off")
        return None, None, None

    known_aps_in_area = filter_known_aps(known_aps, scan)

    if len(known_aps_in_area) > 2:
        return choose_access_points(known_aps_in_area)

    print("not enough access points, 3 needed, only got " + str(len(known_aps_in_area)) + ". trying again.\n")
    return None, None, None


def get_dbms(known_aps_in_area, interface=wifi_interface):
    """
    :param known_aps_in_area: list of 3 known access points which are in the wifi range
    :param interface: wifi interface to be used
    :return: the same list with the AccessPoints.dbm value loaded
    """
    scan = []
    while len(scan) == 0:
        scan = list(Cell.all(interface))
    # get list of aps-scan

    ret = []
    for cell in scan:
        for ap in known_aps_in_area:
            if cell.ssid == ap.ssid:
                ret.append(cell.signal)
                if len(ret) == 3:
                    return ret
    return ret
