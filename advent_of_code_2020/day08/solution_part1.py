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

class ConsoleCPU():
	"""
	Class for running ELF CPU
	"""

	def __init__(self):
		"""
		Constructor
		"""
		self.code = []
		self.acc = 0
		self.ptr = 0

	def read_code(self, filename):
		"""
		Read program code from file
		"""
		data = []
		with open(filename, "r") as fileh:
			data = fileh.readlines()

		self.code = []
		for item in data:
			inst, value = item.strip().split(' ', 1)
			self.code.append([inst, int(value), 0]) # instruction value, repetition
		self.ptr = 0

	def run(self, debug = False):
		"""
		Run the console processor (or continue running when previously stopped)
		"""
		while True:
			if self.code[self.ptr][2] > 0:
				#print("Repeat instruction {}, Ptr:{}, acc: {}".format(self.code[self.ptr], self.ptr, self.acc))
				print("Part1: {}".format(self.acc))
				break
			if debug:
				print("Ptr: {}, Instruction {}, Acc: {}".format(self.ptr, self.code[self.ptr], self.acc))
			if self.code[self.ptr][0] == 'nop':
				self.code[self.ptr][2] +=1
				self.ptr += 1
			elif self.code[self.ptr][0] == 'acc':
				self.code[self.ptr][2] +=1
				self.acc += self.code[self.ptr][1]
				self.ptr += 1
			elif self.code[self.ptr][0] == 'jmp':
				self.code[self.ptr][2] +=1
				self.ptr += self.code[self.ptr][1]
			

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read and run code
	cpu = ConsoleCPU()
	cpu.read_code(infile)
	res = cpu.run(False)

#==============================================================================

main()

#EOF
