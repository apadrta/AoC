#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 8A
"""

import argparse
from math import floor
import numpy as np
from PIL import Image


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


def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read data
	rdata = []
	with open(infile, "r") as fileh:
		rdata = fileh.readlines()

	data = [x.strip() for x in rdata]

	pixels = []
	for line in data:
		for c in line:
			pixels.append(int(c))

	width = 25
	height = 6

	layers = int(len(pixels) / width / height)
	
	minval = width * height
	minlayer = 0
	visible = [2] * minval
	for i in range(0, layers):
		curlayer = pixels[i*width*height:(i+1)*width*height]
		#print(curlayer)
		zeros = curlayer.count(0)
		if zeros < minval:
			minval = zeros
			minlayer = i
		for j in range(0, width * height):
			if visible[j] == 2:
				visible[j] = curlayer[j]

	layerdata = pixels[minlayer*width*height:(minlayer+1)*width*height]
	print("part1: {}".format(layerdata.count(1)*layerdata.count(2)))

	#visible = [str(x).replace('1', '*').replace('0', '') for x in visible]
	arr = np.array(visible)
	arr = arr.reshape(height, width)
	im = Image.fromarray(arr.astype('uint8')*255)
	print("Check file part2.png")
	im.save("part2.png")
	print(arr)

	#print("part2: {}".format(len(youpath[(i-1)::]) + len(sanpath[(i-1)::]) - 2))








#==============================================================================

main()

#EOF
