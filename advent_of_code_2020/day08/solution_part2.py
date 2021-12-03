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
		self.corr = []

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
		self.acc = 0

	def find_corrupted(self):
		"""
		Initialize list of potentialy fixes of corrupted instructions
		"""
		self.corr = []
		for i in range(0, len(self.code)):
			if self.code[i][0] == 'nop':
				self.corr.append([i, 'jmp'])
			elif self.code[i][0] == 'jmp':
				self.corr.append([i, 'nop'])

		return self.corr

	def fix_code(self, patch):
		"""
		fix instruction
		"""
		self.code[patch[0]][0] = patch[1]


	def run(self, debug = False):
		"""
		Run the console processor (or continue running when previously stopped)
		"""
		while True:
			if debug:
				print("Ptr: {}, Instruction {}".format(self.ptr, self.code[self.ptr]))
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
			if debug:
				print("  -> Acc: {}".format(self.acc))

			if self.ptr > len(self.code):
				return (2, self.acc) # end of code (abnormal)		

			if self.ptr == len(self.code):
				return (1, self.acc) # end of code (normal)

			if self.code[self.ptr][2] > 0:
				#print("Repeat instruction {}, Ptr:{}, acc: {}".format(self.code[self.ptr], self.ptr, self.acc))
				return (0, self.acc) # end on repeat

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read and run code
	cpu = ConsoleCPU()
	cpu.read_code(infile)
	corrupted = cpu.find_corrupted()
	for c in corrupted:
		#print("=== {} ===",format(c))
		cpu.read_code(infile)
		cpu.fix_code(c)
		res = cpu.run(False)
		if res[0] == 1:
			print("Part2: {}".format(res[1]))
			break

#==============================================================================

main()

#EOF
