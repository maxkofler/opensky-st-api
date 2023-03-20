import blog
import dateutil.parser as dparser
import dateutil

class Entry:
    def __init__(self):
        self.addr: int
        self.tail: str
        self.alt: int
        self.speed: int
        self.track: int
        self.lat: float
        self.long: float
        self.vvel: float
        self.e_category: int
        self.timestamp: dateutil.datetime

    def from_json(json) -> super:
        obj = Entry()

        obj.addr = int(json["Icao_addr"])
        obj.tail = str(json["Tail"]).strip()
        obj.alt = round(int(json["Alt"]) * 0.305, 0)
        obj.speed = round((int(json["Speed"]) * 1.852) / 3.6, 0)
        obj.track = int(json["Track"])
        obj.lat = float(json["Lat"])
        obj.long = float(json["Lng"])
        obj.vvel = float(json["Vvel"])
        obj.e_category = int(json["Emitter_category"])
        obj.timestamp = dparser.parse(json["Timestamp"], fuzzy=True)

        return obj

    def from_array(arr) -> super:
        obj = Entry()

        obj.alt = int(float(arr[0]))
        obj.speed = int(float(arr[1]))
        obj.track = int(float(arr[2]))
        obj.lat = float(arr[3])
        obj.long = float(arr[4])
        obj.vvel = float(arr[5])
        obj.timestamp = dparser.parse(arr[6], fuzzy=True)

        return obj

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
            "timestamp": self.timestamp.timestamp()
        }

    def get_info_csv(self):
        return "{};{};{};{};{};{};{}".format(self.alt, self.speed, self.track, self.lat, self.long, self.vvel, self.timestamp)
