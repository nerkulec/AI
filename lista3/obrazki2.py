import numpy as np

# #- pewny pełny
# .- pewny pusty
# ?- nierozpatrzony

def T(image): #transpose
    return list(map(list, zip(*image)))

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
    # rows
    for row_num, (row, row_ch) in enumerate(zip(image, rows)):
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
            return image, False
        for x in range(len_row):
            if all_full[x]:
                image[row_num][x] = '#'
            elif all_empty[x]:
                image[row_num][x] = '.'
    #draw(image)
    #cols
    imageT = T(image) #transpose
    for col_num, (col, col_ch) in enumerate(zip(imageT, cols)):
        len_col = len(col)
        all_full = [True for _ in range(len_col)]
        all_empty = [True for _ in range(len_col)]
        any_legal = False
        for arr in all_cols[col_num]:
            if legal(arr, col):
                any_legal = True
                all_full = [all_full[y] and arr[y]=='#' for y in range(len_col)]
                all_empty = [all_empty[y] and arr[y]=='.' for y in range(len_col)]
        if not any_legal:
            return image, False
        for y in range(len_col):
            if all_full[y]:
                image[y][col_num] = '#'
            elif all_empty[y]:
                image[y][col_num] = '.'
    #draw(image)
    return image, True

def consequences(image, rows, cols, all_rows, all_cols): # returns image, solved, possible
    while any(any(p == '?' for p in row) for row in image):
        prev_image = image
        image, possible = step(image, rows, cols, all_rows, all_cols)
        if not possible:
            return image, False, False
        if prev_image == image:
            return image, False, True
    return image, True, True

def nonogram(rows, cols):
    width = len(cols)
    height = len(rows)
    all_rows = [[hyp_row for hyp_row in all_arrangements(width, rows[y])] for y in range(height)]
    all_cols = [[hyp_col for hyp_col in all_arrangements(height, cols[x])] for x in range(width)]
    image = [['?' for _ in range(width)] for _ in range(height)]
    image, finished, possible = consequences(image, rows, cols, all_rows, all_cols)
    if finished:
        return image
    while not finished:
        for y in range(height):
            for hyp_row in all_rows[y]:
                hyp_image = image.copy()
                hyp_image[y] = hyp_row
                new_image, finished, possible = consequences(hyp_image, rows, cols, all_rows, all_cols)
                if finished:
                    return new_image
                if not possible:
                    all_rows[y].remove(hyp_row)
        image, finished, possible = consequences(image, rows, cols, all_rows, all_cols)
        assert possible
        if finished:
            return image
        for x in range(width):
            for hyp_col in all_cols[x]:
                hyp_image = image.copy()
                hyp_imageT = T(hyp_image)
                hyp_imageT[x] = hyp_col
                new_image, finished, possible = consequences(T(hyp_imageT), cols, cols, all_rows, all_cols)
                if finished:
                    return new_image
                if not possible:
                    all_cols[x].remove(hyp_col)
        image, finished, possible = consequences(image, rows, cols, all_rows, all_cols)
        assert possible
        if finished:
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


