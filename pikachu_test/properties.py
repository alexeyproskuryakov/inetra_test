__author__ = '4ikist'

import os

default_timeout = 2000

config_path = os.environ['APPDATA'] + '\\pikachu'

pikachu_process_name = 'pikachu.exe'

pid_file_destination = config_path + '\\pikachu.pid'
port_file_destination = config_path + '\\pikachu_port'
access_token_file_destination = config_path + '\\auth_token'

pikachu_exec_file_destination = os.environ['LOCALAPPDATA'] + '\\peers3\\pikachu.exe'

etalon_files_destination = os.path.dirname(os.path.dirname(__file__)) + '\\etalon'
download_files_destination = 'd:\\!downloads\\dc++'

# properties for another host server (for available or not etalon files in supplier)
# supplier_server_host = 'localhost' #'192.168.1.119'
# supplier_server_port = 44444
#
# supplier_old_peers_exec_file_destination = "C:\Program Files (x86)\Peers\Peers.exe"
# supplier_old_peers_process_name = 'Peers.exe'


