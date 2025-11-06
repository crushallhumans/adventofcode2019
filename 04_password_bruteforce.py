# adventofcode 2019
# crushallhumans
# puzzle 4 - password bruteforce
# 12/4/2019

import sys
import math
import unittest
import random
import itertools

def password_possible(password):
	if len(password) != 6:
		return False
	adjacency = False
	prior = 0
	groups = {}
	for i in password:
		ii = int(i)
		if i not in groups:
			groups[i] = 0
		if ii < prior:
			return False
		if ii == prior:
			groups[i] += 1
		prior = ii

	for k in groups:
		if groups[k] == 1:
			adjacency = True
	return adjacency


def puzzle_text():
	print("""
""")

class testCase(unittest.TestCase):
	def test_main_function(self):
		self.assertEqual(
			password_possible('111111'),
			False,
			'111111'
		)
		self.assertEqual(
			password_possible('223450'),
			False,
			'223450'
		)
		self.assertEqual(
			password_possible('123789'),
			False,
			'123789'
		)
		self.assertEqual(
			password_possible('112233'),
			True,
			'112233'
		)
		self.assertEqual(
			password_possible('123444'),
			False,
			'123444'
		)
		self.assertEqual(
			password_possible('111122'),
			True,
			'111122'
		)


if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		print ("go")
		total = 0
		for i in range(1,2):
			if password_possible(str(i)):
				total += 1

		print(total)

	print("done");

