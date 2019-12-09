# adventofcode 2019
# crushallhumans
# puzzle 9 - intcode relative mode
# 12/9/2019

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

	# augment memory
	initial_length = len(instructions)
	for i in range(0,10000):
		instructions.append(0)

	i = instruction_position
	relative_base = 0
	test_c = 1
	diag_code = -1
	outputs = []
	num_instrux = initial_length
	if type(inputs) is not list:
		x = list()
		x.append(inputs)
		inputs = x

	if DEBUG: print (f"instructions: {instructions[0:initial_length]}")
	if DEBUG: print (f"inputs: {inputs}")

	single_param_opcodes 	= [3,4,9]
	multi_param_opcodes 	= [1,2,7,8]
	jump_opcodes 			= [5,6] 

	write_final_param_opcodes = [3,1,2,7,8]
	read_final_param_opcodes  = [4,5,6,9] 

	try:
		jump = 999999
		opcode = None
		s_opcode = None

		dc = 0
		monitor = 10000
		while i < num_instrux:
			if DEBUG: print (f"\n{dc},{i}: {instructions[i:i+20]}...")
			dc += 1

			if not dc % monitor:
				sys.stdout.write('.')  # same as print
				sys.stdout.flush()

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
				if (dc >= monitor):
					print("")
				return (diag_code, instructions[0:initial_length], is_feedback, i)

			# handle opcode
			else:
				vals = []
				jump = 4

				# handle parameterized opcode
				# get operational values
				# set cursor jump value
				if (opcode > 99):
					s_opcode = str(opcode)
					opcode = int(s_opcode[-2:])
					num_params = len(s_opcode) - 2
					if DEBUG: print (f"num_params: {num_params}")

					if (opcode in multi_param_opcodes and 5 > len(s_opcode) > 2):
						while (len(s_opcode) < 5):
							s_opcode = f"0{s_opcode}"
						num_params = 3

					if not (10 > opcode > 0):
						raise Exception(f"bad opcode encoded: {s_opcode}")

					if DEBUG: print (f"opcode: {opcode}")
					if DEBUG: print (f"s_opcode: {s_opcode}")
					if DEBUG: print (f"s_opcode[-2:]: {s_opcode[-2:]}")
					if DEBUG: print (f"num_params: {num_params}")
					if DEBUG: print ("..")

					# process parameters starting from left of 0N
					for d in range(0,num_params):
						pos = -2-(d+1)
						param = int(s_opcode[pos])
						inner_idx = i+d+1
						idx = instructions[inner_idx]

						if DEBUG: print (f"pos: {pos}")
						if DEBUG: print (f"param: {param}")
						if DEBUG: print (f"inner_idx: {inner_idx}")

						# immediate mode
						if param == 1:
							if DEBUG: print (f"val immmode appending RAW: {idx}")
							vals.append(idx)
						else:
							# relative mode
							if param == 2:
								relidx = relative_base + idx
								if DEBUG: print (f"val relmode instructions[{relative_base} + {idx} = {relidx}]: {instructions[relidx]}")
								idx = relidx
							elif param == 0:
								# position mode
								if DEBUG: print (f"val posmode {idx}: {instructions[idx]}")
							else:
								raise Exception(f"unknown parameter mode {param}")

							#handle final value (write)
							if (abs(pos) == len(s_opcode) and opcode in write_final_param_opcodes):
								# write values are always positional
								if DEBUG: print (f"final: appending {idx}")
								vals.append(idx)
							else:
								if DEBUG: print (f"middle: appending {instructions[idx]}")
								vals.append(instructions[idx])
						if DEBUG: print (".")

								


				# handle unparameterized (positional) opcode value collection
				if not len(vals):
					if DEBUG: print (f"plain opcode {opcode} getting val +1 at {instructions[i+1]} ({i+1}): {instructions[instructions[i+1]]}")

					# input code is always immediate
					if opcode == 3:
						vals.append(instructions[i+1])
					else:
						vals.append(instructions[instructions[i+1]])

					if DEBUG: print (f"plain opcode {opcode} getting val +2 at {instructions[i+2]} ({i+2}): {instructions[instructions[i+2]]}")
					vals.append(instructions[instructions[i+2]])

					if (opcode in multi_param_opcodes):
						if DEBUG: print (f"plain opcode {opcode} getting val +3 (write position) at {instructions[i+3]} ({i+3}): {instructions[instructions[i+3]]}")
						vals.append(instructions[i+3])


				#PROCESS OPCODES
				# jump codes
				if (opcode in jump_opcodes):
					if DEBUG: print (f"vals op{opcode}: {vals}")
					if (opcode == 5):
						if vals[0] != 0:
							if DEBUG: print (f"JUMP TO : {vals[1]}")
							i = vals[1]
							continue
						else:
							jump = 3
					elif (opcode == 6):
						if vals[0] == 0:
							if DEBUG: print (f"JUMP TO : {vals[1]}")
							i = vals[1]
							continue
						else:
							jump = 3

				# output code
				elif (opcode == 4):
					jump = 2
					if DEBUG: print (f"vals op{opcode}: {vals}")
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
					if DEBUG: print (f"vals op{opcode}: {vals}")
					if (len(inputs)):
						if DEBUG: print (f"got inputs from main input array")
						instructions[vals[0]] = inputs.pop(0)
					elif (len(outputs)):
						feedback = outputs.pop(0)
						if DEBUG: print (f"feeding back output: {feedback}")
						if DEBUG: print (f"remaining outputs: {outputs}")
						instructions[vals[0]] = feedback
					else:
						# readline for inputs (mostly this is an error)
						instructions[vals[0]] = input('> ')
					if DEBUG: print (f"write pos: {vals[0]}")
					if DEBUG: print (f"write val: {instructions[vals[0]]}")

				# relative base offset code
				elif (opcode == 9):
					jump = 2
					if DEBUG: print (f"vals op{opcode}: {vals}")
					if DEBUG: print (f"relative_base before: {relative_base}")
					relative_base = relative_base + vals[0]
					if DEBUG: print (f"relative_base after: {relative_base}")
						
				# operation codes
				elif (opcode in multi_param_opcodes):
					if DEBUG: print (f"vals op{opcode}: {vals}")
					result = -1
					jump = len(vals)+1
					position = vals.pop()

					if (opcode == 1):
						result = reduce((lambda x, y: x + y), vals)
					elif (opcode == 2):
						result = reduce((lambda x, y: x * y), vals)
					elif (opcode == 7):
						result = 1 if vals[0] < vals[1] else 0
					elif (opcode == 8):
						result = 1 if vals[0] == vals[1] else 0

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
		#day 2
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

		#day 5
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

		#day 7
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

		# day 9
		self.assertEqual(
			process_instructions(
				[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
			)[1],
			[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
		)
		self.assertGreaterEqual(
			process_instructions(
				[1102,34915192,34915192,7,4,7,99,0]
			)[0],
			32768
		)
		self.assertEqual(
			process_instructions(
				[104,1125899906842624,99]
			)[0],
			1125899906842624
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
		instructions = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,33,1017,1101,24,0,1014,1101,519,0,1028,1102,34,1,1004,1101,0,31,1007,1101,0,844,1025,1102,0,1,1020,1102,38,1,1003,1102,39,1,1008,1102,849,1,1024,1101,0,22,1001,1102,25,1,1009,1101,1,0,1021,1101,0,407,1022,1101,404,0,1023,1101,0,35,1013,1101,27,0,1011,1101,0,37,1016,1102,1,26,1019,1102,28,1,1015,1101,0,30,1000,1102,1,36,1005,1101,0,29,1002,1101,23,0,1012,1102,1,32,1010,1102,21,1,1006,1101,808,0,1027,1102,20,1,1018,1101,0,514,1029,1102,1,815,1026,109,14,2107,24,-5,63,1005,63,199,4,187,1105,1,203,1001,64,1,64,1002,64,2,64,109,-1,2108,21,-7,63,1005,63,225,4,209,1001,64,1,64,1106,0,225,1002,64,2,64,109,-16,1201,6,0,63,1008,63,35,63,1005,63,249,1001,64,1,64,1106,0,251,4,231,1002,64,2,64,109,9,2102,1,2,63,1008,63,37,63,1005,63,271,1105,1,277,4,257,1001,64,1,64,1002,64,2,64,109,11,1208,-8,23,63,1005,63,293,1105,1,299,4,283,1001,64,1,64,1002,64,2,64,109,8,21107,40,39,-8,1005,1017,319,1001,64,1,64,1106,0,321,4,305,1002,64,2,64,109,-28,2101,0,6,63,1008,63,39,63,1005,63,341,1106,0,347,4,327,1001,64,1,64,1002,64,2,64,109,19,2107,26,-7,63,1005,63,363,1106,0,369,4,353,1001,64,1,64,1002,64,2,64,109,1,1202,-9,1,63,1008,63,39,63,1005,63,395,4,375,1001,64,1,64,1105,1,395,1002,64,2,64,109,9,2105,1,-3,1106,0,413,4,401,1001,64,1,64,1002,64,2,64,109,-13,1207,-4,26,63,1005,63,435,4,419,1001,64,1,64,1105,1,435,1002,64,2,64,109,-1,21101,41,0,7,1008,1019,41,63,1005,63,461,4,441,1001,64,1,64,1105,1,461,1002,64,2,64,109,7,21107,42,43,-2,1005,1017,479,4,467,1105,1,483,1001,64,1,64,1002,64,2,64,109,-6,21108,43,46,0,1005,1013,499,1106,0,505,4,489,1001,64,1,64,1002,64,2,64,109,17,2106,0,-2,4,511,1105,1,523,1001,64,1,64,1002,64,2,64,109,-27,1202,-1,1,63,1008,63,28,63,1005,63,547,1001,64,1,64,1106,0,549,4,529,1002,64,2,64,109,18,1206,-1,567,4,555,1001,64,1,64,1106,0,567,1002,64,2,64,109,-16,21102,44,1,6,1008,1011,43,63,1005,63,587,1106,0,593,4,573,1001,64,1,64,1002,64,2,64,109,8,21102,45,1,-1,1008,1012,45,63,1005,63,619,4,599,1001,64,1,64,1105,1,619,1002,64,2,64,109,7,1205,1,633,4,625,1106,0,637,1001,64,1,64,1002,64,2,64,109,-8,2102,1,-3,63,1008,63,25,63,1005,63,659,4,643,1105,1,663,1001,64,1,64,1002,64,2,64,109,14,1206,-5,679,1001,64,1,64,1105,1,681,4,669,1002,64,2,64,109,-28,2101,0,2,63,1008,63,30,63,1005,63,707,4,687,1001,64,1,64,1106,0,707,1002,64,2,64,109,21,21101,46,0,0,1008,1019,48,63,1005,63,727,1106,0,733,4,713,1001,64,1,64,1002,64,2,64,109,-3,21108,47,47,1,1005,1017,751,4,739,1106,0,755,1001,64,1,64,1002,64,2,64,109,-13,1207,0,37,63,1005,63,771,1105,1,777,4,761,1001,64,1,64,1002,64,2,64,109,7,2108,21,-9,63,1005,63,797,1001,64,1,64,1105,1,799,4,783,1002,64,2,64,109,22,2106,0,-5,1001,64,1,64,1106,0,817,4,805,1002,64,2,64,109,-4,1205,-8,829,1106,0,835,4,823,1001,64,1,64,1002,64,2,64,109,-4,2105,1,0,4,841,1105,1,853,1001,64,1,64,1002,64,2,64,109,-30,1208,6,30,63,1005,63,871,4,859,1105,1,875,1001,64,1,64,1002,64,2,64,109,-2,1201,9,0,63,1008,63,22,63,1005,63,897,4,881,1106,0,901,1001,64,1,64,4,64,99,21101,27,0,1,21102,1,915,0,1106,0,922,21201,1,66266,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1105,1,922,22101,0,1,-1,21201,-2,-3,1,21101,0,957,0,1106,0,922,22201,1,-1,-2,1105,1,968,21202,-2,1,-2,109,-3,2106,0,0]

		# get BOOST code
		print (process_instructions(instructions,1)[0])

		# get distress code
		print (process_instructions(instructions,2)[0])



	print("done");




def puzzle_text():
	print("""
--- Day 9: Sensor Boost ---
You've just said goodbye to the rebooted rover and left Mars when you receive a faint distress signal coming from the asteroid belt. It must be the Ceres monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The Elves send up the latest BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors, for tenuous safety reasons, it refuses to do so until the computer it runs on passes some checks to demonstrate it is a complete Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support for parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: the parameter is interpreted as a position. Like position mode, parameters in relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from address 0. Instead, they count from a value called the relative base. The relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current relative base. When the relative base is 0, relative mode parameters and position mode parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if the value is negative) by the value of the parameter.
For example, if the relative base is 2000, then after the instruction 109,19, the relative base would be 2019. If the next instruction were 204,-34, then the value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

The computer's available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory. (It is invalid to try to access memory at a negative address, though.)
The computer should have support for large numbers. Some instructions near the beginning of the BOOST program will verify this capability.
Here are some example programs that use these features:

109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a copy of itself as output.
1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
104,1125899906842624,99 should output the large number in the middle.
The BOOST program will ask for a single input; run it in test mode by providing it the value 1. It will perform a series of checks on each opcode, output any opcodes (and the associated parameter modes) that seem to be functioning incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report no malfunctioning opcodes when run in test mode; it should only output a single value, the BOOST keycode. What BOOST keycode does it produce?

Your puzzle answer was 2752191671.

--- Part Two ---
You now have a complete Intcode computer.

Finally, you can lock on to the Ceres distress signal! You just need to boost your sensors using the BOOST program.

The program runs in sensor boost mode by providing the input instruction the value 2. Once run, it will boost the sensors automatically, but it might take a few seconds to complete the operation on slower hardware. In sensor boost mode, the program will output a single value: the coordinates of the distress signal.

Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?

Your puzzle answer was 87571.

Both parts of this puzzle are complete! They provide two gold stars: **
""")
