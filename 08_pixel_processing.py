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
		pixels = "122222222021222212220220022122202222022012222222222222022022122222220210000222222222222112222222222022222222222222222222222222022022222222222222222222022222222220222202120221122222212222122202222222222222022222222222222210010222222222222202222222222022222222222222222222222222022222222222222222222222022222222222222212021221222222212222222002222222222222022022022222221201000222222222222202222222222122222222222222222222222222122222222222222222222222122222222122222202022220222022222222122102222222222222122222222222220202202222222222222012222222222222222222222222222222222222222122222222222222222222222222222222222222122222022002212222222002222222222222122022122222221210200222222222222122222222222022222222222222222222222222022022222222222222221222022222222222122212121220222122202222122022222222222222122022222222221222212222222222222202222202222022222222222022222222222222222122222222222222222222222222222222222222121222222102222222222212222222222222222022022221221201212222222222222122202212222122222222222022222222222222122222222222222222222222122222222222222222122222222222202222022122222222222222122222022220220211010222222222222202212202222122222222222022222222222222022022222222222222220222122222222020222222020222022102202222122212222222222222222122022220211220210222222222222202222212222122222222222022222222222222222022222222222222221222122222222122122212021221122212212222022002222222222222222022022222212202020222222222222122222212202122222222222122212222222222122222222222222222222222222222222121122212020221022112202222022122222222222222022022122220202221220222222222222012202212222222222222222022222222222222222122222222222222221222222222222222122202220221022102222222222012222222222222222120122222202200210222222222222222222202212022222222222122202222222222222222222022222222220222222222222220222202020220222122222222222102222222222222122122022220210220122222222222220012212222222222222222222222222222222222222122222022222222221222022222222122222222120221222000202222222222202222222222222021122221202200011222222222222002202202212222222222222122202222222222022122222022222222220222122222222022222202020221122201202222022112212222222222022020022221201210021222222222220002202202212022222222222122202222222222122022222022222222222222022222222022222202221221022111202202222122222222222222122221122221221210200222222222222002222222212122222222222022212222222222122222222222222222220222122222222020122222122222222102212212122212202222222222122020022221201220120222222222220202222212202222222222222022212222222222222122222122222222220222022222222021022222221221022112202202122202212222222222122020122220202221010222222222221122212212222122222222222222222222222222122222222222222222221222122222222221022202222222222022222212122112222222222222022022222220210221220222222202220002222212222122222222222122222222222222022222222122222222220222222222222220222202121220022122222212122122202222222222122222222221202201022222222222221222202222222122222222222222212222222222122222222022222122222222222222222221222202121220022010222202022112222222222222122021122222211211221222222202222202222202222122222222222022222222222222122022222122222222220222122222222220220222120221222012222222222202202222222222222221022220201211222222222212220012202222212022222222222222202222222222022222222122222222221222022222222222120212022220022000202222022122212222222222022022022221222200210222222212221212202212222222222222222122212222222222022122222022222022221222122222222020022222120221022121112222122102212222222222222021022220212202011222222202220012202202212222222222222222212022222222022022222222222022222222022222222220020202121220022112022202022022222222222222222221022220210210110222222222220102202202222222222222222022212022222222122022222222222122220220022222222221021212121220022122222212222112202222222222122121222222211200210222222222221002212212202022222222222022212222220222222222222122222022221222022222222122220212221220222010222122122122202222222222222121122221212220100222222222220122202212212222222222222122222122202222021222222122222022222221022222222222021222120222122112002202122022212222222220022222222220212202222222222212220012212212222122222222222022222122220222022222222122222222220221222222222120221212221221222221212022222212222222222221222220222222201212100122222202221022202222202022222222222122222022220222120022222122222222221222022220222122220212222220222211002102222012202222222221022122122220221202122122222202222222212212222022222122222122202122211222020222222022222022221221222222222121120222022222222101002122022222212222222222222120022220212211112022222222222112212212212122222022222122222222210222121022222122222122222220122220212222121202021222212202212122222102222222222220022221122221212220211122222212221022212202212022222122222022202022200222020222222222222122221221122220222122021222120222012200112102122212212222222221122022122221220222121222222222220222222212202122222222222122202122211222222122222022222222221222022220212121220212020221202220012022222222202222222221022222022220221202102222222222222222222222212122222122222222222002211222121122222222222222221222222220222221120212220222122212202012022022222222222222122220222220200221101222022202221122202202202022222022222222212212201222120022222022222122222220222221212022021202221222002001112012122212202222222222222122122220201200122122022212221222222202202222222222222122212222200222022022222022222022220222222220212022220202121220212201202022022112222222222222122021122222221202220122122202220112212212222122222222222022202022222222120122222022222222221222022222222021121202221220122201212022122222222222222220122120022222221211001122222212222222212212202122222022222122202012220222121222222122222122220221022222202122120202120221002120202212122022202222222220122221022221221212222022022202220002212202212222222222222222222212200222122122222022222122221221022221202022221202022222112000112102222222202222222222022022222222210202212222122212220012222222212222222222222022222212222222222022222222222022220220022220212121220212022221102111222002222112202222222222222222022220221211012122222222221002202202222122222222222022202202221222222122222222222222221220022222212021122202222220002011202022222102222222222220122020022221200201010222222222222122202202202022222222222222222122221222020122222022222222221202122222212022020202121222112102112122022212222222222220022020122222211221011222222222221012222222222122222222222222202112212222022022222022222122222220022122202220122102022220012012122112022122222222222221222022022220220201211221122202222222212202212122222022222222222122200222120222222022222122222200122122202222121012122221202010212202122122202222222222222122102222220202121021022222221112202222202022222002222122212102210222121222222022222122221220222020222122022122120220212202002022222222202222222222222120102221222212210020022222222202202202222222222112222022202122211222021022222222222122220220122122212220220122220221202110122012022212212222222221222122222220212202222022122222210022202212202122222022222022212122210222022022222122222222222210022120202020021122121220222222022002122022212222222221122122002222222220111220122212202102222202222122222012222022202112201202020122222022222022221221022120202221120002121221222122002222122112202222222222022222012221202210222020122222212202202222222122222012222122202012220212222222222022222222221211222022202220122222121222002121212202222102212222222222022121122221211201100221122222211212222212212122222122222122222222201202020122222122222022220220022222202122220102121222122210202212122202202222222222122220002222210211100020122212200212212222202022222122222222212102200222021022222222222022221211022220222022000022022222112102102022022122212222222222022222222220201211222020222222222112202222202122222122222222202022211202022222222022222122221210222121202022001212222220102222222212122102212222222221222120202222200200120021122212222102212202202222222102222022212022210202220022202022222122221201220120222022220202020222102202102102122012222222222221022221102221200212100121122222202022212222212122222002222122222122220202122222222122222222222221221022212122012222021222002120102112222112222222122220122220022222202211102220222202221102212222212222222102221122222112221222021222212122222022222221121022212222221022220221102020222002222122222222122222022020012221200210110020122212221002212212212222222202221222202022212212120122212021222122221220221120212022022112222221222112212012122222222222222222122021202220200212022020222222212122202222202122222122221022222002212202120022202122222122222212120122202021201022220221102220122002022010222222122221122221112221222222020122022202210222202222212022222002222222212202211202120222102122222222221202022020212122011222121221002011102112222012212222222222122020012222200212222020022212222202212202222022222122220022202202222202120222012120222122221210022020222120211012022222002001212102022102202222122222022121122221210210121022222202222102202202202222222200220122202122200212021021122021222222220200221221202221001212020222112110002122222120222222222222022222212221222220201121022222202202222202222220222122221122212202201202220021002222222122221201122200222222220122022221222102202212022212212222002221222221122222200202012022102212200012202222212221222201221122222012221212022121002121222222220221121020212021110202121222022222102222022220212220002221222221202221222221112121112202012222212202202122222222222022212202220202022122112020222122221221021111212122211112221221002021122222122210212220022221122121102222211222121020122202212112222212222022222012221022222200201212020122022221222122221220122202202021201112121221112200012112022111222122012221122120012221222222110120122212111222202212202120222211221122202020212222221021122020222222220200020112212121121002220221102122022212222201202220122220122221222222201222222221022212002122212222202021222112221022222001200202120221112021222122221211122222202122010122020222122211002212022102202122112222222120022220221211120221202212200102222212202220222200220122202112210222122120102020222022220222221002222121011202120221022220222022122200212222002222122221212221222211101021012222201012222212202022222122220222202100220222222122122021222122220202022212202122000112022220202201222121122222212220002222122120110220200211022121122222000222212212222221222010220222222120201222022121222122222022221220221020212020202222220221212110122210222001212021212222022122211222210212010220112212210012222222220222222121222222212202202222121220222021222122222212222102212122111122221220122112202122022211202022022220122221112222211220221022112212000012210222220020222100220222000212201212121121020021222222220212121112202202121222120220112211002002222022202221222220222222211222112222010221122212022102201212221022222101221022222211212202121221012120222022221220022012202222122022122210202011222211022001222202002222122221222221101201021120002222212122200202221120222020222222101021200222220020122220222122222202122120202101201022122200112022022201222111222011122220222221110220222210001221002202201022200212210221222020221022122220200202221121101121222022220220022001102002002102022222102101202212022202202221112220022222020220211201121020012222202212221202222021222201220222121201210222020121021221222122220221120122122222201102122212122002012112122012212020222220122220221221201201222101202212202202211212222022222112220222202201212202221022002122222122221202100011112102200212020202102102212121022121202000022221122121012222002220000002011202001112211222211021222102222122110101221222020020102222222022222212120011002112021122021210222222212110222121222010122222122022202220211212020010201222010112201202222122222020220022221001210212222021211022222222222211010002212122222112121221102110012120022201202102212221122122212220020212201001120222011002221022210121222220221022220021222202220220112122222022221222010222202102010102222200212011122210221212222222002220122022110222220200212220002222202022221222202021222022221122112121221222020021002121222222222222202110202102112122020200122000112000122122212211202220222021212221200210220221010222222002202212220121222122222222100020211221021221211022222222221222112101002202222212220200122002122200222100202111222220222120020222020200121010001222201112202202200221222212221022210212212222122222022121222022222110101021102112002012022202022202002010020102202221022220122022201221210212002011212222122122201222220221120012222122012220210202021220010020222022221110212210202021220202220202112002122220121221222212012220222121102221202212101201102202011112200022222021022220221122002211221222021021110021222222220201211120112002011012122201102021022222020100212022112221020122212220021221201102022222121202220102202020121002222002110121220221222022122022222222222121211112222122220002220212002121202221120022202222022222022021221221112202212112111222010212212002201222220202220102010221102210120221101222222222221102002012012120022122120210202222212022122210222200212222121220112222220202021201212222201222211202220221122221221122212202010222020120120122222022221100220212102100001002021212002111112001120212222122012220122021012221001211210222221202220212222122202020022121220002000112102201220021101120222222221101011200022121121212020210112201002012222221212002102120121020020221000210221011012222210122222222200022221111221212020210000222022120212021222022220202112010202000012022220212202000202212121001212212012221220020222220221202111222010002022112222122211121020211222222200101111222020121120022222222220111001011212020000012220202022022112011221102002020122221022122111222100200021011010222100102212112221221222112220122111111211200020100221120222222221001212110112201002102002222222211022220020121222122012120011220022221200201101011211122112102211222202221122202222002200210222200021000211122222112220011000101112000122002102202022001222102221001102122122021022020200221112210000202021122111222202022200021200001201022002110100212122011121120222012220010022002122022210022111210212202002001102212102121022021111221200220022201210121010122110222221212212021010102222102002220221210122110120120222102222111122100112202211112021120012122102212011211122102022220002220221221120211211101200212002102220112221222020220201122011020012221220101002020222122220100221011122120000212101002102100122110000110012200002221021122022220221201020000211112112112212222210120000000201102200210110212221101210022222202220020112002022021022122021010222121222120021101222022202020120221022220112222201121122122010222222102220221211200210002211201012202022112212020122002220220100112202122002102122010122210022200100011222101212220211020111220222222001122120102221212221222210122012020202122020101001211120200100120022202221222011212202220000202001002002022202022110021220111202121222122122220201212200210220112002212212012210021002200212012111002001200121202200221022212221022000111200112220201120010120220220210222111022200001200222202210000100020021010101220200010122011000210212201122101121221121120101211021010101201000111"
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