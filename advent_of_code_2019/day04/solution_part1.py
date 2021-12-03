#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 4A
"""

import argparse

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
		checkdouble = False
		last = istr[0]
		for c in istr[1:]:
			if c == last:
				checkdouble = True
				break
			last = c
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
