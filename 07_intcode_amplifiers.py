# adventofcode 2019
# crushallhumans
# puzzle 7 - intcode amplifiers
# 12/7/2019

import sys
import unittest
from functools import reduce 
from itertools import permutations 

#DEBUG = True
DEBUG = False

def run_phase_sequence(program, sequence, feedback_mode = False):
	inp = 0
	if DEBUG: print (f"program: {program}")
	if DEBUG: print (f"sequence: {sequence}")
	program_states = dict()
	repeat_sequence = True
	seq_len = len(sequence)
	d = 0

	while repeat_sequence:
		if DEBUG: print (f"d: {d}")
		if DEBUG: print (f"seq_len: {seq_len}")
		i = sequence[d]
		if DEBUG: print (f"seq i: {i}")
		if DEBUG: print (f"inp: {inp}")
		inner_program = program.copy()
		inputs = [i,inp]
		instruction_position = 0
		if i in program_states:
			inner_program = program_states[i][0].copy()
			instruction_position = program_states[i][1]
			inputs = inp
		else:
			program_states[i] = []
		full_output = process_instructions(inner_program, inputs, feedback_mode, instruction_position)
		out = full_output[0]
		if DEBUG: print (f"out: {out}")
		inp = out

		d += 1
		if feedback_mode:
			if DEBUG: print (f"feedback mode is recent output feedback?: {full_output[2]}")
			if full_output[2]: #feedback pause/halt
				program_states[i] = [
					full_output[1].copy(),	#instruction set
					full_output[3], 		#instruction pointer
					full_output[0]			#most recent return val
				]
			else: #natural program halt
				if d >= seq_len:
					#if we halt on the final sequence in feedback mode, return
					repeat_sequence = False
					if out == -1:
						out = program_states[sequence[seq_len-1]][2]
			if d >= seq_len:
				d = 0
		else:
			if d >= seq_len:
				repeat_sequence = False
	return out

def process_instructions(instructions, inputs = (), feedback_mode = False, instruction_position = 0):
	i = instruction_position
	test_c = 1
	diag_code = -1
	outputs = []
	num_instrux = len(instructions)
	if type(inputs) is not list:
		x = list()
		x.append(inputs)
		inputs = x

	if DEBUG: print (f"instructions: {instructions}")
	if DEBUG: print (f"inputs: {inputs}")

	try:
		jump = 999999
		opcode = None
		while i < num_instrux:
			if DEBUG: print (f"\n{i}: {instructions[i:i+20]}...")

			is_feedback = False
			if opcode == 'FEEDBACK': #feedback signal
				opcode = 99
				is_feedback = True
			else:
				opcode = instructions[i]
			if DEBUG: print (f"opcode: {opcode}")

			# handle exit
			if (opcode == 99):
				jump = 0
				if len(outputs) == 1:
					diag_code = outputs[0]
				elif not len(outputs):
					diag_code = -1
				else:
					diag_code = outputs
				if DEBUG: print (f" _ {diag_code} _")
				if DEBUG: print (" ___ 99 ___ \n")
				return (diag_code, instructions, is_feedback, i)

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
					outputs.append(vals[0])
					test_c += 1
					if feedback_mode:
						if DEBUG: print (f"pause and feedback?: {instructions[i + jump]}")
						if instructions[i + jump] != 99:
							opcode = "FEEDBACK"
							i += jump
							continue

				# input code
				elif (opcode == 3):
					jump = 2
					if DEBUG: print (f"vals op3: {vals}")
					if (len(inputs)):
						instructions[vals[0]] = inputs.pop(0)
					elif (len(outputs)):
						feedback = outputs.pop(0)
						if DEBUG: print (f"feeding back output: {feedback}")
						if DEBUG: print (f"remaining outputs: {outputs}")
						instructions[vals[0]] = feedback
					else:
						instructions[vals[0]] = input('> ')
					if DEBUG: print (f"write pos: {vals[0]}")
					if DEBUG: print (f"write val: {instructions[vals[0]]}")
						
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

	def test_run_phase_sequence(self):
		self.assertEqual(
			run_phase_sequence(
				[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
				(4,3,2,1,0)
			),
			43210,
			"[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],(4,3,2,1,0)"
		)
		self.assertEqual(
			run_phase_sequence(
				[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
				(0,1,2,3,4)
			),
			54321,
			"[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],(0,1,2,3,4)"
		)
		self.assertEqual(
			run_phase_sequence(
				[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],
				(1,0,4,3,2)
			),
			65210,
			"[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],(1,0,4,3,2)"
		)
		self.assertEqual(
			run_phase_sequence(
				[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
				(9,8,7,6,5),
				True # feedback mode
			),
			139629729,
			"[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],(9,8,7,6,5)"
		)
		self.assertEqual(
			run_phase_sequence(
				[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10],
				(9,7,8,5,6),
				True # feedback mode
			),
			18216,
			"[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10],(9,7,8,5,6)"
		)






if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		instructions = [3,99]

		# direct mode
		thruster_outputs = []
		permute = [0,1,2,3,4]
		for i in permutations(permute):
			thruster_outputs.append(run_phase_sequence(instructions.copy(), i))

		print(sorted(thruster_outputs))

		# feedback mode
		thruster_outputs = []
		permute = [5,6,7,8,9]
		for i in permutations(permute):
			thruster_outputs.append(run_phase_sequence(instructions.copy(), i, True))

		print(sorted(thruster_outputs))


	print("done");




def puzzle_text():
	print("""
""")
