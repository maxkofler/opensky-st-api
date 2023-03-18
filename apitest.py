#!python3
import requests
import sys
import random, string

letters = string.ascii_letters
username = "".join(random.choice(letters) for i in range(15))
password = "".join(random.choice(letters) for i in range(15))
otherpass = "".join(random.choice(letters) for i in range(15))

if (len(sys.argv) != 2):
    print("Need the URL for the API!")
    exit(-1)

api_url = sys.argv[1] + "/"
last_resp = []
authkey = ""

def p(text):
    print(text, end="", flush=True)

def pn(text):
    print(text)

def req(endpoint, data):
    global api_url
    global last_resp
    last_resp = requests.post(api_url + endpoint, data=data).json()
    return last_resp

print("!!!")
print("")
print("MAKE SURE YOU DELETE THE SERVERS users.meta FILE BEFORE THIS!")
print("")
print("!!!")

p("Creating user...")
if (req("createuser", { "user": username, "pass": password})["response_code"] == 200):
    pn("OK")
else:
    pn("FAIL")

p("Logging in as user...")
if (req("auth", { "user": username, "pass": password})["response_code"] == 200):
    pn("OK")
    authkey = last_resp["payload"]
else:
    pn("FAIL")

p("Logging in as wrong user...")
if (req("auth", { "user": username + "garbage", "pass": password})["response_code"] == 200):
    pn("FAIL")
else:
    pn("OK")

p("Logging in with wrong password...")
if (req("auth", { "user": username, "pass": password + "garbage"})["response_code"] == 200):
    pn("FAIL")
else:
    pn("OK")

p("Checkauth...")
if (req("checkauth", { "authkey": authkey})["response_code"] == 200):
    pn("OK")
else:
    pn("FAIL")

p("Changing password...")
if (req("changepass", { "authkey": authkey, "pass": otherpass })["response_code"] == 200):
    pn("OK")
else:
    pn("FAIL")

p("Logoff...")
if (req("logoff", { "authkey": authkey})["response_code"] == 200):
    pn("OK")
else:
    pn("FAIL")

p("Checkauth after logoff...")
if (req("checkauth", { "authkey": authkey})["response_code"] == 200):
    pn("FAIL")
else:
    pn("OK")

p("Logging in with old password...")
if (req("auth", { "user": username, "pass": password })["response_code"] == 200):
    pn("FAIL")
else:
    pn("OK")

p("Logging in with new password...")
if (req("auth", { "user": username, "pass": otherpass })["response_code"] == 200):
    pn("OK")
    authkey = last_resp["payload"]
else:
    pn("FAIL")

p("Changing password back...")
if (req("changepass", { "authkey": authkey, "pass": otherpass })["response_code"] == 200):
    pn("OK")
else:
    pn("FAIL")

p("Logoff...")
if (req("logoff", { "authkey": authkey})["response_code"] == 200):
    pn("OK")
else:
    pn("FAIL")
