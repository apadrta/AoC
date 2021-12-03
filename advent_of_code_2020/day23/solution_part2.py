#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 23A
"""

import argparse
import string
import numpy as np
import copy


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
	parser.add_argument(\
		'-s',
		'--steps',
		type=int,
		help='number of steps',
		required=True)

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile, args.steps


#==============================================================================


def main():
	"""
	Main function
	"""

	# process args
	infile, steps = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]

	# init field
	ncups = 1000000
	cups = np.zeros((ncups), dtype=int)

	for i in range(0, len(lines[0])):
		# add data from file
		cups[i] = lines[0][i]

	for i in range(len(lines[0])+1, ncups + 1):
		# add to maximum
		cups[i-1] = i
	
	#print(cups)

	s = 0
	ci = -1
	while s < steps:
		#print("Step {}".format(s+1))
		#print("  Input", cups)
		ci = (ci + 1) % ncups	# cup index
		#print("  Cup: index {}, value {}".format(ci, cups[ci]))
		#ci = cups[0]
		p1i = (ci + 1) % ncups	# first part index
		p2i = (ci + 2) % ncups	# second part index
		p3i = (ci + 3) % ncups	# third par index
		#print("  Part indexes", p1i, p2i, p3i)
		#print("  Part: from {}, to {}".format(p1i, p3i))
		#c3 = cups[1:4]
		d = cups[ci] - 1
		if d == 0:
			d = ncups
		while d in cups[p1i:p3i+1]:
			d = d - 1
			if d == 0:
				d = ncups
		di = np.where(cups==d)[0][0]
		#print("  Destination: value {}, index {}".format(d, di))

		#print(cups[:ci+1], ci)	# from beginning to current
		#print(cups[p1i:p1i+3], p1i)	# part to move
		#print(cups[p1i+3:di+1], di) # part between movedp and destination (include destination)
		#print(cups[p1i+4:])	# part after destination
		#print(cups[:ci+1] + cups[p1i+3:di+1] + cups[p1i:p1i+3] + cups[p1i+4:])
		if p1i < di:
			# array not splitted
			move = copy.deepcopy(cups[p1i:p1i+3])
			#print(move)
			#print(cups[p1i:di+1])
			#print(cups[p1i+3:di+1])
			lena = di + 1 - (p1i+3)
			#print("part", cups[p1i+3:di+1])
			#print("old", cups[p1i: p1i + lena])
			#print(p1i + lena, p1i + lena +3 -1)
			cups[p1i:p1i + lena] = cups[p1i+3:di+1] # move part a
			cups[p1i + lena: p1i + lena + 3] = move # rewrite part p
		else:
			part1 = cups[p1i:]
			part2 = cups[:di+1]
			lenp1 = len(part1)
			lenp2 = len(part2)
			tmp = np.zeros((lenp1+lenp2), dtype=int)
			tmp[0:lenp1] = part1
			tmp[lenp1:] = part2
			#print("tmp1", tmp)
			move = copy.deepcopy(tmp[0:3])
			tmp[:-3] = tmp[3:]
			tmp[-3:] = move
			#print("tmp2", tmp)
			cups[p1i:] = tmp[:ncups-p1i]
			cups[:lenp2] = tmp[ncups-p1i:]
			

			#print(cups[p1i:p1i + len(part1)])
			#cups[p1i:p1i + len(part1)] = part1
			#cups[p1i + len(part1):] = part2[:))]

		
		#cups[ci+1] = cups[di] 

		#cups[di+1:di+1+3] = move
		#cups[di+1+3+1] 
		# move three cups to final position
		#print([cups[0]])
		#print([cups[4:di+1]])
		#print(c3)
		#print([cups[di+1:]])
#		cups = [cups[0]] + cups[4:di+1] + c3 + cups[di+1:]
		#print("  output", cups)

		s += 1

		if s % 1000 == 0:
			print("Step=",s)

	#print(cups)

	i = np.where(cups==1)[0][0]
	a = (i + 1) % ncups
	b = (i + 2) % ncups
	print(a)
	print(b)
	print("Part 2:", cups[a]*cups[b])

#==============================================================================

main()

#EOF
