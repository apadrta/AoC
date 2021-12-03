#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 13A
"""

import argparse
#from math import floor
from itertools import permutations
import numpy as np
from PIL import Image

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

class ElfCPU():
	"""
	Class for running ELF CPU
	"""

	def __init__(self):
		"""
		Constructor
		"""
		self.code = {}
		self.output = []
		self.inputs = []
		self.inputindex = 0
		self.ptr = 0
		self.offset = 0

	def read_code(self, filename):
		"""
		Read program code from file
		"""
		data = []
		with open(filename, "r") as fileh:
			data = fileh.read()
		#self.code = [int(x) for x in data.strip().split(',')]
		rcode = [int(x) for x in data.strip().split(',')]
		i = 0
		self.code = {}
		for num in rcode:
			self.code[i] = num
			i += 1

	def reset(self):
		"""
		Reset computer
		"""
		self.code = {}
		self.output = []
		self.inputs = []
		self.inputindex = 0
		self.ptr = 0
		self.offset = 0


	def get_state(self):
		"""
		Print CPU state (debug purpose)
		"""
		return "PTR: {}, InputIndex = {}, Inputs: {}, Output: {}".format(self.ptr, self.inputindex, self.inputs, self.output)

	def get_output(self):
		"""
		Provide output
		"""
		return self.output

	def add_inputs(self, new_inputs):
		"""
		Add new input array to current one
		"""
		self.inputs = self.inputs + new_inputs

	def set_inputs(self, new_inputs):
		"""
		Add input array 
		"""
		self.inputs = new_inputs
		self.inputindex = 0

	def init_var(self, index, mode):
		"""
		Initialize variable
		"""
		if mode == 1:
			# mode 1 = use number directly
			addr = self.ptr + index + 1
		if mode == 0:
			# mode 0 = use number as pointer
			addr = self.code[self.ptr + index + 1]
		elif mode == 2:
			# mode 2 = use number as pointer with offset
			addr = self.code[self.ptr + index + 1] + self.offset
		if addr not in self.code:
			self.code[addr] = 0
		
		return self.code[addr]


	def run(self, debug = False):
		"""
		Run the elf processor (or continue running when previously stopped)
		"""
		maxparams = 3	# maxparams for instructions
		while True:
			# prepoces mode and opcode
			istr = "0" * (maxparams + 1) + str(self.code[self.ptr])
			opcode = int(istr[-2:])
			mode = [int(x) for x in istr[:-2][::-1]]
			if debug:
				print("\nPTR: {}, istr: {}, opcode: {}, mode: {}".format(self.ptr, istr, opcode, mode))

			# prepare mode parameters
			params = [0] * 3
			if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
				params[0] = self.init_var(0, mode[0])
			if opcode in [1, 2, 5, 6, 7, 8]:
				params[1] = self.init_var(1, mode[1])
			if opcode in []:
				params[2] = self.init_var(2, mode[2])

			if opcode == 99:
				#print("program completed")
				return 99

			elif opcode == 1:
				# add
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1], self.code[self.ptr + 2], self.code[self.ptr + 3]])
					print("ADD [{}] {} -> {} ({} M{} + {} M{})".format(self.code[self.ptr + 3], self.code[self.code[self.ptr + 3]], params[0] + params[1], params[0], mode[0], params[1], mode[1]))
				if mode[2] == 2:
					self.code[self.code[self.ptr + 3] + self.offset] = params[0] + params[1]
				else:
					self.code[self.code[self.ptr + 3]] = params[0] + params[1]
				self.ptr += 4

			elif opcode == 2:
				# multiply
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1], self.code[self.ptr + 2], self.code[self.ptr + 3]])
					print("MLT [{}] {} -> {} ({} M{} * {} M{})".format(self.code[self.ptr + 3], self.code[self.code[self.ptr + 3]], params[0] + params[1], params[0], mode[0], params[1], mode[1]))
				if mode[2] == 2:
					self.code[self.code[self.ptr + 3] + self.offset] = params[0] * params[1]
				else:
					self.code[self.code[self.ptr + 3]] = params[0] * params[1]
				self.ptr += 4

			elif opcode == 3:
				# input
				if self.inputindex >= len(self.inputs):
					# not enough inputs
					if debug:
						print("No more inputs, add some and run me again")
					return 3
				indata = self.inputs[self.inputindex]
				self.inputindex += 1
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1]])
					print("INP [{}] {} -> {}".format(self.code[self.ptr + 1], self.code[self.code[self.ptr + 1]], indata))
				if mode[0] == 2:
					self.code[self.code[self.ptr + 1] + self.offset] = indata
				else:
					self.code[self.code[self.ptr + 1]] = indata
				self.ptr += 2

			elif opcode == 4:
				# output
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1]])
					print("OUT {}".format(params[0]))			
				self.output.append(params[0])
				self.ptr += 2
				#return 4

			elif opcode == 5:
				# jump-if-true
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1], self.code[self.ptr + 2]])
					print("JTR PTR -> {}".format("(JUMP, {} not 0)".format(params[0]) if params[0] != 0 else "(+3)"))			
				if params[0] == 0:
					self.ptr += 3
				else:
					self.ptr = params[1]
				
			elif opcode == 6:
				# jump-if-false
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1], self.code[self.ptr + 2]])
					print("JFA PTR -> {}".format("(JUMP, {} is 0)".format(params[0]) if params[0] != 0 else "(+3)"))			
				if params[0] == 0:
					self.ptr = params[1]
				else:
					self.ptr += 3
				
			elif opcode == 7:
				# less than
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1], self.code[self.ptr + 2], self.code[self.ptr + 3]])
					print("LTH [{}] {} -> {} ({} M{} <? {} M{})".format(self.code[self.ptr + 3], self.code[self.code[self.ptr + 3]], 1 if params[0] < params[1] else 0, params[0], mode[0], params[1], mode[1]))
				if params[0] < params[1]:
					val = 1
				else:
					val = 0
				if mode[2] == 2:
					self.code[self.code[self.ptr + 3] + self.offset] = val
				else:
					self.code[self.code[self.ptr + 3]] = val
				self.ptr += 4
			
			elif opcode == 8:
				# equals
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1], self.code[self.ptr + 2], self.code[self.ptr + 3]])
					print("EQL [{}] -> {} ({} M{} <? {} M{})".format(self.code[self.ptr + 3], 1 if params[0] == params[1] else 0, params[0], mode[0], params[1], mode[1]))
				if params[0] == params[1]:
					val = 1
				else:
					val = 0
				if mode[2] == 2:
					self.code[self.code[self.ptr + 3] + self.offset] = val
				else:
					self.code[self.code[self.ptr + 3]] = val
				self.ptr += 4

			elif opcode == 9:
				# change offset
				if debug:
					print([self.code[self.ptr], self.code[self.ptr + 1]])
					print("BOF {} -> {}".format(self.offset, self.offset + params[0]))
				self.offset += params[0]
				self.ptr += 2

			else:
				print("ERROR: unknown instruction")
				return 666


def print_grid(grid, xdim, ydim):
	"""
	print grid in human readable form
	"""
	for i in range(0, ydim):
		row = ''
		for j in range(0, xdim):
			if grid[(i, j)] == 0:
				row += ' '
			elif grid[(i, j)] == 1:
				row += '#'
			elif grid[(i, j)] == 2:
				row += 'X'
			elif grid[(i, j)] == 3:
				row += '='
			elif grid[(i, j)] == 4:
				row += 'O'
		print(row)

def output2grid(output, xdim, ydim):
	"""
	format cpu output to grid structure
	"""
	xs = output[0::3]
	ys = output[1::3]
	tiles = output[2::3]
	grid = np.zeros((ydim, xdim))
	ballx = 0
	paddlex = 0
	for i in range(0, len(tiles)):
		if xs[i] == -1 and ys[i] == 0:
			score = tiles[i]
		else:
			grid[(ys[i], xs[i])] = tiles[i]
			if tiles[i] == 4:
				ballx = xs[i]
			elif tiles[i] == 3:
				paddlex = xs[i]

	return grid, ballx, paddlex, score

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()


	# part one
	floor = {}
	posx = 0
	posy = 0
	heading = 0 # 0 up, 1 right, 2, down, 3 left 

	cpu = ElfCPU()
	cpu.read_code(infile)
	cpu.code[0] = 2	# insert quarter
	
	res = cpu.run(False)
	inst = cpu.get_output()
	print("RES ", res)
	# process output
	xs = inst[0::3]
	ys = inst[1::3]
	tiles = inst[2::3]
	score = 0
	xdim = max(xs) + 1
	ydim = max(ys) + 1
	
	grid, bx, px, score = output2grid(inst, xdim, ydim)
	print_grid(grid, xdim, ydim)
	ai = 0
	while np.count_nonzero(grid == 2) > 0:
	#for s in range(0, 100):


		cpu.set_inputs([ai])
		res = cpu.run(False)
		inst = cpu.get_output()
		grid, bx, px, score = output2grid(inst, xdim, ydim)
		if bx < px:
			ai = -1
		elif bx > px:
			ai = +1
		else:
			ai = 0
		#print(bx, px, ai, np.count_nonzero(grid == 2))

		#print("Score: {}".format(score))
		#print_grid(grid, xdim, ydim)
		#if score % 1000 == 0:
		#	print(score)

	print("Part 2:", score)

#==============================================================================

main()

#EOF
