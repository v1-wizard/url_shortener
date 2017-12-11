FROM frolvlad/alpine-python3

MAINTAINER Aliaksei Boole <aliaksei.boole@gmail.com>

RUN pip install aiohttp && pip install cerberus && pip install tinydb

COPY ./app /app
COPY ./data /data
ENV PYTHONPATH=/

ENTRYPOINT ["python3", "/app/main.py"]
