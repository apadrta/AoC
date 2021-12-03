#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 13A
"""

import argparse
import math

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

def get_time(ref_intv, intv, delta, step):
	"""
	compute min time step
	"""
	n = step
	while True:
		if (n * ref_intv + delta) % intv == 0:
			return n * ref_intv
		n += step

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

	buses = lines[1].split(',')
	depts = []
	for i in range(0, len(buses)):
		if buses[i] != 'x':
			depts.append([int(buses[i]), i])

	zeroi = depts[0][0]
	basics = []
	steps = []
	for dept in depts[1:]:
		basics.append(get_time(zeroi, dept[0], dept[1], 1))
		steps.append(math.lcm(zeroi, dept[0]))
	#print(basics)
	#print(steps)

	def goup(basea, stepa, baseb, stepb):
		if basea < baseb:
			add = (baseb - basea) // stepa * stepa
			if (baseb - basea) % stepa != 0:
				add += stepa
			return basea + add, baseb
		elif baseb < basea:
			add = (basea - baseb) // stepb * stepb
			if (basea - baseb) % stepb != 0:
				add += stepb
			return basea, baseb + add
		return basea, baseb


	while len(basics) > 1:
		fin = False
		while basics[0] != basics[1]:
			ret = goup(basics[0], steps[0], basics[1], steps[1])
			basics[0] = ret[0]
			basics[1] = ret[1]
		#print(basics)
		basics = basics[1:]
		newstep = math.lcm(steps[0],steps[1])
		steps = steps[1:]
		steps[0] = newstep
		#print(basics)

	print("Part 2:", basics[0])
	
		



#==============================================================================

main()

#EOF
