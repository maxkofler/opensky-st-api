# opensky-st-api
The API part of the OpenSky SouthTyrol project based on the [branch](https://github.com/AcaciaLinux/branch) webserver

# Obtaining the source code
To fetch the source code, you can use the following command:
```bash
git clone --recursive https://github.com/maxkofler/opensky-st-api
```

# Installation
To install this api on your system, run the following command as root:
```bash
make install
```

# Usage
Straightforward:
```bash
opensky-st-api
```

If you need to send wildcard CORS headers for testing purposes, you can use the following command:
```bash
opensky-st-api --wildcard-cors
```

# Documentation
To find the API documentation, open the [APIDOC.md](APIDOC.md) file.
