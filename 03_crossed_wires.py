# adventofcode 2019
# crushallhumans
# puzzle 3 - crossed wires
# 12/3/2019

import sys
import math
import unittest
import random
import itertools

def get_closest_crossing(route1,route2):
	route_map = [[], []]
	route_steps_map = [{}, {}]
	r = 0
	max_coord = [0,0]
	min_coord = [0,0]
	for route in ([route1,route2]):
		origin = {'x': 0, 'y': 0}
		route_set = set() 
		steps = 1
		for i in (route):
			inner_set = set()
			vec = i[0]
			atk = int(i[1:])
			#print(f"{vec},{atk}")

			origin_idx = 'fail'
			opposed_vec = 'fail'
			multiplier = 1
			if (vec == 'R' or vec == 'L'):
				origin_idx = 'x'
				opposed_vec = origin['y']
				if (vec == 'L'):
					multiplier = -1
			elif (vec == 'U' or vec == 'D'):
				origin_idx = 'y'
				opposed_vec = origin['x']
				if (vec == 'D'):
					multiplier = -1
			else:
				raise Exception("Bad vector: ", vec)

			# print(f"origin_idx: {origin_idx}")
			# print(f"origin[origin_idx]: {origin[origin_idx]}")
			# print(f"opposed_vec: {opposed_vec}")
			# print(f"multiplier: {multiplier}")
			# print(f"atk: {atk}")

			for i in range(0, atk):
				# print(f"i: {i}, c: {origin[origin_idx]}")

				origin[origin_idx] += (multiplier * 1)

				if (origin_idx) == 'x':
					key = (origin[origin_idx],opposed_vec)
					if origin[origin_idx] > max_coord[0]:
						max_coord[0] = origin[origin_idx]
					if origin[origin_idx] < min_coord[0]:
						min_coord[0] = origin[origin_idx]
				else:
					key = (opposed_vec,origin[origin_idx])
					if origin[origin_idx] > max_coord[1]:
						max_coord[1] = origin[origin_idx]
					if origin[origin_idx] < min_coord[1]:
						min_coord[1] = origin[origin_idx]
				if key not in inner_set:
					inner_set.add(key)
					route_steps_map[r][key] = steps

				steps += 1

			# print(inner_set)
			for i in inner_set:
				if i not in route_set:
					route_set.add(i)

		route_map[r] = route_set
		r += 1
	# print(route_map)
	# print(max_coord)
	# print (route_map[0].intersection(route_map[1]))

	lowest_manhattan_distance = 9999999
	lowest_steps = 99999999
	mark_tuple = (0,0)
	for i in route_map[0].intersection(route_map[1]):
		manhattan_distance = abs(i[0]) + abs(i[1])
		steps = route_steps_map[0][i] + route_steps_map[1][i]
		# print(f"manhattan_distance: {manhattan_distance}")
		if manhattan_distance < lowest_manhattan_distance:
			lowest_manhattan_distance = manhattan_distance
			mark_tuple = (i[0], i[1])
		if steps < lowest_steps:
			lowest_steps = steps


	if __name__ != '__main__':
		print(route_map)
		for i in range(max_coord[1]+1,min_coord[1]-1,-1):
			for j in range(min_coord[0],max_coord[0]+1):
				if (j,i) in route_map[0] or (j,i) in route_map[1]:
					n = '1'
					if (j,i) in route_map[1]:
						n = '2'
					if (j,i) in route_map[0] and (j,i) in route_map[1]:
						t = '!'
						if (j,i) == mark_tuple:
							t = '$'
						print(t, end = '')
					else:
						print(n, end = '')
				else:
					x = ' '
					if (j,i) == (0,0):
						x = '*'
					print(x, end = '')
			print("")
		print("")

	return (lowest_manhattan_distance, lowest_steps)



def puzzle_text():
	print("""

""")

class testCase(unittest.TestCase):
	def test_main_function(self):
		self.assertEqual(
			get_closest_crossing(['R8','U5','L5','D3'],['U7','R6','D4','L4'])[0],
			6
		)
		self.assertEqual(
			get_closest_crossing(
				['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
				['U62','R66','U55','R34','D71','R55','D58','R83']
			)[0]
			,159
		)
		self.assertEqual(
			get_closest_crossing(
				['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
				['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
			)[0]
			,135
		)
	def test_secondary_function(self):
		self.assertEqual(
			get_closest_crossing(['R8','U5','L5','D3'],['U7','R6','D4','L4'])[1],
			30
		)
		self.assertEqual(
			get_closest_crossing(
				['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
				['U62','R66','U55','R34','D71','R55','D58','R83']
			)[1]
			,610
		)
		self.assertEqual(
			get_closest_crossing(
				['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
				['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
			)[1]
			,410
		)
if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		wire1 = []
		wire2 = []
		f = get_closest_crossing(wire1, wire2)
		print (f)	

	print("done");

