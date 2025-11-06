# adventofcode 2019
# crushallhumans
# puzzle 5 - intcode part 2
# 12/5/2019

import sys
import unittest
from functools import reduce 

#DEBUG = True
DEBUG = False

def process_instructions(instructions, inputt = -1):
	i = 0
	test_c = 1
	diag_code = -1
	num_instrux = len(instructions)

	if DEBUG: print (f"instructions: {instructions}")
	if DEBUG: print (f"inputt: {inputt}")

	try:
		jump = 999999
		while i < num_instrux:
			if DEBUG: print (f"\n{i}: {instructions[i:i+20]}...")

			opcode = instructions[i]
			if DEBUG: print (f"opcode: {opcode}")

			# handle exit
			if (opcode == 99):
				jump = 0
				if DEBUG: print (" ___ 99 ___ \n\n")
				return (diag_code,instructions)

			# handle opcode
			else:
				vals = []
				jump = 4

				# handle parameterized opcode
				# get operational values
				# set cursor jump value
				if (opcode > 99):
					s_opcode = str(opcode)
					jump = len(s_opcode)

					# handle leading zeroes for non-IO opcodes
					if jump == 3 and opcode != 104 and opcode != 103:
						s_opcode = f"0{s_opcode}"
						jump = len(s_opcode)

					num_params = jump - 2
					opcode = int(s_opcode[-2:])

					if not (9 > opcode > 0):
						raise Exception('bad opcode encoded: {s_opcode}')

					if DEBUG: print (f"opcode: {opcode}")
					if DEBUG: print (f"s_opcode: {s_opcode}")
					if DEBUG: print (f"s_opcode[-2:]: {s_opcode[-2:]}")
					if DEBUG: print (f"processed jump: {jump}")

					# process parameters starting from left of 0N
					for d in range(0,num_params):
						pos = -2-(d+1)
						param = int(s_opcode[pos])
						inner_idx = i+d+1
						idx = instructions[inner_idx]

						if DEBUG: print (f"pos: {pos}")
						if DEBUG: print (f"param: {param}")
						if DEBUG: print (f"inner_idx: {inner_idx}")

						# position mode
						if param == 0:
							if DEBUG: print (f"val posmode {idx}: {idx}")
							vals.append(instructions[idx])
						# immediate mode
						elif param == 1:
							if DEBUG: print (f"val immmode RAW: {idx}")
							vals.append(idx)


				# handle unparameterized opcode value collection
				if not len(vals):
					if DEBUG: print (f"plain opcode {opcode} getting val +1 at {i+1}")

					# input code is always immediate
					if opcode == 3:
						vals.append(instructions[i+1])
					else:
						vals.append(instructions[instructions[i+1]])

					# non-IO codes get a second value
					if (opcode != 3 and opcode != 4):
						if DEBUG: print (f"plain opcode {opcode} getting val +2 at {i+2}")
						vals.append(instructions[instructions[i+2]])


				#PROCESS OPCODES
				# jump codes
				if (opcode == 5 or opcode == 6):
					if DEBUG: print (f"vals op5/6: {vals}")
					jump = 3
					if (opcode == 5):
						if vals[0] != 0:
							if DEBUG: print (f"JUMP TO : {vals[1]}")
							i = vals[1]
							continue
						else:
							pass
					elif (opcode == 6):
						if vals[0] == 0:
							if DEBUG: print (f"JUMP TO : {vals[1]}")
							i = vals[1]
							continue
						else:
							pass

				# output code
				elif (opcode == 4):
					jump = 2
					if DEBUG: print (f"vals op4: {vals}")
					diag_code = vals[0]
					test_c += 1

				# input code
				elif (opcode == 3):
					jump = 2
					if DEBUG: print (f"vals op3: {vals}")
					instructions[vals[0]] = inputt
					if DEBUG: print (f"write pos: {vals[0]}")
					if DEBUG: print (f"write val: {inputt}")
						
				# operation codes
				elif (opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8):
					if DEBUG: print (f"vals op1/2/7/8: {vals}")
					result = -1
					if (opcode == 1):
						result = reduce((lambda x, y: x + y), vals)
					elif (opcode == 2):
						result = reduce((lambda x, y: x * y), vals)
					elif (opcode == 7):
						result = 1 if vals[0] < vals[1] else 0
					elif (opcode == 8):
						result = 1 if vals[0] == vals[1] else 0

					position = instructions[i+(jump-1)]
					instructions[position] = result

					if DEBUG: print (f"write pos: {position}")
					if DEBUG: print (f"write val: {result}")
				else:
					raise Exception('opcode not understood: ',opcode) 
			if DEBUG: print (f"jump: {jump}")
			i += jump
	except:
		raise Exception("Unknown exception")
	raise Exception("process_instructions finished organically")
	return False


