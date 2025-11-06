# adventofcode 2019
# crushallhumans
# puzzle 10 - asteroids
# 8/27/2020

import sys
import unittest
from functools import reduce
from itertools import permutations

DEBUG = True


# DEBUG = False

def run_phase_sequence(program, sequence, feedback_mode=False):
    return False


def process_instructions(instruction):
    coords = [0,0]
    asteroids = []
    row = 0
    col = 0
    for i in instruction:
        if (i == '#'):
            asteroids.append([row, col])
        elif (i == "\n"):
            row += 1
            col = -1
        col += 1
    print(asteroids)

    

    return coords


class testCase(unittest.TestCase):
    def test_process_instructions(self):
        self.assertEqual(
            process_instructions(""".#..#
.....
#####
....#
...##"""),
            [3,4],
            "3,4 basic example!"
        )

    def test_run_phase_sequence(self):
        self.assertEqual(
            True,
            True,
            "Truth!"
        )


if __name__ == '__main__':
    try:
        sys.argv[1]
        puzzle_text()

    except:
        instructions = [0]

    # get BOOST code
    # print (process_instructions(instructions,1)[0])

    # get distress code
    # print (process_instructions(instructions,2)[0])

    print("done");


def puzzle_text():
    print("""
""")
