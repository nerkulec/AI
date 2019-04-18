import numpy as np

# #- pewny pełny
# .- pewny pusty
#  - nierozpatrzony
# %- niepewny pełny
# ,- niepewny pusty

explore = 0.05
maxloops = lambda w, h: w*h*6

def diff(orig, new):
    return sum([orig[i]^new[i] for i in range(len(orig))])

def all_arrangements(len_row, ch):
    def h(len_row, ch):
        sum_ch = sum(ch)
        len_ch = len(ch)
        if len_ch == 0:
            yield [0]*len_row
        else:
            for start in range(len_row-sum_ch-len_ch+1):
                for arrangement in h(len_row-ch[0]-start-1, ch[1:]):
                    yield [0]*start + [1]*ch[0] + [0] + arrangement
    for arr in h(len_row+1, ch):
        yield arr[:-1]

cache = dict()
def multi_opt_dist(row, ch):
    if (tuple(row), tuple(ch)) in cache:
        return cache[tuple(row), tuple(ch)]
    d = min(diff(row, new_row) for new_row in all_arrangements(len(row), ch))
    cache[tuple(row), tuple(ch)] = d
    return d

def legal(arr, row):
    for i in range(len(row)):
        if arr[i] == 0 and row[i] == '#':
            return False
        if arr[i] == 1 and row[i] == '.':
            return False
    return True

def step(rows, cols):
    ncols = len(cols)
    nrows = len(rows)
    image = [['#' if all(arr[i]==1 for arr in all_arrangements(ncols, row_ch)) else ' ' for i in range(ncols)] for row_ch in rows]
    # fill in cols if sure (all legal arrangements have it)
    return image
    
def nonogram(rows, columns, init=None):
    ncols = len(columns)
    nrows = len(rows)
    if init is None:
        image = [[np.random.choice([1]) for _ in range(ncols)] for _ in range(nrows)] # image[y][x]
    else:
        image = init

    cols_good = False
    rows_good = False

    counter = 0

    while(True):
        counter += 1

        if counter>maxloops(nrows, ncols):
            image = [[np.random.choice([0,1]) for _ in range(ncols)] for _ in range(nrows)]
            counter = 0

        bad_rows = []
        for y in range(nrows):
            row = image[y]
            if(multi_opt_dist(row, rows[y]) > 0):
                bad_rows.append(y)
        rows_good = len(bad_rows) == 0

        bad_columns = []
        for x in range(ncols):
            col = [row[x] for row in image]
            if(multi_opt_dist(col, columns[x]) > 0):
                bad_columns.append(x)
        cols_good = len(bad_columns) == 0

        if cols_good and rows_good:
            break

        c = np.random.choice(['row', 'column'])
        #c = True
        if(c == 'column'): # random bad col
            if cols_good:
                continue
            if np.random.random() < explore:
                x = np.random.choice(range(ncols))
            else:
                x = np.random.choice(bad_columns)
            best_ys = [0]
            best_delta = 100000000
            for y in range(nrows):
                dist1 = multi_opt_dist([row[x] for row in image], columns[x]) #dist col
                dist2 = multi_opt_dist(image[y], rows[y])                     #dist row
                image[y][x] ^= 1
                dist3 = multi_opt_dist([row[x] for row in image], columns[x]) #dist col
                dist4 = multi_opt_dist(image[y], rows[y])                     #dist row
                delta = dist3+dist4 - dist1-dist2
                image[y][x] ^= 1
                if delta < best_delta:
                    best_ys = [y]
                    best_delta = delta
                elif delta == best_delta:
                    best_ys.append(y)
            best_y = np.random.choice(best_ys)
            image[best_y][x] ^= 1

        else: # random bad row
            if rows_good:
                continue
            if np.random.random() < explore:
                y = np.random.choice(range(nrows))
            else:
                y = np.random.choice(bad_rows)
            best_xs = [0]
            best_delta = 100000000
            for x in range(ncols):
                dist = multi_opt_dist([row[x] for row in image], columns[x]) + multi_opt_dist(image[y], rows[y])
                image[y][x] ^= 1
                delta = multi_opt_dist([row[x] for row in image], columns[x]) + multi_opt_dist(image[y], rows[y]) - dist
                image[y][x] ^= 1
                if delta < best_delta:
                    best_xs = [x]
                    best_delta = delta
                elif delta == best_delta:
                    best_xs.append(x)
            best_x = np.random.choice(best_xs)
            image[y][best_x] ^= 1
        print(counter)
        draw(image)
    return image

def draw(image):
    for y in range(len(image)):
        for x in range(len(image[y])):
            print('#' if image[y][x] == 1 else '.', end='')
        print()
    print()

with open("zad_input.txt", "r") as in_f:
    with open("zad_output.txt", "w") as out_f:
        w, h = [int(x) for x in next(in_f).split()]
        r = [[int(el) for el in line.split()] for line in in_f]
        rows, cols = r[:w], r[w:]
        image = initial_analysis(rows, cols)
        image = nonogram(rows, cols)
        for y in range(len(image)):
            for x in range(len(image[y])):
                out_f.write('#' if image[y][x] == 1 else '.')
            out_f.write("\n")


