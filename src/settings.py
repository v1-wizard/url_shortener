import os

USH_PORT = int(os.environ.get('USH_PORT', 8888))
USH_MONGO_CON_STRING = os.environ.get(
    'USH_MONGO_CON_STRING', 'mongodb://localhost:27017/'
)
USH_LOGGER_CONF_PATH = os.environ.get(
    'USH_LOGGER_CONF_PATH', '../logging.conf'
)
