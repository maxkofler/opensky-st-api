import re
import blog

from webserver import webauth
from webserver import webserver
from webserver import usermanager

class branch_web_providers():
    
    @staticmethod
    def get_post_providers():
        post_providers = {
            "auth": branch_web_providers.auth_endpoint,
            "checkauth": branch_web_providers.check_auth_endpoint,
            "logoff": branch_web_providers.logoff_endpoint,
            "createuser": branch_web_providers.create_user_endpoint,
        }
        return post_providers
    
    @staticmethod
    def get_get_providers():
        get_providers = {
            "": branch_web_providers.root_endpoint
        }
        return get_providers

    #
    # endpoint used to authenticate a user
    #
    # ENDPOINT /auth (POST)
    @staticmethod
    def auth_endpoint(httphandler, form_data, post_data):
        # invalid request
        if("user" not in post_data or "pass" not in post_data):
            blog.debug("Missing request data for authentication")
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for authentication")
            return
        
        if(webauth.web_auth().validate_pw(post_data["user"], post_data["pass"])):
            blog.debug("Authentication succeeded.")
            key = webauth.web_auth().new_authorized_key()
            
            httphandler.send_web_response(webserver.webstatus.SUCCESS, "{}".format(key.key_id))
        
        else:
            blog.debug("Authentication failure")
            httphandler.send_web_response(webserver.webstatus.AUTH_FAILURE, "Authentication failed.")

    #
    # checks if the user is logged in or not
    #
    # ENDPOINT /checkauth (POST)
    @staticmethod
    def check_auth_endpoint(httphandler, form_data, post_data):
        if("authkey" not in post_data):
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for authentication.")    
            return
        
        if(webauth.web_auth().validate_key(post_data["authkey"])):
            httphandler.send_web_response(webserver.webstatus.SUCCESS, "Authentication succeeded.")
            
        else:
            httphandler.send_web_response(webserver.webstatus.AUTH_FAILURE, "Authentication failed.")
            
    #
    # destroys the specified session and logs the user off
    #
    # ENDPOINT /logoff (POST)
    @staticmethod
    def logoff_endpoint(httphandler, form_data, post_data):
        if("authkey" not in post_data):
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for authentication.")
            return

        # check if logged in       
        if(webauth.web_auth().validate_key(post_data["authkey"])):
            webauth.web_auth().invalidate_key(post_data["authkey"])
            httphandler.send_web_response(webserver.webstatus.SUCCESS, "Logoff acknowledged.")
            
        else:
            httphandler.send_web_response(webserver.webstatus.AUTH_FAILURE, "Invalid authentication key.")
            
 
    #
    # creates a webuser
    #
    # ENDPOINT /createuser (POST)
    @staticmethod
    def create_user_endpoint(httphandler, form_data, post_data):

        if("user" not in post_data):
            blog.debug("Missing request data for user creation: Username (user)")
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for user creation: User (user)")
            return

        if("pass" not in post_data):
            blog.debug("Missing request data for user creation: Password (pass)")
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for user creation: Password (pass)")
            return

        nuser = post_data["user"]
        npass = post_data["pass"]
        
        if(bool(re.match('^[a-zA-Z0-9]*$', nuser)) == False):
            blog.debug("Invalid username for account creation")
            httphandler.send_web_response(webserver.webstatus.SERV_FAILURE, "Invalid username for account creation")
            return
        
        if(not usermanager.usermanager().add_user(nuser, npass)):
            httphandler.send_web_response(webserver.webstatus.SERV_FAILURE, "User already exists.")
            return

        httphandler.send_web_response(webserver.webstatus.SUCCESS, "User created")

    #
    # / endpoint, returns html page
    #
    # ENDPOINT: / (GET)
    @staticmethod
    def root_endpoint(httphandler, form_data):
        httphandler.send_str_raw(200, "<h1>Bad request.</h1>")

