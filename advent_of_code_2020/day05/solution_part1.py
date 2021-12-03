#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 5A
"""

import argparse

#==============================================================================


def get_args():
	"""
	Cmd line argument parsing (preprocessing)
	"""
	# Assign description to the help doc
	parser = argparse.ArgumentParser(\
		description='Advent of code 2020')

	# Add arguments
	parser.add_argument(\
		'-i',
		'--infile',
		type=str,
		help='Inputfilename',
		required=True)

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile


#==============================================================================

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()

	boards = [x.strip() for x in data]

	sids = []
	for board in boards:
		row = row = int(board[:7].replace('B', '1').replace('F', '0'),2)
		col = board[7:]
		col = int(board[7:].replace('L', '0').replace('R', '1'),2)
		sid =  row * 8 + col
		sids.append(sid)
		#print("{} -> row, {}, column {}, seat ID {}".format(board, row, col, sid))
	print("Part 1: {}".format(max(sids)))

	sids = sorted(sids)
	last = sids[0]
	for s in sids[1:]:
		if s == last + 2:
			print("Part 2: {}".format(last + 1))
		last = s

#==============================================================================

main()

#EOF
