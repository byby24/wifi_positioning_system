from access_points import get_scanner

x = get_scanner("wlan0")
print(x.get_access_points())
