# -*- coding: utf-8 -*-

SHORTCUT = {
    'link': {
        'type': 'string',
        'regex': ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                  '(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
        'empty': False,
        'required': True,
    },
}

GET_STATS = {
    'id': {
        'type': 'string',
        'empty': False,
        'required': True
    }
}

PURGE_ALL = {
    'confirm': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed': ['yes', 'Yes', 'YES']
    },
}

WEB_SOCKET_MSG = {
    'command': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed': ['shortcut', 'get_stats', 'purge_all', 'get_all_links'],
    },
    'body': {
        'type': 'dict',
        'required': True,
    },
}
