
import blog
import os
from planeentry import Entry

class Plane:
    def __init__(self, addr: int, tail: str):
        self.addr = addr
        self.tail = tail
        self.entries = []
        blog.debug("New plane: addr: {}, tail: {}".format(self.addr, self.tail))

    def add_entry(self, entry: Entry):
        self.entries.append(entry)
        blog.debug("Plane {} ({}) updated: Alt: {} m, Speed: {} m/s, Lat: {}, Long: {}".format(self.addr, self.tail, entry.alt, entry.speed, entry.lat, entry.long))

        if (not os.path.exists("planes")):
            os.makedirs("planes")

        a = open("planes/{}.csv".format(self.tail), 'a')

        a.writelines(entry.get_info_csv() + "\n")
        a.close()
