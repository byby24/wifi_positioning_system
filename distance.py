from math import log10


def signal_strength_to_dbm(quality: int):
    return (quality / 2) - 100


def dbm_to_distance2(dbm: int, freq: float):
    return 10 ** ((27.55 - (20 * log10(freq)) + abs(dbm)) / 20.0)


def dbm_to_distance3(RSSI, A, n):
    aux = RSSI - A
    aux = (-1) * aux
    aux = float(aux) / (10 * n)
    x = 10 ** aux
    return x


def dbm_to_distance1(dbm: int, dbm_in_d0:int, d0:int, path_loss):
    return 10.0 ** ((dbm_in_d0 - dbm) / (10 * path_loss))


def calculate_distance(quality):
    return dbm_to_distance1(signal_strength_to_dbm(quality))


print(dbm_to_distance1(30, 50, 1, 3))