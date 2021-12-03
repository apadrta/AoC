#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 14A
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


def ore_required(lines, finaly, finalyn):
	"""
	compute how much ore is needed for product "finaly" in ammount "finalyn"
	"""

	# read rules
	rules = {}
	waste = {}
	for line in lines:
		raw, out = line.split(' => ')
		outn, outi = out.split(' ')
		desc = [int(outn), []]
		pre = raw.split(', ')
		for p in pre:
			n, i = p.split(' ')
			desc[1].append([i, int(n)])
		if outi not in rules:
			rules[outi] = desc
			waste[outi] = 0
	
	primary = 'ORE'

	waste[primary] = 0
	done = {finaly: finalyn}
	#print(rules)
	#print(waste)
	while True:
		for key, rule in rules.items():
			for item in done:
				if key == item:
					outn = done.pop(key)
					spare = 0
					if waste[key] > 0:
						if waste[key] > outn:
							spare = outn
							waste[key] -= outn
						else:
							spare = waste[key]
							waste[key] = 0
					#print("working on {}".format(key))
					#print("  required amount: {}".format(outn))
					#print("  spare - taken from waste:", spare)
					#print("  required to produce:", outn - spare)
					outn = outn - spare

					#print("  producing rule", rule)
					repeats = math.ceil(outn / rule[0])
					#print("  number of repeats:", repeats)
					store = repeats * rule[0] - outn
					waste[key] += store
					#print("  waste stored:", store)
					for r in rule[1]:
						#print("  new prerequisity ", r)
						#print("    required inputs", repeats * r[1] )
						if r[0] not in done:
							done[r[0]] = 0
						done[r[0]] += repeats * r[1]

					#print("  =>", done)
					#print("  => waste", waste)
					break
		if len(done) == 1:
			break
	return done['ORE']

# =============================================================================

def main():
	"""
	Main function
	"""

	# process args
	filename = get_args()

	data = []
	with open(filename, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]


	oren = ore_required(lines, 'FUEL', 1)


	print("Part 1:", oren)


	total = 1000000000000

	minn = math.floor(total / oren)
	maxn = math.floor(3* total / oren)
	mintotal = ore_required(lines, 'FUEL', minn)
	maxtotal = ore_required(lines, 'FUEL', maxn)

	diff = 0
	lastdiff = -1
	while True:

		midn = math.floor((maxn + minn) / 2)
		midtotal = ore_required(lines, 'FUEL', midn)

		if midtotal > total:
			maxn = midn
		if midtotal < total:
			minn = midn

		lastdiff = diff
		diff = abs(midtotal - total)
		#print(midn, midtotal)
		#print("diff", diff, lastdiff)
		if diff == lastdiff:
			break


	print("Part 2: {}".format(midn))


#==============================================================================

main()

#EOF
