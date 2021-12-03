#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 14A
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
	lines = [x.strip() for x in data]

	memory = {}
	mask = 36 * 'X'

	for line in lines:
		inst, value = line.split(' = ')
		if inst == 'mask':
			mask = value
		elif inst[:3] == 'mem':
			#print('---')
			#print(mask)
			addr = bin(int(inst[4:-1]))[2:]
			addr = (len(mask) - len(addr)) * '0' + addr
			#print(addr)
			baddr = ''
			for i in range(0, len(mask)):
				if mask[i] == '0':
					baddr += addr[i]
				else:
					baddr += mask[i]
			#print(baddr)
			process = [baddr]
			addrs = []
			while process:
				waddr = process.pop()
				if waddr.count('X') > 1:
					process.append(waddr.replace('X', '1', 1))
					process.append(waddr.replace('X', '0', 1))
				else:
					addrs.append(waddr.replace('X', '1', 1))
					addrs.append(waddr.replace('X', '0', 1))

			#print(mval)
			#print(int(mval, 2))
			#print(addrs)
			for addr in addrs:
				memory[addr] = int(value)
	#print(memory)

	summ = 0
	for value in memory.values():
		summ += value
	print("Part 2: {}".format(summ))



	

#==============================================================================

main()

#EOF
