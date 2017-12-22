# -*- coding: utf-8 -*-

import os

USH_PORT = int(os.environ.get('USH_PORT', 7777))
USH_DB_PATH = os.environ.get('USH_DB_PATH', '../data/links.json')
