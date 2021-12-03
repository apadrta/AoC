#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 18A
"""

import argparse
import string

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


def main():
	"""
	Main function
	"""

	def convert_content(cont):
		"""
		process content
		"""
		res = 0
		lastsign = '+'

		plevel = 0
		part = []
		pstart = 0
		newc = []
		for i in range(0, len(cont)):
			if cont[i] == '(':
				plevel += 1
			elif cont[i] == ')':
				plevel -= 1
			if plevel == 1 and cont[i] == '(':
				pstart = i
			if plevel == 0 and cont[i] == ')':
				part = convert_content(cont[pstart+1:i])
			if plevel == 0 :
				if part:
					newc.append(part)
					part = ''
				else:
					newc.append(cont[i])
		return newc

	def compute(arr):
		"""
		compute single array
		"""
		#print("compute in", arr)
		while '+' in arr:
			pos = arr.index('+')
			arr[pos] = arr[pos - 1] + arr [pos + 1]
			arr.pop(pos + 1)
			arr.pop(pos - 1)
		#print("compute out +", arr)
		while '*' in arr:
			pos = arr.index('*')
			arr[pos] = arr[pos - 1] * arr [pos + 1]
			arr.pop(pos + 1)
			arr.pop(pos - 1)
		#print("compute out *", arr)
		return arr[0]

	def evaluate_content(cont):
		"""
		evaluate content
		"""
		newc = []
		for c in cont:
			if type(c) is list:
				newc.append(evaluate_content(c))
			else:
				newc.append(c)
		#print("newc", newc)
		res = compute(newc)
		#print(res)
		return res

	# process args
	infile = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]

	summ = 0
	for line in lines:
		content = []
		lastdigit = False
		intstr = ''
		for c in line:
			if c.isdigit():
				intstr += c
				lastdigit = True
				#print("instr+ ", intstr)
			else:
				if lastdigit:
					content.append(int(intstr))
					#print("instr=", intstr)
					intstr = ''
				lastdigit = False
		
			if c in ('(', ')', '+', '*'):
				content.append(c)
				lastdigit = False

		if lastdigit:
			content.append(int(intstr))
		print(content)
		# convert to fields
		c2 = convert_content(content)
		print(c2)
		summ += evaluate_content(c2)
		
	print("Part 2:", summ)

#==============================================================================

main()

#EOF
