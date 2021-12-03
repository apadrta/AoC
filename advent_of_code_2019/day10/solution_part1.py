#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 10A
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
		self.asteroids = []
		self.sensorpos = None

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
				val = 0	# space
				if data[y][x] == '#':
					val = 1 # asteroid
					self.asteroids.append((x, y))
				self.arr[(x, y)] = val
				x += 1
			y += 1

	def visible(self, pos):
		"""
		count visible asteroids
		"""
		diffs = []
		for ast in self.asteroids:
			if ast != pos:
				xdiff = ast[0]-pos[0]
				ydiff = ast[1]-pos[1]
				xygcd = math.gcd(xdiff, ydiff)
				if xygcd != 0:
					xdiff = xdiff / xygcd
					ydiff = ydiff / xygcd
				diff = (xdiff, ydiff)
				#print(diff)
				if diff not in diffs:
					#print("  +")
					diffs.append(diff)
		return diffs


	def best_sensor(self):
		"""
		find best place for sensor
		"""
		best = 0
		bestpos = (0, 0)
		for pos in self.asteroids:
			curr = len(self.visible(pos))
			if curr > best:
				best = curr
				bestpos = pos
		self.sensor = bestpos
		return bestpos, best


	def fire(self, sensor, direction):
		"""
		target asteroid in given direction
		"""
		#print("ION cannon at {} targeting in direction {} ...".format(sensor, direction))
		x = int(sensor[0] + direction[0])
		y = int(sensor[1] + direction[1])
		while x >= 0 and x < self.maxx and y >= 0 and y < self.maxy:
			if self.arr[(x, y)] == 1:
				self.arr[(x, y)] = 9
				#print("  Asteorid vaporized at {}".format((x, y)))
				#print(self.arr.transpose())
				self.arr[(x, y)] = 4
				return True, (x, y)
			x += int(direction[0])
			y += int(direction[1])
		#print("  nothing to vaporize")
		return False, (0, 0)



	def vaporize(self):
		"""
		start vaporizing the asteroids
		"""

		#self.sensor = (8, 3)
		firediff = self.visible(self.sensor)
		self.arr[(self.sensor)] = 9

		# compute fire orders
		xvals = sorted(list(set([int(x[0]) for x in firediff])))
		yvals = sorted(list(set([int(x[1]) for x in firediff])))

		angles = {}
		for f in firediff:
			x = int(f[0])
			y = int(f[1])
			if x == 0 and y < 0:
				# up
				angle = 0.0
			elif x > 0 and y < 0:
				# right up
				angle = pi/2 - math.atan(abs(y)/abs(x))
			elif x > 0 and y ==  0:
				# right
				angle = pi/2
			elif x > 0 and y > 0:
				# right down
				angle = pi/2 + math.atan(abs(y)/abs(x))
			elif x == 0 and y > 0:
				# down
				angle = pi
			elif x < 0 and y > 0:
				# left down
				angle = 3/2 * pi - math.atan(abs(y)/abs(x))
			elif x < 0 and y == 0:
				# left
				angle = 3/2 * pi				
			elif x < 0 and y < 0:
				# left up
				angle = 3/2*pi + math.atan(abs(y)/abs(x))
			angles[angle] = f
		hits = 0
		result = -1
		while hits < len(self.asteroids) - 1:
			for angle in sorted(angles):
				res, target = self.fire(self.sensor, angles[angle])
				if res:
					hits += 1
					#print("{}. hit at {}".format(hits, target))
					if hits == 200:
						result = target[0]*100 + target[1]
		
		return result



def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	obj = Seats()
	obj.read(infile)
	res = obj.best_sensor()
	print("Part 1: {} at position {}".format(res[1], res[0]))

	res = obj.vaporize()
	print("Part 2: {}".format(res))
	#print(obj.arr.transpose())
	#obj.arr[(1,0)] = '9'
	#print(obj.arr.transpose())
	#print(obj.asteroids)
	#print(obj.visible((4,2)))
	#pos = (1,1)
	#print(obj.adjanced(pos))
	#obj.eval_round()
	#print(obj.adjanced(pos))
	#print("Part 2: {}".format(obj.find_stable()))


#==============================================================================

main()

#EOF
