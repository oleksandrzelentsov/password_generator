#!/usr/bin/env python
import myModule
import random
import sys
import argparse
import sqlite3
from time import time

def get_args():
	parser = argparse.ArgumentParser(description='Generate some passwords and print generation statistics.')
	parser.add_argument('-c', '--count', nargs='?', type=int, help='count of passwords to generate', default=1)
	parser.add_argument('-min', '--min_size', nargs='?', type=int, help='minimum size of password', default=16)
	parser.add_argument('-max', '--max_size', nargs='?', type=int, help='maximum size of password', default=17)
	parser.add_argument('-v', '--verbose', help='print all unique passwords (statistics will be printed if no this option)', const=True, action="store_const", default=False)
	parser.add_argument('-s', '--statistics', help='do not print statistical data (passwords will be printed)', const=False, action="store_const", default=True)
	parser.add_argument('-d', '--database', help='do not fill statistical data in the database', const=False, action="store_const", default=True)
	args = parser.parse_args(sys.argv[1:])
	return args

def add_to_database(*args):
	database_filename = '.password_generation_effectiveness.db'
	conn = sqlite3.connect(database_filename)
	cur = conn.cursor()
	sql = """insert into generation_data
	(count, min_length, max_length, arguments_parsing_time,
	unary_generation_time, whole_generation_time, duplicates_count)
	values (?,?,?,?,?,?,?)"""
	cur.execute(sql, args)
	conn.commit()
	conn.close()

def Main():
	argparse_time = time()
	args = get_args()
	n = args.count
	size_min = args.min_size
	size_max = args.max_size
	verbose = args.verbose
	write_to_db = args.database
	show_statistics = args.statistics
	argparse_time = time() - argparse_time
	data = []
	one_iteration_time_array = []
	whole_generation_time = time()
	for i in range(n):
		one_iteration_time = time()
		data += [myModule.generate_password(random.randrange(size_min, size_max), i)]
		one_iteration_time_array.append(time() - one_iteration_time)

	u_data = set(data)
	whole_generation_time = round(time() - whole_generation_time, 2)
	unary_generation_time = (float(sum(one_iteration_time_array))/float(len(one_iteration_time_array)))
	dups = len(data) - len(u_data)
	dups_percent = round(float(dups)/float(len(data)) * 100, 2)
	if verbose or not show_statistics:
		print 'Passwords:\n{'
		for i in sorted(u_data, key=lambda x: len(x)):
			print '\t', i
		print '}'
	if show_statistics or not verbose:
		print 'arguments parsing time:\t\t\t%e' % argparse_time
		print 'unary generation time:\t\t\t%e' % unary_generation_time
		print 'whole generation time:\t\t\t%.2f' % whole_generation_time
		print 'duplicates count & %%:\t\t\t%i (%.2f%%)' % (dups, dups_percent)
	if write_to_db:
		add_to_database(n, size_min, size_max, argparse_time, unary_generation_time, whole_generation_time, dups)

if __name__ == "__main__":
	Main()
