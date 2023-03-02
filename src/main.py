
from branchweb import webserver
import endpoints
from branchweb import webauth
import blog
import argparse

import threading
import asyncio
import websockets
import json
import dateutil.parser as dparser
import os

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

class Plane:
    def __init__(self, addr: int, tail: str):
        self.addr = addr
        self.tail = tail
        self.entries = []
        blog.info("New plane: addr: {}, tail: {}".format(self.addr, self.tail))

    def add_entry(self, entry: Entry):
        self.entries.append(entry)
        blog.debug("Plane {} ({}) updated: Alt: {} m, Speed: {} m/s, Lat: {}, Long: {}".format(self.addr, self.tail, entry.alt, entry.speed, entry.lat, entry.long))

        if (not os.path.exists("planes")):
            os.makedirs("planes")

        a = open("planes/{}.csv".format(self.tail), 'a')

        a.writelines(entry.get_info_csv() + "\n")
        a.close()

class FlightDataThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.planes = []

    def get_plane(self, addr: int):
        for plane in self.planes:
            if (plane.addr == addr):
                return plane
        return None

    async def handler(self, websocket: websockets.WebSocketClientProtocol) -> None:
        async for message in websocket:
            jsn = json.loads(message)
            entry = Entry(jsn)
            plane = self.get_plane(entry.addr)
            if (plane == None):
                self.planes.append(Plane(entry.addr, entry.tail))
            else:
                plane.add_entry(entry)

    async def consume(self, url: str) -> None:
        async with websockets.connect(url) as websocket:
            await self.handler(websocket)

    def run(self):
        self.loop.run_until_complete(self.consume("wss://ws.datapool.opendatahub.testingmachine.eu/flightdata/sbs-aggregated"))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--wildcard-cors", help="Lets the webserver send wildcard CORS headers for testing purposes", action="store_true")
    args = parser.parse_args()
    blog.enable_debug_level()

    # Setup the configuration and logger
    blog.info("Setting up webserver configuration..")
    webserver.WEB_CONFIG["logger_function_debug"] = blog.debug
    webserver.WEB_CONFIG["logger_function_info"] = blog.web_log
    webserver.WEB_CONFIG["web_debug"] = True
    webserver.WEB_CONFIG["send_cors_headers"] = args.wildcard_cors

    if (args.wildcard_cors):
        blog.warn("WARNING: You are sending wildcard CORS headers, this should not be used in production!")

    # Load the user file for the first time
    blog.info("Loading user file..")
    webauth.web_auth.setup_user_manager()

    # Set up the endpoints
    webserver.web_server.register_get_endpoints(
            endpoints.branch_web_providers.get_get_providers())
    webserver.web_server.register_post_endpoints(
            endpoints.branch_web_providers.get_post_providers())

    flightData = FlightDataThread()
    flightData.start()

    # Start the webserver
    webserver.start_web_server("localhost", 8080)	
