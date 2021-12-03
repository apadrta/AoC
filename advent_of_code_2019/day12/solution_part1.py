#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 12A
"""

import argparse
import numpy as np
import collections
import math
from math import pi

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
	parser.add_argument(\
		'-s',
		'--steps',
		type=int,
		help='Number of simulation steps',
		required=True)

	# Array for all arguments passed to script
	args = parser.parse_args()

	# Return arg variables
	return args.infile, args.steps


#==============================================================================

class Moon():
	"""
	Class for seat problem solution
	"""

	def __init__(self, position, name):
		"""
		Constructor
		"""
		self.name = name
		self.pos = position
		self.velocity = [0, 0, 0]
		self.gravchange = [0, 0, 0]

	def GravityForces(self, moon):
		"""
		update itself according to othermoon
		"""
		#print("Gravitation in action between {} and {}".format(self.name, moon.name))
		for i in range(0,3):
			if self.pos[i] < moon.pos[i]:
				self.gravchange[i] += 1
				moon.gravchange[i] -= 1
			elif self.pos[i] > moon.pos[i]:
				self.gravchange[i] -= 1
				moon.gravchange[i] += 1

	def Move(self):
		"""
		Move with moon
		"""
		for i in range(0, 3):
			self.velocity[i] += self.gravchange[i]
			self.pos[i] += self.velocity[i]
			self.gravchange[i] = 0

	def GetEnergy(self):
		"""
		compute energy of moon
		"""
		p_energy = 0
		k_energy = 0
		for i in range(0, 3):
			p_energy += abs(self.pos[i])
			k_energy += abs(self.velocity[i])
		return p_energy * k_energy


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

	# init moons
	moons = []
	i = 0
	for item in data:
		parts = item.strip().replace('>', '').replace('<', '').replace('>', '').split(', ')
		coords = []
		for part in parts:
			coords.append(int(part.split('=')[1]))
		
		moons.append(Moon(coords, "Moon #{}".format(i)))
		i += 1
		#<x=3, y=3, z=0>

	# move with moons
	s = 0
	while s < steps:
		for i in range(0, len(moons)):
			for j in range(i+1, len(moons)):
				moons[i].GravityForces(moons[j])
		for moon in moons:
			#print("Force", moon.name, moon.gravchange)
			moon.Move()
			#print("Position", moon.name, moon.pos)
			#print("Velocity", moon.name, moon.velocity)
		s += 1
	energy = 0
	for moon in moons:
		energy += moon.GetEnergy()
	print("Part 1: ", energy)
	

#==============================================================================

main()

#EOF
