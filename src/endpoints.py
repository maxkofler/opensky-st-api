import re
import blog

from branchweb import webserver
from branchweb import usermanager

class branch_web_providers():

    usermgr = usermanager.usermanager()

    @staticmethod
    def get_post_providers():
        post_providers = {
            "auth": branch_web_providers.auth_endpoint,
            "checkauth": branch_web_providers.check_auth_endpoint,
            "logoff": branch_web_providers.logoff_endpoint,
            "createuser": branch_web_providers.create_user_endpoint,
            "changepass": branch_web_providers.change_pass_endpoint,
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

        user = branch_web_providers.usermgr.get_user(post_data["user"])

        if (user is None):
            blog.debug("Failed to authenticate user '{}': Not registered".format(post_data["user"]))
            httphandler.send_web_response(webserver.webstatus.AUTH_FAILURE, "Authentication failed: user {} is not registered.".format(post_data["user"]))
            return

        authkey = user.authenticate(post_data["pass"])

        if (authkey is None):
            blog.debug("Authentication failure")
            httphandler.send_web_response(webserver.webstatus.AUTH_FAILURE, "Authentication failed.")
        else:
            blog.debug("Authentication succeeded for user {} with new autkey {}".format(user.name, authkey.key_id))
            httphandler.send_web_response(webserver.webstatus.SUCCESS, "{}".format(authkey.key_id))

    #
    # checks if the user is logged in or not
    #
    # ENDPOINT /checkauth (POST)
    @staticmethod
    def check_auth_endpoint(httphandler, form_data, post_data):
        if("authkey" not in post_data):
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for authentication.")    
            return

        authkey = post_data["authkey"]

        user = branch_web_providers.usermgr.get_key_owner(authkey)

        if (user is None):
            blog.debug("Authkey {} was tested for validity: FALSE".format(authkey))
            httphandler.send_web_response(webserver.webstatus.AUTH_FAILURE, "Authkey {} is invalid.".format(authkey))
        else:
            branch_web_providers.usermgr.update_user(user)
            blog.debug("Authkey {} was tested for validity: TRUE".format(authkey))
            httphandler.send_web_response(webserver.webstatus.SUCCESS, "Authkey {} is valid.".format(authkey))

    #
    # destroys the specified session and logs the user off
    #
    # ENDPOINT /logoff (POST)
    @staticmethod
    def logoff_endpoint(httphandler, form_data, post_data):
        if("authkey" not in post_data):
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for authentication.")
            return

        authkey = post_data["authkey"]

        user = branch_web_providers.usermgr.revoke_authkey(authkey)

        if (user is None):
            blog.debug("Tried to revoke invalid authkey {}".format(authkey))
            httphandler.send_web_response(webserver.webstatus.AUTH_FAILURE, "Invalid authentication key.")
        else:
            blog.debug("Authkey {} owned by {} was revoked".format(authkey, user.name))
            httphandler.send_web_response(webserver.webstatus.SUCCESS, "Logoff acknowledged.")
 
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

        if(not branch_web_providers.usermgr.add_user(nuser, npass)):
            httphandler.send_web_response(webserver.webstatus.SERV_FAILURE, "User already exists.")
            return

        httphandler.send_web_response(webserver.webstatus.SUCCESS, "User created")

    @staticmethod
    def change_pass_endpoint(httphandler, form_data, post_data):

        if("authkey" not in post_data):
            blog.debug("Missing request data for user creation: Authentication key (authkey)")
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for user creation: Authentication key (authkey)")
            return

        if("pass" not in post_data):
            blog.debug("Missing request data for user creation: Password (pass)")
            httphandler.send_web_response(webserver.webstatus.MISSING_DATA, "Missing request data for user creation: Password (pass)")
            return

        authkey = post_data["authkey"]
        newpass = post_data["pass"]

        usr = branch_web_providers.usermgr.get_key_owner(authkey)

        if (usr is None):
            blog.debug("Tried to change password of not authorized key {}".format(authkey))
            httphandler.send_web_response(webserver.webstatus.SERV_FAILURE, "Authkey is not valid for any user")
            return

        blog.debug("Changing password of user {}".format(usr.name))

        # Set the password and force an update on the userfile
        usr.set_password(newpass)
        branch_web_providers.usermgr.write_file()

        httphandler.send_web_response(webserver.webstatus.SUCCESS, "Password changed")

    #
    # / endpoint, returns html page
    #
    # ENDPOINT: / (GET)
    @staticmethod
    def root_endpoint(httphandler, form_data):
        httphandler.send_str_raw(200, "<h1>Bad request.</h1>")

