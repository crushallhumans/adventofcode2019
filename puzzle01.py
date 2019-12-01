# adventofcode 2019
# crushallhumans
# puzzle 1
# 12/1/2019

# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

# For example:

# For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
# For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
# For a mass of 1969, the fuel required is 654.
# For a mass of 100756, the fuel required is 33583.
# The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

# What is the sum of the fuel requirements for all of the modules on your spacecraft?

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
	module_mass = (89822, 149236, 106135, 147663, 91417, 59765, 66470, 121156, 148632, 116660, 90316, 111666, 142111, 72595, 139673, 145157, 77572, 83741, 79815, 74693, 139077, 106066, 125817, 127827, 103884, 147289, 81588, 142651, 69916, 147214, 71501, 130067, 60182, 139195, 115502, 127751, 95013, 73411, 125294, 79809, 118110, 122547, 145141, 72231, 138853, 108119, 139960, 128665, 107228, 73416, 54608, 63811, 72363, 130546, 61055, 56786, 127718, 144953, 149284, 137318, 109566, 112866, 148063, 130570, 67536, 84011, 123795, 128098, 51687, 83758, 59867, 103122, 77339, 72126, 71446, 67162, 112342, 120248, 137629, 135736, 139781, 92512, 105922, 85458, 148571, 51173, 135047, 110175, 93722, 82611, 128288, 125225, 104177, 115081, 78470, 96167, 138445, 117778, 100133, 140047)	
	f = 0
	for i in (module_mass):
		f += fuel_req_incorporated(i)

	print (f)	
	print("done");