# adventofcode 2019
# crushallhumans
# puzzle 2
# 12/2/2019

import sys
import math
import unittest
import random
import itertools

def process_instructions(instructions):
	i = 0
	num_instrux = len(instructions)
	try:
		while i < num_instrux:
			opcode = instructions[i]
			if (opcode == 99):
				return instructions
			elif (3 > opcode > 0):
				val1 = instructions[instructions[i+1]]
				val2 = instructions[instructions[i+2]]
				result = -1
				if (opcode == 1):
					result = val1 + val2
				elif (opcode == 2):
					result = val1 * val2
				position = instructions[i+3]
				if (result < 0):
					raise Exception('improper result: ',result,itertools.islice(i,i+4))
				instructions[position] = result
			else:
				raise Exception('opcode not understood: ',opcode) 
			i += 4
	except:
		raise Exception("Unknown exception")
	raise Exception("process_instructions finished organically")
	return False

def puzzle_text():
	print("""

""")

class testCase(unittest.TestCase):
	def test_process_instructions(self):
		self.assertEqual(
			process_instructions([1,9,10,3,2,3,11,0,99,30,40,50]),
			[3500,9,10,70,2,3,11,0,99,30,40,50]
		)
		self.assertEqual(process_instructions([1,0,0,0,99]), [2,0,0,0,99])
		self.assertEqual(process_instructions([2,3,0,3,99]), [2,3,0,6,99])
		self.assertEqual(process_instructions([2,4,4,5,99,0]), [2,4,4,5,99,9801])
		self.assertEqual(process_instructions([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		instructions = [0]	
		modified_instructions = instructions.copy()
		# replace position 1 with the value 12 and replace position 2 with the value 2
		modified_instructions[1] = 12
		modified_instructions[2] = 2
		f = process_instructions(modified_instructions)
		print (f)	

		c = 0
		d = 1
		monitor = 1000
		limit = 5 * 1000000 #5M
		rrange = 100
		comblimit = rrange*(rrange-1)
		print ("begin finder run, ",comblimit)
		combinations_tried = {}
		while modified_instructions[0] != 19690720 and len(combinations_tried) < (comblimit):
			c += 1
			noun = random.randrange(0,100)
			verb = random.randrange(0,100)
			key = f"{verb}-{noun}"

			if (key in combinations_tried):
				continue

			d += 1
			combinations_tried[key] = True

			if c and not c % monitor:
				print ("%i runs",c)
			if c > limit:
				break

			modified_instructions = instructions.copy()
			modified_instructions[1] = noun
			modified_instructions[2] = verb
			modified_instructions = process_instructions(modified_instructions)

	print(modified_instructions)
	print (f"eval'd {c} permutations, ran {d} programs")
	print("done");

