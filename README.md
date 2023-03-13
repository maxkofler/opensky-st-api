# opensky-st-api
The API part of the OpenSky SouthTyrol project based on the [branch](https://github.com/AcaciaLinux/branch) webserver

# Obtaining the source code
To fetch the source code, you can use the following command:
```bash
git clone --recursive https://github.com/maxkofler/opensky-st-api
```

# Building
It is recommended to build the docker container using the following command:
```bash
docker build . -t opensky-st-api
```

# Usage
After building the container image, it can be used for testing purposes with docker run:
```bash
docker run -it -p "8080:8080" opensky-st-api
```

# Documentation
To find the API documentation, open the [APIDOC.md](APIDOC.md) file.
