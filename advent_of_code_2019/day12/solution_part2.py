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
import copy 

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

	xs = []
	ys = []
	zs = []
	for item in data:
		parts = item.strip().replace('>', '').replace('<', '').replace('>', '').split(', ')
		xs.append(int(parts[0].split('=')[1]))
		ys.append(int(parts[1].split('=')[1]))
		zs.append(int(parts[2].split('=')[1]))

	#print(xs)
	#print(ys)
	#print(zs)

	def simulate_axis(pos, step):
		"""
		simulate one axis
		"""
		s = 0
		vel = [0] * len(pos)
		arange = range(0, len(pos))
		hist = [copy.deepcopy(pos + vel)]
		hist_o0 = [pos[0]]
		hist_o1 = [pos[1]]
		print(hist)
		while True:
			#compute gravity
			grav = [0] * len(pos)
			for i in arange:
				for j in arange:
					if pos[i] < pos[j]:
						grav[i] += 1
					elif pos[i] > pos[j]:
						grav[i] -= 1
			#change and apply velocity
			for i in arange:
				vel[i] += grav[i]
				pos[i] += vel[i]
	
			s += 1
			if s > step or (pos[0] in hist_o0 and pos[1] in hist_o1 and pos + vel in hist):
				print(pos + vel)
				print(s)
				break
			hist.append(copy.deepcopy(pos + vel))
			hist.append(copy.deepcopy(pos[0]))
			hist.append(copy.deepcopy(pos[1]))
			
		return s

	nx = simulate_axis(xs, steps)
	print(nx)
	ny = simulate_axis(ys, steps)
	print(ny)
	nz = simulate_axis(zs, steps)
	print(nz)
	print("Part 2:", math.lcm(nx, ny, nz))
	exit()

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
