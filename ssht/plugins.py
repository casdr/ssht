import os
import logging
import json

import mysql.connector


class Host(object):

    def __init__(
            self,
            hostname,
            port=None,
            ipv4=None,
            ipv6=None,
            user=None):
        self.hostname = hostname
        self.port = port
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.user = user

    @staticmethod
    def factory(host):
        if type(host) == tuple:
            return Host(*host)
        if type(host) == dict:
            return Host(**host)

    @property
    def display(self):
        if self.user:
            return '{0}@{1}'.format(self.user, self.hostname)
        return self.hostname


class Parser(object):

    def __init__(self, path):
        '''

        :param path:
        '''
        self._path = path
        self._hosts = []

    def get_files(self, ext='.json'):
        return [x for x in os.listdir(self._path) if x.endswith(ext)]

    def search(self, name):
        return [x for x in self._hosts if name in x.hostname]


class JsonParser(Parser):   # pragma: nocover

    def __init__(self, *args, **kwargs):
        super(JsonParser, self).__init__(*args, **kwargs)
        self._files = self.get_files(ext='.json')
        self._load_data()

    def _load_data(self):
        '''
        Load parser specific data files
        '''
        for file_ in self._files:
            path = os.path.join(self._path, file_)
            logging.debug('Parsing "{0}"'.format(path))
            with open(path, 'r') as fh:
                try:
                    d = json.loads(fh.read())
                    logging.debug('Got: {0}'.format(d))
                    for host in d['hosts']:
                        self._hosts.append(Host.factory(host))
                except json.decoder.JSONDecodeError as ex:
                    logging.error(ex)


class MySQLParser(Parser):  # pragma: nocover

    def __init__(self, *args, **kwargs):
        super(MySQLParser, self).__init__(*args, **kwargs)
        self._files = self.get_files(ext='.mysql')
        self._load_data()

    def _load_data(self):
        '''
        Load parser specific data files
        '''
        for file_ in self._files:
            path = os.path.join(self._path, file_)
            logging.debug('Parsing "{0}"'.format(path))
            with open(path, 'r') as fh:
                d = json.loads(fh.read())
                logging.debug('Got: {0}'.format(d))
                conn = mysql.connector.connect(**d['config'])
                c = conn.cursor()
                c.execute(d['query'])

                for row in c:
                    self._hosts.append(Host.factory(row))