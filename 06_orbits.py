# adventofcode 2019
# crushallhumans
# puzzle 6 - orbits
# 12/6/2019

import sys
import unittest
from functools import reduce 

#DEBUG = True
DEBUG = False


def process_instructions(instructions):
	num_orbits = 0
	orbiter_map = dict()
	for i in instructions:
		sp = i.split(')')
		centerr = sp[0]
		orbiter = sp[1]
		if orbiter not in orbiter_map:
			orbiter_map[orbiter] = []
		orbiter_map[orbiter].append(centerr)

	if DEBUG: print(orbiter_map)
	runs = 0
	c = 0
	d = 1
	monitor = 10

	prior_num_orbits = 0
	while (c < 100000):
		num_orbits = 0
		for orbiter in orbiter_map.keys():
			orbits = orbiter_map[orbiter]
			if DEBUG: print(f"!--> {orbiter}: {orbits}")
			centerr = orbits[0]

			# ugh so bruteforce, couldn't get recursion to work
			#orbiter_map = recurse_count_indirects(orbiter, centerr, orbiter_map, 1)
			
			if centerr in orbiter_map:
				for i in orbiter_map[centerr]:
					if DEBUG: print(f"{orbiter} indirectly orbits {i}")
					if (i not in orbiter_map[orbiter]):
						orbiter_map[orbiter].append(i)

		for orbiter in orbiter_map.keys():
			num_orbits += len(orbiter_map[orbiter])

		if c and not c % monitor:
			if DEBUG: print (f"{c} runs, {num_orbits} orbits")

		if num_orbits != prior_num_orbits:
			prior_num_orbits = num_orbits
		else:
			break

		c += 1

	if DEBUG: print (orbiter_map)

	return (orbiter_map,num_orbits)

def shortest_path(instructions, two_points, saved_map = None):
	orbiter_map = saved_map or process_instructions(instructions)[0]

	path_a = orbiter_map[two_points[0]]
	path_b = orbiter_map[two_points[1]]
	shortest_length = 0

	a_depth = 0
	paths = set()
	for i in path_a:
		if DEBUG: print (f"testing A node {i} at {a_depth}")
		if i in path_b:
			b_depth = path_b.index(i)
			if DEBUG: print (f"\t B node {i} present at {b_depth}")
			paths.add(b_depth + a_depth)
			break
		a_depth += 1

	if len(paths):
		shortest_length = sorted(paths)[0]

	return (paths, shortest_length)




class testCase(unittest.TestCase):
	def test_process_instructions(self):
		self.assertEqual(
			process_instructions(
				['COM)B',
				'B)C',
				'C)D',
				'D)E',
				'E)F',
				'B)G',
				'G)H',
				'D)I',
				'E)J',
				'J)K',
				'K)L']
			)[1],
			42
		)

		self.assertEqual(
			shortest_path(
				['COM)B',
				'B)C',
				'C)D',
				'D)E',
				'E)F',
				'B)G',
				'G)H',
				'D)I',
				'E)J',
				'J)K',
				'K)L',
				'K)YOU',
				'I)SAN'],
				('YOU','SAN')
			)[1],
			4	
		)




if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		instructions = []
		SAVED_PATH_MAP = {}
		# find all orbits
		f = process_instructions(instructions.copy())
		print (f)	

		# find shortest path
		f = shortest_path(instructions.copy(), ('YOU', 'SAN'), f[0])
		print (f)


	print("done");




def puzzle_text():
	print("""
""")
