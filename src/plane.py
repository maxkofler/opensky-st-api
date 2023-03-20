
import blog
import os
import csv
from planeentry import Entry

class Plane:
    def __init__(self, addr: int, tail: str):
        self.addr = addr
        self.tail = tail
        self.entries = []

    def add_entry(self, entry: Entry):
        blog.debug("Plane {} ({}) updated: Alt: {} m, Speed: {} m/s, Lat: {}, Long: {}".format(self.addr, self.tail, entry.alt, entry.speed, entry.lat, entry.long))

        if (not os.path.exists("planes")):
            os.makedirs("planes")

        a = open("planes/{}.csv".format(self.tail), 'a')

        a.writelines(entry.get_info_csv() + "\n")
        a.close()

    def load_from_file(addr: int, tail: str) -> super:
        path = os.path.join("planes", "{}.csv".format(tail))

        if (not os.path.exists(path)):
            return None

        plane = Plane(addr, tail)

        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                plane.entries.append(Entry.from_array(row))

        return plane

    def get_entries(self) -> list[Entry]:
        return self.entries
