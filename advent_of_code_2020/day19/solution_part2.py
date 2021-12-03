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
		self.debug = False
		# check for
		self.p11max = 0
		self.p08max = 0
		self.p11act = 0
		self.p08act = 0


	def checkr(self, rid, wused):
		"""
		check rule id
		"""
		if self.debug: print("working on rule {} -> {}, string used {}".format(rid, self.rules[rid], self.works[0:wused]))
		# check if at least one rule is OK
		
		ok = True
		checkrules = self.rules[rid]
		if rid == '8':
			# manual override of rule 8
			if self.p08act < self.p08max:
				checkrules = [['42', '8']]
				self.p08act += 1
			else:
				checkrules = [['42']]
		elif rid == '11':
			# manual override of rule 8
			if self.p11act < self.p11max:
				checkrules = [['42', '11', '31']]
				self.p11act += 1
			else:
				checkrules = [['42', '31']]
		for rule in checkrules:
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
		
		for i in range(0, len(string)):
			for j in range(0, len(string)):
				self.p11max = i
				self.p08max = j
				self.p11act = 0
				self.p08act = 0
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


#	for i in range(0, 22):
#		for j in range(0, 22):
#			obj.p11max = i
#			obj.p08max = j
#			obj.p11act = 0
#			obj.p08act = 0
#			print(i, j, obj.check('aaaaabbaabaaaaababaa', finalrule))
#			#print("  ", obj.p08act)
#			#print("  ", obj.p11act)
#
#	exit(1)
	

	for item in items:
		#res = check_string(rules, item, finalrule)

		res = obj.check(item, finalrule)
		print("{} = {}".format(item, res))
		if res:
			summ += 1

	print("Part 2: {}".format(summ))


	

#==============================================================================

main()

#EOF
