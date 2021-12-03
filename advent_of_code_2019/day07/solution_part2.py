#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 7B
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

class ElfCPU():
	"""
	Class for running ELF CPU
	"""

	def __init__(self):
		"""
		Constructor
		"""
		self.code = []
		self.output = []
		self.inputs = []
		self.inputindex = 0
		self.ptr = 0

	def read_code(self, filename):
		"""
		Read program code from file
		"""
		data = []
		with open(filename, "r") as fileh:
			data = fileh.read()
		self.code = [int(x) for x in data.strip().split(',')]

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
			if opcode in [1, 2, 4, 5, 6, 7, 8]:
				params[0] = self.code[self.ptr + 1]
				if mode[0] == 0:
					params[0] = self.code[self.code[self.ptr + 1]]
			if opcode in [1, 2, 5, 6, 7, 8]:
				params[1] = self.code[self.ptr + 2]
				if mode[1] == 0:
					params[1] = self.code[self.code[self.ptr + 2]]
			if opcode in []:
				params[2] = self.code[self.ptr + 3]
				if mode[2] == 0:
					params[2] = self.code[self.ode[self.ptr + 3]]

			if opcode == 99:
				#print("program completed")
				return 99

			elif opcode == 1:
				# add
				if debug:
					print(self.code[self.ptr:self.ptr + 4])
					print("ADD [{}] {} -> {} ({} M{} + {} M{})".format(self.code[self.ptr + 3], self.code[self.code[self.ptr + 3]], params[0] + params[1], params[0], mode[0], params[1], mode[1]))
				self.code[self.code[self.ptr + 3]] = params[0] + params[1]
				self.ptr += 4

			elif opcode == 2:
				# multiply
				if debug:
					print(self.code[self.ptr:self.ptr + 4])
					print("MLT [{}] {} -> {} ({} M{} * {} M{})".format(self.code[self.ptr + 3], self.code[self.code[self.ptr + 3]], params[0] + params[1], params[0], mode[0], params[1], mode[1]))
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
					print(self.code[self.ptr:self.ptr + 2])
					print("INP [{}] {} -> {}".format(self.code[self.ptr + 1], self.code[self.code[self.ptr + 1]], indata))
				self.code[self.code[self.ptr + 1]] = indata
				self.ptr += 2

			elif opcode == 4:
				# output
				if debug:
					print(self.code[self.ptr:self.ptr + 2])
					print("OUT {}".format(params[0]))			
				self.output.append(params[0])
				self.ptr += 2
				#return 4

			elif opcode == 5:
				# jump-if-true
				if debug:
					print(self.code[self.ptr:self.ptr + 3])
					print("JTR PTR -> {}".format("(JUMP, {} not 0)".format(params[0]) if params[0] != 0 else "(+3)"))			
				if params[0] == 0:
					self.ptr += 3
				else:
					self.ptr = params[1]
				
			elif opcode == 6:
				# jump-if-false
				if debug:
					print(self.code[self.ptr:self.ptr + 3])
					print("JFA PTR -> {}".format("(JUMP, {} is 0)".format(params[0]) if params[0] != 0 else "(+3)"))			
				if params[0] == 0:
					self.ptr = params[1]
				else:
					self.ptr += 3
				
			elif opcode == 7:
				# less than
				if debug:
					print(self.code[self.ptr:self.ptr + 4])
					print("LTH [{}] {} -> {} ({} M{} <? {} M{})".format(self.code[self.ptr + 3], self.code[self.code[self.ptr + 3]], 1 if params[0] < params[1] else 0, params[0], mode[0], params[1], mode[1]))
				if params[0] < params[1]:
					self.code[self.code[self.ptr + 3]] = 1
				else:
					self.code[self.code[self.ptr + 3]] = 0
				self.ptr += 4
			
			elif opcode == 8:
				# equals
				if debug:
					print(self.code[self.ptr:self.ptr + 4])
					print("EQL [{}] {} -> {} ({} M{} <? {} M{})".format(self.code[self.ptr + 3], self.code[self.code[self.ptr + 3]], 1 if params[0] == params[1] else 0, params[0], mode[0], params[1], mode[1]))
				if params[0] == params[1]:
					self.code[self.code[self.ptr + 3]] = 1
				else:
					self.code[self.code[self.ptr + 3]] = 0
				self.ptr += 4
			
			else:
				print("ERROR: unknown instruction")
				return 666

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	#cpu = ElfCPU()
	#cpu.read_code(infile)
	#cpu.add_inputs([5, 0])
	#res = cpu.run()
	#print(res, cpu.get_output())
	
	#cpu.add_inputs([5, 0])
	#res = cpu.run(False)
	#print(res, cpu.get_output())

	#cpu.add_inputs([5, 0])
	#res = cpu.run(False)
	#print(res, cpu.get_output())
	#exit(1)

	orders = list(permutations([5, 6, 7, 8, 9]))

	#orders = [[9,8,7,6,5], ]
	#orders = [[9,7,8,5,6], ]


	maxsignal = 0
	for order in orders:

		thrusters = []
		for i in range(0,5):
			thrusters.append(ElfCPU())
			thrusters[i].read_code(infile)
			thrusters[i].add_inputs([order[i]])
			#print(thrusters[i].get_state())
		
		signal = 0
		while True:
			for i in range(0,5):
				#print("T:{} init:{} sig:{}".format(i, order[i], signal))
				#print("Start {} {}".format(i, thrusters[i].get_state()))
				thrusters[i].add_inputs([int(signal)])
				res = thrusters[i].run()
				#print("  output: ",thrusters[i].get_output())
				signal = thrusters[i].get_output()[-1]
				#print("End {} {}".format(i, thrusters[i].get_state()))
			if res == 99:
				
				break
		if signal > maxsignal:
			maxsignal = signal
	
	print("Part 2: {}".format(maxsignal))

#==============================================================================

main()

#EOF
