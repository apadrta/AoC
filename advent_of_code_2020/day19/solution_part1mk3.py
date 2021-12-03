#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 19A
"""

import argparse
import copy

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


class CheckString():
	"""
	class for checking strings
	"""

	def __init__(self, ruleset):
		"""
		constructor
		"""
		self.rules = ruleset		# all rules
		self.strchrs = ['a', 'b']	# string chars
		self.works = ''			# evaluated string
		#self.wused = 0			# actualy consumed part of string
		self.debug = True


	def checkr(self, rid, wused):
		"""
		check rule id
		"""
		if self.debug: print("working on rule {} -> {}, string used {}".format(rid, self.rules[rid], self.works[0:wused]))
		# check if at least one rule is OK
		
		ok = True
		for rule in self.rules[rid]:
			if self.debug: print("  checking rule {}".format(rule))
			# check if all parts of actual rule are ok
			ok = True
			cused = wused
			for r in rule: 
				if self.debug: print("    checking part {}".format(r))
				if r in self.strchrs:
					if cused >= len(self.works):
						ok = False
						break
					elif self.works[cused] == r:
						if self.debug: print("      char test OK")
						cused += 1
					else:
						if self.debug: print("      char test failed")
						ok = False
						break
				else:
					res, charconsumed = self.checkr(r, cused)
					cused = charconsumed
					if not res:
						# one of "and" rules broken, all broken
						if self.debug: print("      part invalid")
						ok = False
						break
			if ok:
				break
		return ok, cused


	def check(self, string, frule):
		"""
		check if string is complieng with final rule
		"""
		self.works = string
		ok, cused = self.checkr(frule, 0)
		if ok and cused == len(self.works):
			return True
		return False


#==============================================================================

def main():
	"""
	Main function
	"""

	# process args
	infile = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data]

	rules = {}
	i = 0
	for line in lines:
		if not line:
			break
		name, content = line.split(':')
		rules[name] = []
		values = content.split('|')
		for value in values:
			rules[name].append(value.strip().replace('"','').split(' '))
		i += 1

	items = lines[i+1:]

	obj = CheckString(rules)
	finalrule = '0'
	summ = 0

	#print(obj.check('aaaaabbaabaaaaababaa', finalrule))

	#exit(1)
	

	for item in items:
		#res = check_string(rules, item, finalrule)
		res = obj.check(item, finalrule)
		print("{} = {}".format(item, res))
		if res:
			summ += 1

	print("Part 1: {}".format(summ))


	# print("Part 2: {}".format(res))
	

#==============================================================================

main()

#EOF
