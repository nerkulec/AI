# :((((

import numpy as np
from tqdm import tqdm
from itertools import product
from heapq import heappush, heappop
from util import timeit, cacheit

# #- pewny pełny
# .- pewny pusty
# ?- nierozpatrzony

def T(image): #transpose
    return list(map(list, zip(*image)))

@timeit
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

@timeit
def legal(arr, row):
    for i in range(len(row)):
        if arr[i] == '#' and row[i] == '.':
            return False
        if arr[i] == '.' and row[i] == '#':
            return False
    return True

def step(image, rows, cols, all_rows, all_cols, changed):
    image = deepcopy(image)
    width = len(cols)
    height = len(rows)
    anything_changed = False
    changes = []
    if changed == 'all':
        row_nums = range(height)
        col_nums = range(width)
    else:
        row_nums = set(c[1] for c in changed)
        col_nums = set(c[0] for c in changed)
    # rows
    for row_num in row_nums:
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
            return image, False, anything_changed, changes
        for x in range(len_row):
            if all_full[x] and image[row_num][x] != '#':
                image[row_num][x] = '#'
                changes.append((x, row_num))
                anything_changed = True
            elif all_empty[x] and image[row_num][x] != '.':
                image[row_num][x] = '.'
                changes.append((x, row_num))
                anything_changed = True
    # cols
    imageT = T(image) #transpose
    for col_num in col_nums:
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
            return image, False, anything_changed, changes
        for y in range(len_col):
            if all_full[y] and image[y][col_num] != '#':
                image[y][col_num] = '#'
                changes.append((col_num, y))
                anything_changed = True
            elif all_empty[y] and image[y][col_num] != '.':
                image[y][col_num] = '.'
                changes.append((col_num, y))
                anything_changed = True
    return image, True, anything_changed, changes

@timeit
def filter_domains(image, all_rows, all_cols, debug=False):
    imageT = T(image)
    all_rows = [[r for r in all_rows[y] if legal(r, image[y])] for y in range(len(all_rows))]
    all_cols = [[c for c in all_cols[x] if legal(c, imageT[x])] for x in range(len(all_cols))]
    if debug:
        possible_rows = [len(r) for r in all_rows]
        possible_cols = [len(c) for c in all_cols]
        print(f'possible rows: {possible_rows}')
        print(f'possible cols: {possible_cols}')
        print(f'sum: {sum(possible_rows) + sum(possible_cols)}')
    return all_rows, all_cols

# def consequences(image, rows, cols, all_rows, all_cols): # returns image, solved, possible
#     possible = True
#     changes = 'all'
#     while any(any(p == '?' for p in row) for row in image):
#         image, possible, anything_changed, changes = step(image, rows, cols, all_rows, all_cols, changes)
#         if not possible or not anything_changed:
#             return image, False, possible
#     return image, True, possible

@timeit
def consequences(image, rows, cols, all_rows, all_cols, safe=False): # returns image, possible
    queue = []
    if not safe:
        image = deepcopy(image)
        all_rows = all_rows.copy()
        all_cols = all_cols.copy()
    for y in range(len(image)):
        heappush(queue, (0, 'row', y))
    for x in range(len(image[0])):
        heappush(queue, (0, 'col', x))
    counter = 1
    while queue:
        _, t, num = heappop(queue)
        if t == 'row':
            row = image[num]
            len_row = len(row)
            all_full = [True for _ in range(len_row)]
            all_empty = [True for _ in range(len_row)]
            any_legal = False
            for arr in all_rows[num]:
                if legal(arr, row):
                    any_legal = True
                    for x in range(len_row):
                        if image[num][x] == '?':
                            if all_full[x]:
                                all_full[x] = arr[x]=='#'
                            if all_empty[x]:
                                all_empty[x] = arr[x]=='.'
                else:
                    pass #remove arr from all_rows
            if not any_legal:
                return image, False
            for x in range(len_row):
                if image[num][x] == '?':
                    if all_full[x] and image[num][x] != '#':
                        image[num][x] = '#'
                        heappush(queue, (counter, 'col', x))
                        counter += 1
                    elif all_empty[x] and image[num][x] != '.':
                        image[num][x] = '.'
                        heappush(queue, (counter, 'col', x))
                        counter += 1
        elif t == 'col':
            col = [image[y][num] for y in range(len(image))]
            len_col = len(col)
            all_full = [True for _ in range(len_col)]
            all_empty = [True for _ in range(len_col)]
            any_legal = False
            for arr in all_cols[num]:
                if True or legal(arr, col):
                    any_legal = True
                    for y in range(len_col):
                        if image[y][num] == '?':
                            if all_full[y]:
                                all_full[y] = arr[y]=='#'
                            if all_empty[y]:
                                all_empty[y] = arr[y]=='.'
            if not any_legal:
                return image, False
            for y in range(len_col):
                if image[y][num] == '?':
                    if all_full[y]:
                        image[y][num] = '#'
                        heappush(queue, (counter, 'row', y))
                        counter += 1
                    elif all_empty[y]:
                        image[y][num] = '.'
                        heappush(queue, (counter, 'row', y))
                        counter += 1
    return image, True

# cwiczenie wykorzystac mutable named parameter as cache in heappush - decorate it

def nonogram(rows, cols):
    width = len(cols)
    height = len(rows)
    all_rows = [[hyp_row for hyp_row in all_arrangements(width, rows[y])] for y in range(height)]
    print(f'all rows calculated: {[len(r) for r in all_rows]}')
    all_cols = [[hyp_col for hyp_col in all_arrangements(height, cols[x])] for x in range(width)]
    print(f'all cols calculated: {[len(c) for c in all_cols]}')
    print(f'sum: {sum([len(r) for r in all_rows]) + sum([len(c) for c in all_cols])}')
    image = [['?' for _ in range(width)] for _ in range(height)]
    image, _ = consequences(image, rows, cols, all_rows, all_cols)
    draw(image)
    image, _ = backtrack(image, rows, cols, all_rows, all_cols)
    image, _ = backtrack(image, rows, cols, all_rows, all_cols)
    draw(image)
    return image

def backtrack(image, rows, cols, all_rows, all_cols, filter_interval=25):
    points = product(range(len(cols)), range(len(rows)))
    points = sorted(points, key=lambda p: min(-abs(p[0]-len(cols)/2), -abs(p[1]-len(rows)/2)))
    counter = 0
    for x,y in points:
        if image[y][x] == '?':
            image[y][x] = '#'
            _, possible = consequences(image, rows, cols, all_rows, all_cols)
            image[y][x] = '.'
            if possible:
                _, possible = consequences(image, rows, cols, all_rows, all_cols)
                if not possible:
                    image[y][x] = '#'
                else:
                    image[y][x] = '?'
        if counter >= filter_interval:
            all_rows, all_cols = filter_domains(image, all_rows, all_cols, True)
            image, possible = consequences(image, rows, cols, all_rows, all_cols)
            timeit('SHOW')
            draw(image)
            counter = -1
        counter += 1
                
    image, possible = consequences(image, rows, cols, all_rows, all_cols)
    return image, possible

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