class testCase(unittest.TestCase):
	def test_process_instructions(self):
		self.assertEqual(
			process_instructions([1,9,10,3,2,3,11,0,99,30,40,50])[1],
			[3500,9,10,70,2,3,11,0,99,30,40,50],
			"[1,9,10,3,2,3,11,0,99,30,40,50]"
		)
		self.assertEqual(process_instructions([1,0,0,0,99])[1], [2,0,0,0,99], [1,0,0,0,99])
		self.assertEqual(process_instructions([2,3,0,3,99])[1], [2,3,0,6,99], [2,3,0,3,99])
		self.assertEqual(process_instructions([2,4,4,5,99,0])[1], [2,4,4,5,99,9801], [2,4,4,5,99,0])
		self.assertEqual(process_instructions([1,1,1,4,99,5,6,0,99])[1], [30,1,1,4,2,5,6,0,99], [1,1,1,4,99,5,6,0,99])

		self.assertEqual(
			process_instructions([1002,4,3,4,33])[1], 
			[1002,4,3,4,99],
			"[1002,4,3,4,33]"
		)

		self.assertEqual(
			process_instructions([3,0,4,0,99],34939329)[0],
			34939329,
			"[3,0,4,0,99],34939329"
		)

		self.assertEqual(
			process_instructions(
				[3,9,8,9,10,9,4,9,99,-1,8],
				8
			)[0],
			1,
			"[3,9,8,9,10,9,4,9,99,-1,8],8"
		)

		self.assertEqual(
			process_instructions(
				[3,9,8,9,10,9,4,9,99,-1,8],
				3
			)[0],
			0,
			"[3,9,8,9,10,9,4,9,99,-1,8],3"
		)

		self.assertEqual(
			process_instructions(
				[3,3,1108,-1,8,3,4,3,99],
				8
			)[0],
			1,
			"[3,3,1108,-1,8,3,4,3,99],8"
		)

		self.assertEqual(
			process_instructions(
				[3,3,1108,-1,8,3,4,3,99],
				3
			)[0],
			0,
			"[3,3,1108,-1,8,3,4,3,99],3"
		)


		self.assertEqual(
			process_instructions(
				[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],
				0
			)[0],
			0,
			"[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],0"
		)
		self.assertEqual(
			process_instructions(
				[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],
				1291278
			)[0],
			1,
			"[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],1291278"
		)
		self.assertEqual(
			process_instructions(
				[3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
				0
			)[0],
			0,
			"[3,3,1105,-1,9,1101,0,0,12,4,12,99,1],0"
		)
		self.assertEqual(
			process_instructions(
				[3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
				3738281
			)[0],
			1,
			"[3,3,1105,-1,9,1101,0,0,12,4,12,99,1],3738281"
		)

		self.assertEqual(
			process_instructions(
				[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
				5
			)[0],
			999,
			"[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],5"
		)
		self.assertEqual(
			process_instructions(
				[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
				8
			)[0],
			1000,
			"[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],8"
		)
		self.assertEqual(
			process_instructions(
				[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
				7347289
			)[0],
			1001,
			"[3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],7347289"
		)





if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		instructions = [3,226]

		# test A/C (1)
		f = process_instructions(instructions.copy(),1)
		print (f[0])	

		print()
		# test Thermal Radiators (5)
		f = process_instructions(instructions.copy(),5)
		print (f[0])	

	print("done");




def puzzle_text():
	print("""
""")
