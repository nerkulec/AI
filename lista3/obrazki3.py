# :((((

import numpy as np
from tqdm import tqdm

# #- pewny pełny
# .- pewny pusty
# ?- nierozpatrzony

def T(image): #transpose
    return list(map(list, zip(*image)))

def deepcopy(thing):
    try:
        return [deepcopy(el) for el in thing.copy()]
    except AttributeError:
        return thing

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
        yield list(arr[:-1])

def legal(arr, row):
    for i in range(len(row)):
        if arr[i] == '#' and row[i] == '.':
            return False
        if arr[i] == '.' and row[i] == '#':
            return False
    return True

def step(image, rows, cols, all_rows, all_cols):
    image = deepcopy(image)
    width = len(cols)
    height = len(rows)
    anything_changed = False
    # rows
    for row_num in range(height):
        row = image[row_num]
        row_ch = rows[row_num]
        len_row = len(row)
        all_full = [True for _ in range(len_row)]
        all_empty = [True for _ in range(len_row)]
        any_legal = False
        for arr in all_rows[row_num]:
            if legal(arr, row):
                any_legal = True
                all_full = [all_full[x] and arr[x]=='#' for x in range(len_row)]
                all_empty = [all_empty[x] and arr[x]=='.' for x in range(len_row)]
        if not any_legal:
            return image, False, anything_changed
        for x in range(len_row):
            if all_full[x] and image[row_num][x] != '#':
                image[row_num][x] = '#'
                anything_changed = True
            elif all_empty[x] and image[row_num][x] != '.':
                image[row_num][x] = '.'
                anything_changed = True
    # cols
    imageT = T(image) #transpose
    for col_num in range(width):
        col = imageT[col_num]
        col_ch = cols[col_num]
        len_col = len(col)
        all_full = [True for _ in range(len_col)]
        all_empty = [True for _ in range(len_col)]
        any_legal = False
        for arr in all_cols[col_num]:
            if legal(arr, col):
                any_legal = True
                all_full = [all_full[y] and arr[y] == '#' for y in range(len_col)]
                all_empty = [all_empty[y] and arr[y] == '.' for y in range(len_col)]
        if not any_legal:
            return image, False, anything_changed
        for y in range(len_col):
            if all_full[y] and image[y][col_num] != '#':
                image[y][col_num] = '#'
                anything_changed = True
            elif all_empty[y] and image[y][col_num] != '.':
                image[y][col_num] = '.'
                anything_changed = True
    return image, True, anything_changed

def filter_domains(image, all_rows, all_cols):
    imageT = T(image)
    all_rows = [[r for r in all_rows[y] if legal(r, image[y])] for y in range(len(all_rows))]
    all_cols = [[c for c in all_cols[x] if legal(c, imageT[x])] for x in range(len(all_cols))]
    print(f'possible rows: {[len(r) for r in all_rows]}')
    print(f'possible cols: {[len(c) for c in all_cols]}')
    return all_rows, all_cols

def consequences(image, rows, cols, all_rows, all_cols): # returns image, solved, possible
    possible = True
    while any(any(p == '?' for p in row) for row in image):
        image, possible, anything_changed = step(image, rows, cols, all_rows, all_cols)
        if not possible or not anything_changed:
            return image, False, possible
        all_rows, all_cols = filter_domains(image, all_rows, all_cols)
    return image, True, possible

def nonogram(rows, cols):
    width = len(cols)
    height = len(rows)
    all_rows = [[hyp_row for hyp_row in all_arrangements(width, rows[y])] for y in range(height)]
    print(f'all rows calculated: {[len(r) for r in all_rows]}')
    all_cols = [[hyp_col for hyp_col in all_arrangements(height, cols[x])] for x in range(width)]
    print(f'all cols calculated: {[len(c) for c in all_cols]}')
    image = [['?' for _ in range(width)] for _ in range(height)]
    image, solved, possible = consequences(image, rows, cols, all_rows, all_cols)
    if solved:
        return image
    image, solved = backtrack(image, rows, cols, all_rows, all_cols)
    draw(image)
    return image

def backtrack(image, rows, cols, all_rows, all_cols):
    for y in range(len(rows)):
        for x in tqdm(range(len(cols))):
            if image[y][x] == '?':
                image[y][x] = '#'
                _, _, possible = consequences(image, rows, cols, all_rows, all_cols)
                image[y][x] = '.'
                if possible:
                    _, _, possible = consequences(image, rows, cols, all_rows, all_cols)
                    if not possible:
                        image[y][x] = '#'
                    else:
                        image[y][x] = '?'
        image, solved, possible = consequences(image, rows, cols, all_rows, all_cols)
        all_rows, all_cols = filter_domains(image, all_rows, all_cols)
        draw(image)
                
    image, solved, _ = consequences(image, rows, cols, all_rows, all_cols)
    return image, solved

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

