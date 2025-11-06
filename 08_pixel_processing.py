# adventofcode 2019
# crushallhumans
# puzzle 8 - pixel processing
# 12/8/2019

import sys
import math
import unittest
import random
import itertools

def generate_layers(pixels, w, h):
	layers = []
	layer = []
	row = []
	wc = 0
	hc = 0
	for i in str(pixels):
		if wc >= w:
			layer.append(row.copy())
			row = []
			wc = 0
			hc += 1
		if hc >= h:
			layers.append(layer.copy())
			layer = []
			hc = 0
		row.append(int(i))
		wc += 1
	layer.append(row.copy())
	layers.append(layer.copy())

	return layers

def generate_image(pixels, w, h):
	layers = generate_layers(pixels, w, h)
	final_layer = []
	for hc in range(0,h):
		row = []
		for wc in range(0,w):
			pixel_val = None
			d = 0
			for layer in layers:
				pixel = layer[hc][wc]
				if pixel == 0 or pixel == 1:
					pixel_val = '.' if pixel else ' '
					break
				d += 1
			if pixel_val:
				row.append(pixel_val)
			else:
				raise Exception(f"no pixel found at {hc} x {wc}")
		final_layer.append(row) 
	return final_layer

class testCase(unittest.TestCase):
	def test_main_function(self):
		self.assertEqual(
			generate_layers(
				"123456789012",
				3,
				2
			),
			[[[1,2,3],[4,5,6]],[[7,8,9],[0,1,2]]]
		)

	def test_secondary_function(self):
		self.assertEqual(
			generate_image(
				"0222112222120000",
				2,
				2
			),
			[[' ','.'],['.',' ']]
		)



if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		pixels = "101000111"
		layers = generate_layers(pixels, 25, 6)
		print (f"{len(layers)} layers")
		lowest_zeroes = 9999999
		lowest_layer = []
		for i in layers:
			zeroes = 0
			for j in i:
				zeroes += j.count(0)
			if zeroes < lowest_zeroes:
				lowest_zeroes = zeroes
				lowest_layer = i

		print (lowest_zeroes)
		print (lowest_layer)

		ones = 0
		twos = 0
		for i in lowest_layer:
			ones += i.count(1)
			twos += i.count(2)
		print (ones * twos)

		image = generate_image(pixels, 25, 6)
		print (image)

		final_print = []
		for i in image:
			final_print.append(''.join(i)) 
		print("\n".join(final_print))

	print("done");




def puzzle_text():
	print("""
""")