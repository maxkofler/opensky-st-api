
import blog
import threading
import asyncio
import websockets
import json
from plane import Plane
from planeentry import Entry

class FlightDataThread(threading.Thread):

    websocket: websockets.WebSocketClientProtocol

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
            entry = Entry.from_json(jsn)
            plane = self.get_plane(entry.addr)
            if (plane == None):
                blog.info("New plane: addr: {}, tail: {}".format(entry.addr, entry.tail))
                self.planes.append(Plane(entry.addr, entry.tail))
            else:
                plane.add_entry(entry)

    async def consume(self, url: str) -> None:
        async with websockets.connect(url) as websocket:
            self.websocket = websocket
            await self.handler(websocket)

    def run(self):
        asyncio.run(self.consume("wss://ws.datapool.opendatahub.testingmachine.eu/flightdata/sbs-aggregated"))

    async def stop(self):
        await self.websocket.close()
