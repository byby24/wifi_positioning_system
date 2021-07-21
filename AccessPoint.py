class AccessPoint:
    def __init__(self, *argv):

        if type(argv[0]) is dict:
            self.x = argv[0]["x"]
            self.y = argv[0]["y"]
            self.ssid = argv[0]["ssid"]
            self.dbm_in_d0 = argv[0]["dbm_in_d0"]
            self.d0 = argv[0]["d0"]
            self.dbm = None
            self.distance = None

        else:
            self.x = argv[0]
            self.y = argv[1]
            self.ssid = argv[2]
            self.dbm_in_d0 = argv[3]
            self.d0 = argv[4]
            self.distance = argv[5]
            self.dbm = None

    def __str__(self):
        return "x: {0}, y: {1}, dbm: {2}, distance: {3}, ssid: {4}, dbm in d0 {5}, d0 {6}". \
            format(self.x, self.y, self.dbm, self.distance, self.ssid, self.dbm_in_d0, self.dbm)