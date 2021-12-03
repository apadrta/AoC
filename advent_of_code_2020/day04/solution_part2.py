#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code - 4B
"""

import argparse

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

	# process args
	infile = get_args()

	# read data
	data = []
	with open(infile, "r") as fileh:
		data = fileh.readlines()
	lines = [x.strip() for x in data] + ['']

	item = {}
	valid = 0
	for line in lines:
		if not line:
			print(item)
			if len(item) == 8 or (len(item) == 7 and 'cid' not in item):
				hgtcheck = False
				if 'cm' in item['hgt'] or 'in' in item['hgt']:
					hval = int(item['hgt'][:-2])
					hmet = item['hgt'][-2:]
					if (hmet == 'cm' and hval >=150 and hval <=193) or (hmet == 'in' and hval >=59 and hval <=78):
						hgtcheck = True
						print('hmet OK')
				hclcheck = False
				if item['hcl'][0] == '#' and item['hcl'][1:].isalnum():
					hclcheck = True
					print('hlc OK')
				eclcheck = False
				if item['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
					eclcheck = True
					print('ecl OK')
				pidcheck = False
				if item['pid'].isdigit() and len(item['pid']) == 9:
					pidcheck = True
					print('pid OK')
				if (int(item['byr']) >= 1920 and int(item['byr']) <=2002) and (int(item['iyr']) >= 2010 and int(item['iyr']) <=2020) and (int(item['eyr']) >= 2020 and int(item['eyr']) <= 2030) and hgtcheck and hclcheck and eclcheck and pidcheck:		
					print('VALID')
					valid += 1
			item = {}
		else:
			parts = line.split(' ')
			for part in parts:
				key, value = part.split(':')
				item[key] = value

	print("Valid passports: {}".format(valid))
	



#==============================================================================

main()

#EOF
