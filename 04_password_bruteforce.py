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
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle answer was 931.

--- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
How many different passwords within the range given in your puzzle input meet all of the criteria?

Your puzzle answer was 609.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your Advent calendar and try another puzzle.

Your puzzle input was 272091-815432.
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
		for i in range(272091,815432):
			if password_possible(str(i)):
				total += 1

		print(total)

	print("done");

