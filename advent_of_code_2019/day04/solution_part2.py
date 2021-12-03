#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 4A
"""

import argparse

#==============================================================================

def checkdoublestr(istr):
	"""
	check elf single double :)
	"""
	last = istr[0]
	lastlen = 1
	for c in istr[1:]:
		if c == last:
			lastlen +=1
		else:
			if lastlen == 2:
				return True
			else:
				lastlen = 1
		last = c

	if lastlen == 2:
		return True

	return False

#==============================================================================

def main():
	"""
	Main function
	"""

	char = '372304-847060'
	minlim, maxlim = char.split('-')
	minlim = int(minlim)
	maxlim = int(maxlim)

	i = minlim
	valid = 0
	while i <= maxlim:
		istr = str(i)
		checkdouble = checkdoublestr(istr)
		checkdecrease = True
		last = istr[0]
		for c in istr[1:]:
			if c < last:
				checkdecrease = False
				break
			last = c
		
		if checkdouble and checkdecrease:
			valid += 1
		i += 1

	print(valid)

#==============================================================================

main()

#EOF
