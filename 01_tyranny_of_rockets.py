# adventofcode 2019
# crushallhumans
# puzzle 1
# 12/1/2019

import sys
import math
import unittest

def rocket_equation(mass):
	return math.floor(mass/3) - 2

def fuel_req_incorporated(mass):
	total = rocket_equation(mass)
	n  = rocket_equation(total)
	while n > 0:
		total += n
		n = rocket_equation(n)
	return total

def puzzle_text():
	print("""

""")

class testCase(unittest.TestCase):
	def test_rocket_equation(self):
		self.assertEqual(
			rocket_equation(12),
			2
		)
		self.assertEqual(
			rocket_equation(14),
			2
		)
		self.assertEqual(
			rocket_equation(1969),
			654
		)
		self.assertEqual(
			rocket_equation(100756),
			33583
		)

	def test_fuel_req_incorporated(self):
		self.assertEqual(
			fuel_req_incorporated(12),
			2
		)
		self.assertEqual(
			fuel_req_incorporated(14),
			2
		)
		self.assertEqual(
			fuel_req_incorporated(1969),
			966
		)
		self.assertEqual(
			fuel_req_incorporated(100756),
			50346
		)

if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		module_mass = (0,12)	
		f = 0
		for i in (module_mass):
			f += fuel_req_incorporated(i)
		print (f)	

	print("done");

