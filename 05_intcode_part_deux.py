# adventofcode 2019
# crushallhumans
# puzzle 4
# 12/2/2019

import sys
import math
import unittest
import random
import itertools
from functools import reduce 

DEBUG = True

def process_instructions(instructions, inputt = 0):
	i = 0
	if DEBUG: print (f"instructions: {instructions}")
	num_instrux = len(instructions)
	try:
		jump = 999999
		while i < num_instrux:
			if DEBUG: print (f"\n{instructions[i:i+7]}...")
			opcode = instructions[i]
			if DEBUG: print (f"opcode: {opcode}")
			if (opcode == 99):
				jump = 0
				return instructions
			else:
				vals = []
				if (opcode > 99):
					s_opcode = str(opcode)
					jump = len(s_opcode)
					num_params = jump - 2
					opcode = int(s_opcode[-2:])
					if DEBUG: print (f"jump: {jump}")
					if DEBUG: print (f"opcode: {opcode}")
					if DEBUG: print (f"s_opcode[-2:]: {s_opcode[-2:]}")
					for d in range(0,num_params):
						pos = -2-(d+1)
						if DEBUG: print (f"pos: {pos}")
						param = int(s_opcode[pos])
						if DEBUG: print (f"param: {param}")
						idx = instructions[i+d+1]
						if DEBUG: print (f"idx: {idx}")
						if param == 0:
							vals.append(instructions[idx])
						elif param == 1:
							vals.append(idx)
				else:
					jump = 4

				if (opcode == 3 or opcode == 4):
					jump = 2
					idx = instructions[i+1]
					if DEBUG: print (f"io idx: {idx}")
					val1 = instructions[idx]
					if DEBUG: print (f"io val1: {val1}")
					if (opcode == 3):
						instructions[idx] = inputt
					elif (opcode == 4):
						print(f"----> OPCODE4: {instructions[idx]}")
						
				elif (opcode == 1 or opcode == 2):
					if not len(vals):
						vals.append(instructions[instructions[i+1]])
						vals.append(instructions[instructions[i+2]])
					if DEBUG: print (f"vals: {vals}")
					result = -1
					if (opcode == 1):
						result = reduce((lambda x, y: x + y), vals)
					elif (opcode == 2):
						result = reduce((lambda x, y: x * y), vals)
					position = instructions[i+(jump-1)]
					if DEBUG: print (f"write pos: {position}")
					instructions[position] = result
				else:
					raise Exception('opcode not understood: ',opcode) 
			i += jump
	except:
		raise Exception("Unknown exception")
	raise Exception("process_instructions finished organically")
	return False

