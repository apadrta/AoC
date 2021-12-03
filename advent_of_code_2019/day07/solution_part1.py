#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 7A
"""

import argparse
from math import floor
from itertools import permutations

#==============================================================================


def get_args():
	"""
	Cmd line argument parsing (preprocessing)
	"""
	# Assign description to the help doc
	parser = argparse.ArgumentParser(\
		description='Advent of code 2019')

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

def run_elf_cpu(code, inputs, debug = False):
	"""
	Run the elf processor
	"""
	output = []
	maxparams = 3
	inputindex = 0 
	ptr = 0
	while True:
		# prepoces mode and opcode
		istr = "0" * (maxparams + 1) + str(code[ptr])
		opcode = int(istr[-2:])
		mode = [int(x) for x in istr[:-2][::-1]]
		if debug:
			print("\nPTR: {}, istr: {}, opcode: {}, mode: {}".format(ptr, istr, opcode, mode))


		# prepare mode parameters
		params = [0] * 3
		if opcode in [1, 2, 4, 5, 6, 7, 8]:
			params[0] = code[ptr + 1]
			if mode[0] == 0:
				params[0] = code[code[ptr + 1]]
		if opcode in [1, 2, 5, 6, 7, 8]:
			params[1] = code[ptr + 2]
			if mode[1] == 0:
				params[1] = code[code[ptr + 2]]
		if opcode in []:
			params[2] = code[ptr + 3]
			if mode[2] == 0:
				params[2] = code[code[ptr + 3]]

		#print(ptr, nums[ptr])
		if opcode == 99:
			#print("program completed")
			break

		elif opcode == 1:
			# add
			if debug:
				print(code[ptr:ptr + 4])
				print("ADD [{}] {} -> {} ({} M{} + {} M{})".format(code[ptr + 3], code[code[ptr + 3]], params[0] + params[1], params[0], mode[0], params[1], mode[1]))
			code[code[ptr + 3]] = params[0] + params[1]
			ptr += 4

		elif opcode == 2:
			# multiply
			if debug:
				print(code[ptr:ptr + 4])
				print("MLT [{}] {} -> {} ({} M{} * {} M{})".format(code[ptr + 3], code[code[ptr + 3]], params[0] + params[1], params[0], mode[0], params[1], mode[1]))
			code[code[ptr + 3]] = params[0] * params[1]
			ptr += 4

		elif opcode == 3:
			# input
			indata = inputs[inputindex]
			inputindex += 1
			if debug:
				print(code[ptr:ptr + 2])
				print("INP [{}] {} -> {}".format(code[ptr + 1], code[code[ptr + 1]], indata))
			code[code[ptr + 1]] = indata
			ptr += 2

		elif opcode == 4:
			# output
			if debug:
				print(code[ptr:ptr + 2])
				print("OUT {}".format(params[0]))			
			output.append(params[0])
			ptr += 2

		elif opcode == 5:
			# jump-if-true
			if debug:
				print(code[ptr:ptr + 3])
				print("JTR PTR -> {}".format("(JUMP, {} not 0)".format(params[0]) if params[0] != 0 else "(+3)"))			
			
			if params[0] == 0:
				ptr += 3
			else:
				ptr = params[1]
				
		elif opcode == 6:
			# jump-if-false
			if debug:
				print(code[ptr:ptr + 3])
				print("JFA PTR -> {}".format("(JUMP, {} is 0)".format(params[0]) if params[0] != 0 else "(+3)"))			
			
			if params[0] == 0:
				ptr = params[1]
			else:
				ptr += 3
				
		elif opcode == 7:
			# less than
			if debug:
				print(code[ptr:ptr + 4])
				print("LTH [{}] {} -> {} ({} M{} <? {} M{})".format(code[ptr + 3], code[code[ptr + 3]], 1 if params[0] < params[1] else 0, params[0], mode[0], params[1], mode[1]))
			if params[0] < params[1]:
				code[code[ptr + 3]] = 1
			else:
				code[code[ptr + 3]] = 0
			ptr += 4
			
		elif opcode == 8:
			# equals
			if debug:
				print(code[ptr:ptr + 4])
				print("EQL [{}] {} -> {} ({} M{} <? {} M{})".format(code[ptr + 3], code[code[ptr + 3]], 1 if params[0] == params[1] else 0, params[0], mode[0], params[1], mode[1]))
			if params[0] == params[1]:
				code[code[ptr + 3]] = 1
			else:
				code[code[ptr + 3]] = 0
			ptr += 4
			
		else:
			print("ERROR: unknown instruction")
			break

	return output

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.read()

	orders = list(permutations([0, 1, 2, 3, 4]))

	maxsignal = 0
	for order in orders:
		signal = 0
		for i in order:
			code = [int(x) for x in data.strip().split(',')]
			signal = run_elf_cpu(code, [int(i), int(signal)], False)[0] # part 1
		print(signal)
		if signal > maxsignal:
			maxsignal = signal
	
	print("Part 1: {}".format(maxsignal))

#==============================================================================

main()

#EOF
