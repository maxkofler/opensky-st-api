
from branchweb import webserver
import endpoints
from branchweb import usermanager
import blog
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--wildcard-cors", help="Lets the webserver send wildcard CORS headers for testing purposes", action="store_true")
    args = parser.parse_args()

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
    userm = usermanager.usermanager()

    # Set up the endpoints
    webserver.web_server.register_get_endpoints(
            endpoints.branch_web_providers.get_get_providers())
    webserver.web_server.register_post_endpoints(
            endpoints.branch_web_providers.get_post_providers())

    # Start the webserver
    webserver.start_web_server("localhost", 8080)	
