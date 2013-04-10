__author__ = '4ikist'

import requests
import unittest2
import hashlib
import random

from pikachu_test.contrib import loggers
from pikachu_test import properties
from pikachu_test.contrib import environment_manager
from pikachu_test.contrib import etalon_files


logger = loggers.logger


def _send_request(url, token, tth, name, size):
    params = {'auth_token': token,
              'xt': 'urn:tree:tiger:%s' % tth,
              'dn': name,
              'xl': size}

    logger.info('send request to %s with params %s' % (url, params))
    response = requests.get(url, params=params, timeout=properties.default_timeout)
    return response


class TestPickachuPlay(unittest2.TestCase):
    def setUp(self):
        self.connection_mode = 'active'
        pid, self.port, access_token = environment_manager.set_connection_mode(self.connection_mode)
        self.assertNotEqual(self.port, 'INVALID')
        logger.info('pikachu (%s) work in port: %s, access token is: %s' % (pid, self.port, access_token))
        self.access_token = access_token
        self.play_url = 'http://localhost:%s/play' % self.port
        self.status_url = 'http://localhost:%s/status' % self.port
        self.etalon_files = etalon_files.get_files()


class TestPikachuPlayMethodActive(TestPickachuPlay):
    def setUp(self):
        super(TestPikachuPlayMethodActive, self).setUp()
        self.connection_mode = 'active'

    def testGetPartFile(self):
        logger.info(
            '\n------------------------------------------\nTest get part file\n mode = %s' % self.connection_mode)
        for el in self.etalon_files:
            file_params = self.etalon_files[el]
            size = random.randint(0, file_params['size'] - (file_params['size'] % 2))
            etalon_file_content = open(
                '%s\\%s' % (properties.etalon_files_destination, file_params['name']), 'rb').read(size)

            response = _send_request(self.play_url,
                                     self.access_token,
                                     file_params['tth'],
                                     file_params['name'],
                                     size)

            self.assertEqual(response.status_code, 206,
                             msg='status code must be 206, but here is %s' % response.status_code)

            for el in range(size):
                resp_el = response.content[el]
                etalon_el = etalon_file_content[el]
                self.assertEqual(resp_el, etalon_el, msg='response el and etalon must be equals')

    def testGetZeroFile(self):
        logger.info(
            '\n------------------------------------------\nTest get zero file\n mode = %s' % self.connection_mode)
        for el in self.etalon_files:
            file_params = self.etalon_files[el]
            response = _send_request(self.play_url,
                                     self.access_token,
                                     file_params['tth'],
                                     file_params['name'],
                                     0)

            self.assertEqual(response.status_code, 206,
                             msg='status code must be 206, but here is %s' % response.status_code)

            response_file_content = response.content
            etalon_file_content = open(
                '%s\\%s' % (properties.etalon_files_destination, file_params['name']), 'rb').read(0)

            response_hash = hashlib.md5(response_file_content)
            etalon_hash = hashlib.md5(etalon_file_content)

            self.assertEqual(etalon_hash.digest(), response_hash.digest(), msg='hashes of contents must be equals')

    def tearDown(self):
        exit_url = 'http://localhost:%s/exit' % self.port
        params = {'auth_token': self.access_token}
        requests.get(exit_url, params=params)


class TestPikachuPlayMethodPassive(TestPikachuPlayMethodActive):
    def setUp(self):
        super(TestPikachuPlayMethodPassive, self).setUp()
        self.connection_mode = 'passive'


class TestPikachuPlayMethodBad(TestPickachuPlay):
    def setUp(self):
        super(TestPikachuPlayMethodBad, self).setUp()

    def testBadParams(self):
        logger.info('\n------------------------------------------\nTest with bad params')
        response = _send_request(self.play_url, self.access_token, 'some bad tth', 'some another name', 100500)
        self.assertEqual(response.status_code, 400, msg='status code must be 400')

    def testBadParamXt(self):
        logger.info('\n------------------------------------------\nTest with bad param xt')
        response = _send_request(self.play_url, self.access_token, 'some bad tth', '', 100500)
        self.assertEqual(response.status_code, 400, msg='status code must be 400')

    def testBadParamXl(self):
        logger.info('\n------------------------------------------\nTest with bad param xl')
        response = _send_request(self.play_url, self.access_token, 'some bad tth', 'some another name', -100500)
        self.assertEqual(response.status_code, 400, msg='status code must be 400')

    def testBadParamAccessToken(self):
        logger.info('\n------------------------------------------\nTest with bad param access_token')
        response = _send_request(self.play_url, 'none', 'some bad tth', 'some another name', 100500)
        self.assertEqual(response.status_code, 403, msg='status code must be 400')