def puzzle_text():
	print("""
--- Day 2: 1202 Program Alarm ---
On the way to your gravity assist around the Moon, your ship computer beeps angrily about a "1202 program alarm". On the radio, an Elf is already explaining how to handle the situation: "Don't worry, that's perfectly norma--" The ship computer bursts into flames.

You notify the Elves that the computer's magic smoke seems to have escaped. "That computer ran Intcode programs like the gravity assist program it was working on; surely there are enough spare parts up there to build a new Intcode computer!"

An Intcode program is a list of integers separated by commas (like 1,0,0,3,99). To run one, start by looking at the first integer (called position 0). Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to do; for example, 99 means that the program is finished and should immediately halt. Encountering an unknown opcode means something went wrong.

Opcode 1 adds together numbers read from two positions and stores the result in a third position. The three integers immediately after the opcode tell you these three positions - the first two indicate the positions from which you should read the input values, and the third indicates the position at which the output should be stored.

For example, if your Intcode computer encounters 1,10,20,30, it should read the values at positions 10 and 20, add those values, and then overwrite the value at position 30 with their sum.

Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.

Once you're done processing an opcode, move to the next one by stepping forward 4 positions.

For example, suppose you have the following program:

1,9,10,3,2,3,11,0,99,30,40,50
For the purposes of illustration, here is the same program split into multiple lines:

1,9,10,3,
2,3,11,0,
99,
30,40,50
The first four integers, 1,9,10,3, are at positions 0, 1, 2, and 3. Together, they represent the first opcode (1, addition), the positions of the two inputs (9 and 10), and the position of the output (3). To handle this opcode, you first need to get the values at the input positions: position 9 contains 30, and position 10 contains 40. Add these numbers together to get 70. Then, store this value at the output position; here, the output position (3) is at position 3, so it overwrites itself. Afterward, the program looks like this:

1,9,10,70,
2,3,11,0,
99,
30,40,50
Step forward 4 positions to reach the next opcode, 2. This opcode works just like the previous, but it multiplies instead of adding. The inputs are at positions 3 and 11; these positions contain 70 and 50 respectively. Multiplying these produces 3500; this is stored at position 0:

3500,9,10,70,
2,3,11,0,
99,
30,40,50
Stepping forward 4 more positions arrives at opcode 99, halting the program.

Here are the initial and final states of a few more small programs:

1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.
Once you have a working computer, the first step is to restore the gravity assist program (your puzzle input) to the "1202 program alarm" state it had just before the last computer caught fire. To do this, before running the program, replace position 1 with the value 12 and replace position 2 with the value 2. What value is left at position 0 after the program halts?

Your puzzle answer was 4484226.

--- Part Two ---
"Good, the new computer seems to be working correctly! Keep it nearby during this mission - you'll probably use it again. Real Intcode computers support many more features than your new one, but we'll let you know what they are as you need them."

"However, your current priority should be to complete your gravity assist around the Moon. For this mission to succeed, we should settle on some terminology for the parts you've already built."

Intcode programs are given as a list of integers; these values are used as the initial state for the computer's memory. When you run an Intcode program, make sure to start by initializing memory to the program's values. A position in memory is called an address (for example, the first value in memory is at "address 0").

Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values used immediately after an opcode, if any, are called the instruction's parameters. For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3, and 4 are the parameters. The instruction 99 contains only an opcode and has no parameters.

The address of the current instruction is called the instruction pointer; it starts at 0. After an instruction finishes, the instruction pointer increases by the number of values in the instruction; until you add more instructions to the computer, this is always 4 (1 opcode + 3 parameters) for the add and multiply instructions. (The halt instruction would increase the instruction pointer by 1, but it halts the program instead.)

"With terminology out of the way, we're ready to proceed. To complete the gravity assist, you need to determine what pair of inputs produces the output 19690720."

The inputs should still be provided to the program by replacing the values at addresses 1 and 2, just like before. In this program, the value placed in address 1 is called the noun, and the value placed in address 2 is called the verb. Each of the two input values will be between 0 and 99, inclusive.

Once the program has halted, its output is available at address 0, also just like before. Each time you try a pair of inputs, make sure you first reset the computer's memory to the values in the program (your puzzle input) - in other words, don't reuse memory from a previous attempt.

Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)

Your puzzle answer was 5696.

(Final program state was: 
	[19690720, 56, 96, 2, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 6, 1, 112, 1, 5, 19, 113, 2, 6, 23, 226, 1, 27, 5, 227, 2, 9, 31, 681, 1, 5, 35, 682, 2, 6, 39, 1364, 2, 6, 43, 2728, 1, 5, 47, 2729, 2, 9, 51, 8187, 1, 5, 55, 8188, 1, 10, 59, 8192, 1, 63, 6, 8194, 1, 9, 67, 8197, 1, 71, 6, 8199, 1, 75, 13, 8204, 2, 79, 13, 41020, 2, 9, 83, 123060, 1, 87, 5, 123061, 1, 9, 91, 123064, 2, 10, 95, 492256, 1, 5, 99, 492257, 1, 103, 9, 492260, 1, 13, 107, 492265, 2, 111, 10, 1969060, 1, 115, 5, 1969061, 2, 13, 119, 9845305, 1, 9, 123, 9845308, 1, 5, 127, 9845309, 2, 131, 6, 19690618, 1, 135, 5, 19690619, 1, 139, 6, 19690621, 1, 143, 6, 19690623, 1, 2, 147, 19690719, 1, 151, 5, 0, 99, 2, 14, 0, 0]
)

Both parts of this puzzle are complete! They provide two gold stars: **
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

		self.assertEqual(process_instructions(
			[1002,4,3,4,33]), 
			[1002,4,3,4,99]
		)

		self.assertEqual(process_instructions(
			[3,0,4,0,99],34939329)[0],
			34939329
		)

if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		instructions = [3,225,1,225,6,6,1100,1,238,225,104,0,1001,191,50,224,101,-64,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,2,150,218,224,1001,224,-1537,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1002,154,5,224,101,-35,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,1102,76,17,225,1102,21,44,224,1001,224,-924,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,101,37,161,224,101,-70,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,102,46,157,224,1001,224,-1978,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,5,29,225,1101,10,7,225,1101,43,38,225,1102,33,46,225,1,80,188,224,1001,224,-73,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,52,56,225,1101,14,22,225,1101,66,49,224,1001,224,-115,224,4,224,1002,223,8,223,1001,224,7,224,1,224,223,223,1101,25,53,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,226,226,224,1002,223,2,223,1005,224,329,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,8,677,677,224,102,2,223,223,1006,224,359,101,1,223,223,7,226,677,224,102,2,223,223,1005,224,374,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,389,101,1,223,223,7,677,226,224,1002,223,2,223,1006,224,404,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,419,1001,223,1,223,1007,226,226,224,102,2,223,223,1005,224,434,101,1,223,223,1008,226,677,224,102,2,223,223,1005,224,449,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,1008,226,226,224,102,2,223,223,1006,224,479,101,1,223,223,1007,226,677,224,1002,223,2,223,1005,224,494,1001,223,1,223,108,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,554,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,569,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,1008,677,677,224,102,2,223,223,1005,224,599,1001,223,1,223,1107,677,677,224,102,2,223,223,1006,224,614,101,1,223,223,7,226,226,224,102,2,223,223,1005,224,629,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,644,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,659,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226]	
		f = process_instructions(instructions,1)
		print (f)	


	# 	c = 0
	# 	d = 1
	# 	monitor = 1000
	# 	limit = 5 * 1000000 #5M
	# 	rrange = 100
	# 	comblimit = rrange*(rrange-1)
	# 	print ("begin finder run, ",comblimit)
	# 	combinations_tried = {}
	# 	while modified_instructions[0] != 19690720 and len(combinations_tried) < (comblimit):
	# 		c += 1
	# 		noun = random.randrange(0,100)
	# 		verb = random.randrange(0,100)
	# 		key = f"{verb}-{noun}"

	# 		if (key in combinations_tried):
	# 			continue

	# 		d += 1
	# 		combinations_tried[key] = True

	# 		if c and not c % monitor:
	# 			print ("%i runs",c)
	# 		if c > limit:
	# 			break

	# 		modified_instructions = instructions.copy()
	# 		modified_instructions[1] = noun
	# 		modified_instructions[2] = verb
	# 		modified_instructions = process_instructions(modified_instructions)

	# print(modified_instructions)
	# print (f"eval'd {c} permutations, ran {d} programs")
	print("done");

