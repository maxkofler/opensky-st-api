
from webserver import webserver
from webserver import endpoints
from webserver import usermanager
import blog

if __name__ == "__main__":

    # Setup the configuration and logger
    blog.info("Setting up webserver configuration..")
    webserver.WEB_CONFIG["logger_function_debug"] = blog.debug
    webserver.WEB_CONFIG["logger_function_info"] = blog.web_log
    webserver.WEB_CONFIG["web_debug"] = True

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
