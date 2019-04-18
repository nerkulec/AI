from numpy import random
from tqdm import tqdm
import numpy as np

word_set = set()
with open("words_for_ai1.txt", "r") as file:
    for word in file:
        word_set.add(word.strip())

def spacify(line, words):
    n = len(line)
    line = ' '+line
    dyn = [-1]*(n+1)
    dyn[0] = 0
    prev = [0]*(n+1)
    for end in range(2, n+2):
        for start in range(end-1, 0, -1):
            word = line[start:end]
            if word in words and dyn[start-1]>=0:
                value = dyn[start-1] + (end-start)**2
                if value > dyn[end-1]:
                    dyn[end-1] = value
                    prev[end-1] = start
    line = line[1:]
    spaces = []
    loc = prev[-1]
    while loc != 0:
        spaces.append(loc-1)
        loc = prev[loc-1]
    spaces = spaces[:-1]
    for space in spaces:
        line = line[:space] + ' ' + line[space:]
    return line

def gen_random_spaces(line):
    n = len(line)
    if n == 0:
        yield line
    perm = random.permutation(range(1, n+1))
    for i in perm:
        if line[:i] in word_set:
            for rest in gen_random_spaces(line[i:]):
                yield line[:i]+' '+rest

def gen_random_spaces2(line):
    n = len(line)
    if n == 0:
        yield line
    places = list(range(1, n+1))
    places.sort(key=lambda x: 1/abs(x-n/2+0.00001))
    for i in places:
        if line[:i] in word_set:
            for rest in gen_random_spaces(line[i:]):
                yield line[:i]+' '+rest
    

def random_spaces(line):
    a = gen_random_spaces2(line)
    try:
        return next(a)[:-1]
    except StopIteration as s:
        return ''

correct = 0
random_correct = 0
num_lines = 0
with open("stripped.txt", "r") as line_input:
    with open("origin.txt", "r") as origin:
        for line in tqdm(line_input):
            orig_line = next(origin)[:-1]
            if spacify(line.strip(), word_set) == orig_line:
                correct += 1
            r = random_spaces(line.strip())
            if r == orig_line:
                random_correct += 1
            # print(r)
            # print(orig_line)
            # print()
            num_lines += 1

print(correct/num_lines)
print(random_correct/num_lines)


