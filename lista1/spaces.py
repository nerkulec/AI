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

def random_spaces(line):
    n = len(line)
    num_spaces = np.random.randint(n//4)
    spaces = np.random.choice(n, num_spaces, replace=False)
    for space in spaces:
        line = line[:space] + ' ' + line[space:]
    return line

correct = 0
random_correct = 0
num_lines = 0
with open("ptadeusz.txt", "r") as line_input:
    with open("pantadeuszorigin.txt", "r") as origin:
        for line in line_input:
            orig_line = next(origin)
            if spacify(line.strip(), word_set)+'\n' == orig_line:
                correct += 1
            if random_spaces(line.strip())+'\n' == orig_line:
                random_correct += 1
            num_lines += 1

print(correct/num_lines)
print(random_correct/num_lines)

# with open("zad2_input.txt", "r") as line_input:
#     with open("zad2_output.txt", "w") as line_output:
#         for line in line_input:
#             line_output.write(spacify(line.strip(), word_set)+"\n")

