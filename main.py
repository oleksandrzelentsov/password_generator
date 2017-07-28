#!/usr/bin/env python
from argparse import ArgumentParser
from hashlib import md5
from random import randrange
from sys import platform, argv
from subprocess import call
from time import time

import pasgens


class Statistics:
    def __init__(self):
        self._data = dict()

    def __getitem__(self, item):
        if item in list(self._data.keys()):
            return self._data[item]['format_string'] % self._data[item]['value']
        else:
            raise KeyError('there is no statistics item with such key')

    def add(self, name, format_string, value):
        self._data[name] = {'format_string': format_string, 'value': value}

    def iteritems(self):
        return sorted([(k, self._data[k]) for k in list(self._data.keys())], key=lambda x: x[0])

    def get(self, item):
        if item in list(self._data.keys()):
            return self._data[item]['format_string'] % self._data[item]['value']
        else:
            return None


def generate_password(statistics_obj, passwords_count=1, do_not_print_passwords=False, minimum_size=16, maximum_size=16,
                      verbose=False):
    data = []
    one_iteration_time_array = []
    whole_generation_time = time()
    for rand_seed in range(passwords_count):
        one_iteration_time = time()
        data.append(pasgens.generate_password(randrange(minimum_size, maximum_size + 1), rand_seed))
        one_iteration_time_array.append(time() - one_iteration_time)

    u_data = set(data)
    whole_generation_time = round(time() - whole_generation_time, 2)
    unary_generation_time = (float(sum(one_iteration_time_array)) / float(len(one_iteration_time_array)))
    duplicates_count = len(data) - len(u_data)
    duplicates_percent = round(float(duplicates_count) / float(len(data)) * 100, 2)
    statistics_obj.add('unary_generation_time', 'unary generation time:\t\t\t%es', unary_generation_time)
    statistics_obj.add('whole_generation_time', 'whole generation time:\t\t\t%.2fs', whole_generation_time)
    statistics_obj.add('duplicates', 'duplicates count & %%:\t\t\t%i (%.2f%%)', (duplicates_count, duplicates_percent))
    if not do_not_print_passwords:
        for rand_seed in sorted(u_data, key=lambda x: len(x)):
            print(rand_seed)

    if verbose:
        for k, v in statistics_obj.items():
            print(statistics_obj.get(k))


def get_hash_of_file(filename):
    r = ''
    with open(filename, 'r') as f:
        for i in f:
            r += i
    return md5(r).hexdigest()


def get_py_hash():
    return get_hash_of_file(__file__)


def get_c_hash():
    return get_hash_of_file(pasgens.__file__)


def get_latest_git_commit_message():
    commit_message_path = ('' if 'win' in platform else '/tmp/') + 'latest_commit_message.tmp'
    msg = ''
    with open(commit_message_path, 'w') as f:
        p = call('git log -1 --pretty=%B'.split(), stdout=f, stderr=f)
    if p:
        return ''
    with open(commit_message_path, 'r') as f:
        t = ''
        for i in f:
            t += i
        msg += t.strip()
    call(['rm', commit_message_path])
    return msg


def get_args():
    parser = ArgumentParser(description='Generate some passwords and print generation statistics.')
    parser.add_argument('-c', '--count', nargs='?', type=int, help='count of passwords to generate', default=1)
    parser.add_argument('-min', '--min_size', nargs='?', type=int, help='minimum size of password', default=16)
    parser.add_argument('-max', '--max_size', nargs='?', type=int, help='maximum size of password', default=0)
    parser.add_argument('-s', '--silent', help='do not print all unique passwords', const=True, action="store_const",
                        default=False)
    parser.add_argument('-d', '--statistical-data', help='print statistical data', const=True, action="store_const",
                        default=False)
    parser.add_argument('-D', '--database', help='log statistical data in the database', const=True,
                        action="store_const", default=False)
    parsed_arguments_namespace = parser.parse_args(argv[1:])
    return parsed_arguments_namespace


def create_db(cur):
    sql = ''
    with open('schema.sql', 'r') as f:
        sql += ''.join(f.readlines())
    cur.executescript(sql)
    cur.connection.commit()


if __name__ == "__main__":
    statistics = Statistics()
    argument_parsing_time = time()
    args = get_args()
    n = args.count
    size_min = args.min_size
    size_max = args.max_size if size_min < args.max_size else size_min
    silent = args.silent
    write_to_db = args.database
    show_statistics = args.statistical_data
    argument_parsing_time = time() - argument_parsing_time
    statistics.add('argparse_time', 'arguments parsing time:\t\t\t%es', argument_parsing_time)
    generate_password(statistics, n, silent, size_min, size_max, show_statistics)
