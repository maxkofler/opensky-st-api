# opensky-st-api
The API part of the OpenSky SouthTyrol project based on the [branch](https://github.com/AcaciaLinux/branch) webserver

# Usage
There is one dependency for the usermanager: `bcrypt`, you can install it using `pip3`:
```bash
pip3 install bcrypt
```

To use this API, you only need the `python3` interpreter. To just get started, use the following command:
```bash
python3 ./main.py
```

If you need to send wildcard CORS headers for testing purposes, you can use the following command:
```bash
python3 ./main.py --wildcard-cors
```

# Documentation
To find the API documentation, open the [APIDOC.md](APIDOC.md) file.
