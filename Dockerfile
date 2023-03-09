FROM alpine
RUN apk update && apk add python3 py3-pip make
RUN pip install setuptools requests websockets dateutils && pip install bcrypt
COPY branchweb /branchweb/
RUN cd /branchweb/ && python3 setup.py sdist && pip install dist/branchweb-1.0.tar.gz
RUN mkdir /opensky
COPY . /opensky/
CMD /opensky/entry.sh
EXPOSE 8080/tcp