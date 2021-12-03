#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 11A
"""

import argparse
import numpy as np
import collections

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

class Seats():
	"""
	Class for seat problem solution
	"""

	def __init__(self):
		"""
		Constructor
		"""
		self.arr = None
		self.maxx = 0
		self.maxy = 0

	def read(self, filename):
		"""
		Read definition from file
		"""
		data = []
		with open(filename, "r") as fileh:
			data = fileh.readlines()
		self.maxx = len(data[0].strip())
		self.maxy = len(data)
		self.arr = np.full([self.maxx, self.maxy], fill_value=0, dtype=int)
		y = 0
		while y < len(data):
			x = 0
			while x < len(data[y].strip()):
				val = 0	# floor
				if data[y][x] == 'L':
					val = 1	# seat
				elif data[y][x] == '#':
					val = 2 # taken seat
				self.arr[(x, y)] = val
				x += 1
			y += 1

	def adjanced(self, pos):
		"""
		Count used adjanced seats
		"""
		diffs = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, 1), (0, -1)]
		adj = 0
		for diff in diffs:
			x = pos[0] + diff[0]
			y = pos[1] + diff[1]
			while x >= 0 and x < self.maxx and y >= 0 and y < self.maxy:
				if self.arr[(x, y)] == 2:
					adj += 1
					break
				if self.arr[(x, y)] == 1:
					break
				x = x + diff[0]
				y = y + diff[1]

		return(adj)


	def eval_round(self):
		"""
		eval one seat/leave round
		"""
		newarr = np.full([self.maxx, self.maxy], fill_value=0, dtype=int)
		change = False
		for x in range(0, self.maxx):
			for y in range(0, self.maxy):
				pos = (x, y)
				used = self.adjanced(pos)
				if self.arr[pos] == 1 and used == 0:
					change = True
					newarr[pos] = 2
				elif self.arr[pos] == 2 and used >= 5:
					change = True
					newarr[pos] = 1
				else:
					newarr[pos] = self.arr[pos]
		self.arr = newarr
		return change

	def find_stable(self):
		""" 
		find stable position
		"""
		change = True
		while change:
			change = self.eval_round()

		seats = []
		for row in list(self.arr):
			seats.extend(list(row))
		return seats.count(2)



def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	obj = Seats()
	obj.read(infile)
	#pos = (1,1)
	#print(obj.adjanced(pos))
	#obj.eval_round()
	#print(obj.adjanced(pos))
	print("Part 2: {}".format(obj.find_stable()))


#==============================================================================

main()

#EOF
