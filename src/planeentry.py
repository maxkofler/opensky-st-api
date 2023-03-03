import blog
import dateutil.parser as dparser

class Entry:
    def __init__(self, json):
        self.addr = int(json["Icao_addr"])
        self.tail = str(json["Tail"]).strip()
        self.alt = round(int(json["Alt"]) * 0.305, 0)
        self.speed = round((int(json["Speed"]) * 1.852) / 3.6, 0)
        self.track = int(json["Track"])
        self.lat = float(json["Lat"])
        self.long = float(json["Lng"])
        self.vvel = float(json["Vvel"])
        self.e_category = int(json["Emitter_category"])
        self.timestamp = dparser.parse(json["Timestamp"], fuzzy=True)

    def print(self):
        blog.debug("Addr: {}, Tail: {}, Alt: {} km, Speed: {} km/h, Lat: {}, Long: {}, Vvel: {}, Track: {}".format(self.addr, self.tail, self.alt, self.speed, self.lat, self.long, self.vvel, self.track))

    def get_info_dict(self):
        return {
            "alt": self.alt,
            "speed": self.speed,
            "track": self.track,
            "lat": self.lat,
            "long": self.long,
            "vvel": self.vvel,
            "timestamp": str(self.timestamp)
        }

    def get_info_csv(self):
        return "{};{};{};{};{};{};{}".format(self.alt, self.speed, self.track, self.lat, self.long, self.vvel, self.timestamp)
