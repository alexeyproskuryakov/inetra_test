__author__ = '4ikist'

__doc__ = """
some functions for managing files and os processions
"""

import os
import time
import errno
import xml.etree.ElementTree as et

from pikachu_test.properties import *
from pikachu_test.contrib import loggers

logger = loggers.logger


def _silent_remove(filename):
    try:
        if os.path.exists(filename):
            logger.debug('remove file %s' % filename)
            os.remove(filename)
    except OSError, e:
        if e.errno != errno.ENOENT:
            raise Exception('can not delete file %s' % filename)


def _get_parameters():
    """
    waiting while pid, port and access file will exists and return their content
    it is bad code... in future i must use watchdog or another file event framework
    """
    counter = 0
    while True:
        if os.path.exists(port_file_destination) and os.path.exists(access_token_file_destination) and os.path.exists(
                pid_file_destination):
            break
        else:
            counter += 1
            time.sleep(5)
            if counter > 100:
                raise Exception('can not exists one or all files in pid, port access_token')
    return open(pid_file_destination).read(), open(port_file_destination).read(), open(
        access_token_file_destination).read()


def set_connection_mode(mode):
    logger.info('set connection mode %s' % mode)
    etree = et.parse(config_path + '\\conf.xml')
    conn_mode_element = etree.find('.//ConnectionMode')
    conn_mode_element.text = mode
    etree.write(config_path + '\\conf.xml')

    force_stop_pikachu(all=True)
    return start_pikachu()


def clean_downloads_directory():
    for el in os.listdir(download_files_destination):
        _silent_remove(download_files_destination + '\\' + el)


def is_file_in_downloads_directory(file_name):
    return os.path.exists(download_files_destination + file_name)


def start_pikachu():
    logger.info('starting pikachu')
    os.startfile(pikachu_exec_file_destination)
    return _get_parameters()


def force_stop_pikachu(pid=None, all=False):
    logger.info('stopping force pikachu')
    if not all:
        if pid:
            os.system('taskkill /F /FI "PID eq %s"' % pid)
    else:
        #force killing all process with name pikachu.exe
        os.system('taskkill /F /IM %s' % pikachu_process_name)

    clean_pikachu_environment()


def clean_pikachu_environment():
    logger.info('clean pikachu environment')

    _silent_remove(pid_file_destination)
    _silent_remove(port_file_destination)
    _silent_remove(access_token_file_destination)

    _silent_remove(config_path + '\\share.xml')
    _silent_remove(config_path + '\\pikachu-dc.log')
    _silent_remove(config_path + '\\pikachu-http.log')
    _silent_remove(config_path + '\\pikachu-share.log')
    _silent_remove(config_path + '\\pikachu.log')
    _silent_remove(config_path + '\\incomplete\\downloads.xml')

    clean_downloads_directory()


def supplier_start_old_peers():
    os.startfile(supplier_old_peers_exec_file_destination)


def supplier_stop_old_peers():
    os.system('taskkill /F /IM %s' % supplier_old_peers_process_name)
