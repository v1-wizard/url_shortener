FROM python:3-alpine3.6

LABEL maintainer="aliaksei.boole@gmail.com"

ARG APP_DIR=/var/app

COPY requirements.txt $APP_DIR/requirements.txt
RUN pip3 install -r $APP_DIR/requirements.txt --no-cache-dir

COPY src/ $APP_DIR/src/
COPY logging.conf $APP_DIR

ENV USH_PORT=7777
ENV USH_MONGO_CON_STRING=mongodb://localhost:27017/
ENV USH_LOGGER_CONF_PATH=$APP_DIR/logging.conf

WORKDIR $APP_DIR

ENTRYPOINT ["python3", "src/main.py"]