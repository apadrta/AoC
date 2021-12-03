#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 17A
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
	parser.add_argument(\
		'-c',
		'--cycles',
		type=int,
		help='Number of cycles',
		required=True)
	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile, args.cycles


#==============================================================================


def main():
	"""
	Main function
	"""

	# process args
	infile, cycles = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]

	cubex = []
	cubey = []
	cubez = []
	cubeall = []
	for i in range(0, len(lines)):
		for j in range(0, len(lines[i])):
			if lines[i][j] == '#':
				cubex.append(j)
				cubey.append(i)
				cubez.append(0)
				cubeall.append([j, i, 0])

	# create neiborhoood
	nb = []
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			for k in [-1, 0, 1]:
				nb.append([i, j, k])
	nb.remove([0, 0, 0])

	#print(nb, len(nb))

	def pretty_print(cubes):
		xs = [x[0] for x in cubes] 
		ys = [x[1] for x in cubes] 
		zs = [x[2] for x in cubes] 
		for z in range(min(zs), max(zs) + 1):
			print("layer = {}".format(z))
			for y in range(min(ys), max(ys) + 1):
				out = ''
				for x in range(min(xs), max(xs) + 1):
					if [x, y, z] in cubes:
						out += '#'
					else:
						out += '.'
				print(out)

			
				
	

	print("====================================================")
	pretty_print(cubeall)
	#for i in range(0, len(cubex)):
	#	print((cubex[i], cubey[i], cubez[i]))

	c = 0
	while c < cycles:
		newcubes = []

		for x in range(min(cubex) -1, max(cubex) + 2):
			for y in range(min(cubey) -1, max(cubey) + 2):
				for z in range(min(cubez) -1, max(cubez) + 2):
					# compute active neighbors
					active = 0
					for dx, dy, dz in nb:
						#print("  ", [x + dx, y + dy, z + dz])
						if [x + dx, y + dy, z + dz] in cubeall:
							active += 1
							#print("  ++ ", active)
					# evaluate
					#print("  ", active, [x, y, z] in cubeall)
					if [x, y, z] in cubeall and active in (2,3):
						#print(x, y, z)
						#print("  keep active")
						newcubes.append([x, y, z])
					if [x, y, z] not in cubeall and active == 3:
						#print(x, y, z)
						#print("  new active")
						newcubes.append([x, y, z])
		cubex = []
		cubey = []
		cubez = []
		for x, y, z in newcubes:
			cubex.append(x)
			cubey.append(y)
			cubez.append(z)
		cubeall = newcubes
		#print("newcubes", newcubes)
		#print("cubeall", cubeall)

		print("====================================================")
		pretty_print(cubeall)
		#for i in range(0, len(cubex)):
		#	print((cubex[i], cubey[i], cubez[i]))
		
		c += 1

	print("Part 1:", len(cubeall))	

#==============================================================================

main()

#EOF
