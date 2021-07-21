def dbm_to_distance1(dbm: int, dbm_in_d0: int, path_loss):
    """
    :return: distance from a point, using dbm to distance formula
    """
    return 10.0 ** ((dbm_in_d0 - dbm) / (10 * path_loss))
    # return abs((27.55 - (20 * log10(2.4)) - dbm) / 20)


def calculate_distances_from_aps(aps_list, _path_loss):
    """
    :return: list of distances from 3 aps objects from, using the dbm to distance formula
    """
    return [dbm_to_distance1(ap.dbm, ap.dbm_in_d0, _path_loss) for ap in aps_list]
