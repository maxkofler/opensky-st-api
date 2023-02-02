
from webserver import webserver
from webserver import endpoints
from webserver import usermanager

if __name__ == "__main__":
    userm = usermanager.usermanager()
    webserver.web_server.register_get_endpoints(
            endpoints.branch_web_providers.get_get_providers())
    webserver.web_server.register_post_endpoints(
            endpoints.branch_web_providers.get_post_providers())
    webserver.start_web_server("localhost", 8080)	
