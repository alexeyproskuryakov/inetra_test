__author__ = '4ikist'

from pikachu_test.properties import etalon_files_destination


def get_files():
    """
    simple parsing meta file in etalon path and returning
    """
    result = {}
    meta = open(etalon_files_destination + '\\meta').read().strip().split('\n')
    for el in meta:
        ext = el[-3:]
        row = el.split()
        tth = row[0]
        size = int(row[1])
        name = row[2]
        result[ext] = {'tth': tth, 'size': size, 'name': name}
    return result
