from aps_data import get_access_points, get_dbms
from distance import calculate_distances_from_aps
from location import get_position


def get_current_position(path_loss, known_aps):
    """
    the core function, returns the current location
    """
    print("***************************************************")
    ap1, ap2, ap3 = get_access_points(known_aps)
    if ap1 is None:
        return None, None, None, None

    ap1.dbm, ap2.dbm, ap3.dbm = get_dbms((ap1, ap2, ap3))
    ap1.distance, ap2.distance, ap3.distance = calculate_distances_from_aps((ap1, ap2, ap3), path_loss)

    print(
        "dbms measured: {0}: {1} , {2}: {3} , {4}: {5}".format(ap1.ssid, ap1.dbm, ap2.ssid, ap2.dbm,
                                                                           ap3.ssid,
                                                                           ap3.dbm))
    print(
        "distances measured: {0}: {1} , {2}: {3} , {4}: {5}".format(ap1.ssid, ap1.distance, ap2.ssid,
                                                                                 ap2.distance, ap3.ssid,
                                                                                 ap3.distance))

    x, y = get_position(ap1, ap2, ap3)

    if x is not None:
        print("the current location of the user is: " + str((x, y)))

    return (ap1.x, ap1.y), (ap2.x, ap2.y), (ap3.x, ap3.y), (x.real, y.real)
