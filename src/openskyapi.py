
from branchweb import webserver
import endpoints
import blog
import asyncio
from flightdata import FlightDataThread
import argparse
from signal import signal,SIGINT

class OpenSKYAPI:

    flightData: FlightDataThread

    def sigintHandler(self, signal_received, frame):
        blog.warn("Shutting down gracefully...")
        asyncio.get_event_loop().run_until_complete(self.flightData.stop())
        #webserver.web_server.
        #webserver.web_server.server_close()

    def run(self):

        parser = argparse.ArgumentParser()
        parser.add_argument("--wildcard-cors", help="Lets the webserver send wildcard CORS headers for testing purposes", action="store_true")
        args = parser.parse_args()
        blog.enable_debug_level()

        # Setup the configuration and logger
        blog.info("Setting up webserver configuration..")
        webserver.WEB_CONFIG["logger_function_debug"] = blog.debug
        webserver.WEB_CONFIG["logger_function_info"] = blog.info
        webserver.WEB_CONFIG["web_debug"] = True
        webserver.WEB_CONFIG["send_cors_headers"] = args.wildcard_cors

        if (args.wildcard_cors):
            blog.warn("WARNING: You are sending wildcard CORS headers, this should not be used in production!")

        # Set up the endpoints
        webserver.web_server.register_get_endpoints(
                endpoints.branch_web_providers.get_get_providers())
        webserver.web_server.register_post_endpoints(
                endpoints.branch_web_providers.get_post_providers())

        signal(SIGINT, self.sigintHandler)

        self.flightData = FlightDataThread()
        self.flightData.start()

        # Start the webserver
        webserver.start_web_server("0.0.0.0", 8080)
