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

	def process_content(cont):
		"""
		process content
		"""
		res = 0
		lastsign = '+'

		plevel = 0
		part = []
		pstart = 0
		for i in range(0, len(cont)):
			if cont[i] == '(':
				plevel += 1
			elif cont[i] == ')':
				plevel -= 1
			if plevel == 1 and cont[i] == '(':
				pstart = i
			if plevel == 0 and cont[i] == ')':
				part = cont[pstart+1:i]
				#print(part)
				#process_content(part)
			if plevel == 0 :
				if cont[i] in ('+', '*'):
					lastsign = cont[i]
					#print("sign", lastsign)
				else:
					if part:
						lastnum = process_content(part)
						part = []
					else:
						lastnum = cont[i]
					#print("num", lastnum)
					if lastsign == '+':
						res = res + lastnum
					else:
						res = res * lastnum
					#print("res", res)
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
		#print(content)

		summ += process_content(content)

	print("Part 1:", summ)

#==============================================================================

main()

#EOF
