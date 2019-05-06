# wbite - pokazać

import numpy as np

# #- pewny pełny
# .- pewny pusty
# ?- nierozpatrzony

def all_arrangements(len_row, ch):
    def h(len_row, ch):
        sum_ch = sum(ch)
        len_ch = len(ch)
        if len_ch == 0:
            yield '.'*len_row
        else:
            for start in range(len_row-sum_ch-len_ch+1):
                for arrangement in h(len_row-ch[0]-start-1, ch[1:]):
                    yield '.'*start + '#'*ch[0] + '.' + arrangement
    for arr in h(len_row+1, ch):
        yield arr[:-1]

def legal(arr, row):
    for i in range(len(row)):
        if arr[i] == '#' and row[i] == '.':
            return False
        if arr[i] == '.' and row[i] == '#':
            return False
    return True

def step(image, rows, cols):
    # rows
    for row_num, (row, row_ch) in enumerate(zip(image, rows)):
        len_row = len(row)
        all_full = [True for _ in range(len_row)]
        all_empty = [True for _ in range(len_row)]
        for arr in all_arrangements(len_row, row_ch):
            if legal(arr, row):
                all_full = [all_full[x] and arr[x]=='#' for x in range(len_row)]
                all_empty = [all_empty[x] and arr[x]=='.' for x in range(len_row)]
        for x in range(len_row):
            if all_full[x]:
                image[row_num][x] = '#'
            elif all_empty[x]:
                image[row_num][x] = '.'
    draw(image)
    #cols
    imageT = list(map(list, zip(*image))) #transpose
    for col_num, (col, col_ch) in enumerate(zip(imageT, cols)):
        len_col = len(col)
        all_full = [True for _ in range(len_col)]
        all_empty = [True for _ in range(len_col)]
        for arr in all_arrangements(len_col, col_ch):
            if legal(arr, col):
                all_full = [all_full[y] and arr[y]=='#' for y in range(len_col)]
                all_empty = [all_empty[y] and arr[y]=='.' for y in range(len_col)]
        for y in range(len_col):
            if all_full[y]:
                image[y][col_num] = '#'
            elif all_empty[y]:
                image[y][col_num] = '.'
    draw(image)
    return image

def nonogram(rows, cols):
    width = len(cols)
    height = len(rows)
    image = [['?' for _ in range(width)] for _ in range(height)]
    while any(any(p == '?' for p in row) for row in image):
        image = step(image, rows, cols)
    return image

def draw(image):
    for y in range(len(image)):
        for x in range(len(image[y])):
            print(image[y][x], end='')
        print()
    print()

with open("zad_input.txt", "r") as in_f:
    with open("zad_output.txt", "w") as out_f:
        w, h = [int(x) for x in next(in_f).split()]
        r = [[int(el) for el in line.split()] for line in in_f]
        rows, cols = r[:w], r[w:]
        image = nonogram(rows, cols)
        for y in range(len(image)):
            for x in range(len(image[y])):
                out_f.write(image[y][x])
            out_f.write("\n")


