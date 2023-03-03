
import asyncio

from openskyapi import OpenSKYAPI

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    api = OpenSKYAPI()
    api.run()
