#!/usr/bin/env python
import myModule
import random
import sys
import argparse
import sqlite3
import subprocess
from hashlib import md5
from time import time


def get_py_hash():
    r = ''
    with open(__file__, 'r') as f:
        for i in f:
            r += i
    return md5(r).hexdigest()


def get_c_hash():
    r = ''
    with open(myModule.__file__, 'r') as f:
        for i in f:
            r += i
    return md5(r).hexdigest()


def get_latest_git_commit_message():
    commit_message_path = ('' if 'win' in sys.platform else '/tmp/') + 'latest_commit_message.tmp'
    msg = ''
    p = None
    with open(commit_message_path, 'w') as f:
        p = subprocess.call('git log -1 --pretty=%B'.split(), stdout=f, stderr=f)
    if p:
        return ''
    with open(commit_message_path, 'r') as f:
        t = ''
        for i in f:
            t += i
        msg = t.strip()
    subprocess.call(['rm', commit_message_path])
    return msg


def get_args():
    parser = argparse.ArgumentParser(description='Generate some passwords and print generation statistics.')
    parser.add_argument('-c', '--count', nargs='?', type=int, help='count of passwords to generate', default=1)
    parser.add_argument('-min', '--min_size', nargs='?', type=int, help='minimum size of password', default=16)
    parser.add_argument('-max', '--max_size', nargs='?', type=int, help='maximum size of password', default=0)
    parser.add_argument('-s', '--silent', help='do not print all unique passwords', const=True, action="store_const",
                        default=False)
    parser.add_argument('-d', '--statistical-data', help='print statistical data', const=True, action="store_const",
                        default=False)
    parser.add_argument('-D', '--database', help='log statistical data in the database', const=True,
                        action="store_const", default=False)
    args = parser.parse_args(sys.argv[1:])
    return args


def create_db(cur):
    sql = ''
    with open('schema.sql', 'r') as f:
        sql += ''.join(f.readlines())
    cur.executescript(sql)
    cur.connection.commit()


def add_to_database(*args):
    database_filename = '.password_generation_effectiveness.db'
    conn = sqlite3.connect(database_filename)
    cur = conn.cursor()
    create_db(cur)
    sql = """insert into generation_data
(count, min_length, max_length, arguments_parsing_time,
unary_generation_time, whole_generation_time,
duplicates_count, c_files_hash, py_files_hash, git_commit_message)
values (?,?,?,?,?,?,?,?,?,?)"""
    cur.execute(sql, tuple(list(args) + [get_c_hash(), get_py_hash(), get_latest_git_commit_message()]))
    conn.commit()
    conn.close()


def main_function():
    argparse_time = time()
    args = get_args()
    n = args.count
    size_min = args.min_size
    size_max = args.max_size if size_min < args.max_size else size_min
    silent = args.silent
    write_to_db = args.database
    show_statistics = args.statistical_data
    argparse_time = time() - argparse_time
    data = []
    one_iteration_time_array = []
    whole_generation_time = time()
    for i in range(n):
        one_iteration_time = time()
        data.append(myModule.generate_password(random.randrange(size_min, size_max + 1), i))
        one_iteration_time_array.append(time() - one_iteration_time)

    u_data = set(data)
    whole_generation_time = round(time() - whole_generation_time, 2)
    unary_generation_time = (float(sum(one_iteration_time_array)) / float(len(one_iteration_time_array)))
    duplicates_count = len(data) - len(u_data)
    duplicates_percent = round(float(duplicates_count) / float(len(data)) * 100, 2)
    if not silent:
        if n > 1:
            print 'Passwords:\n{'
        for i in sorted(u_data, key=lambda x: len(x)):
            print '\t', i
        if n > 1:
            print '}'
    if show_statistics:
        print 'arguments parsing time:\t\t\t%es' % argparse_time
        print 'unary generation time:\t\t\t%es' % unary_generation_time
        print 'whole generation time:\t\t\t%.2fs' % whole_generation_time
        print 'duplicates count & %%:\t\t\t%i (%.2f%%)' % (duplicates_count, duplicates_percent)
    if write_to_db:
        add_to_database(n, size_min, size_max, argparse_time, unary_generation_time, whole_generation_time,
                        duplicates_count)


if __name__ == "__main__":
    main_function()