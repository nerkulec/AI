import numpy as np

explore = 0.05
maxloops = 1000

def longest_sequence(l):
    longest = 0
    streak = 0
    for i in range(len(l)):
        if l[i] == 1:
            streak += 1
        else:
            if streak>longest:
                longest = streak
            streak = 0
    if streak>longest:
        longest = streak
    return longest

def opt_dist(colors, dist):
    count = dist + colors.count(1) - 2*(colors[:dist].count(1))
    min_count = count
    for i in range(1, len(colors)-dist+1):
        count += 2*colors[i-1] - 2*colors[i+dist-1]
        if count < min_count:
            min_count = count
    return min_count

def nonogram(rows, columns, init=None):
    ncols = len(columns)
    nrows = len(rows)
    if init is None:
        image = [[np.random.choice([0, 1]) for _ in range(ncols)] for _ in range(nrows)] # image[y][x]
    else:
        image = init

    cols_good = False
    rows_good = False

    counter = 0

    while(True):
        counter += 1

        if counter>maxloops:
            image = [[np.random.choice([0, 1]) for _ in range(ncols)] for _ in range(nrows)]
            counter = 0

        bad_rows = []
        for y in range(nrows):
            row = image[y]
            if(not(longest_sequence(row) == rows[y] == row.count(1))):
                bad_rows.append(y)
        rows_good = len(bad_rows) == 0

        bad_columns = []
        for x in range(ncols):
            col = [row[x] for row in image]
            if(not(longest_sequence(col) == columns[x] == col.count(1))):
                bad_columns.append(x)
        cols_good = len(bad_columns) == 0

        if cols_good and rows_good:
            break

        c = np.random.choice(['row', 'column'])
        #c = True
        if(c is 'column'): # random bad col
            if cols_good:
                continue
            if np.random.random() < explore:
                x = np.random.choice(range(ncols))
            else:
                x = np.random.choice(bad_columns)
            best_ys = [0]
            best_delta = 100000000
            for y in range(nrows):
                dist1 = opt_dist([row[x] for row in image], columns[x]) #dist col
                dist2 = opt_dist(image[y], rows[y])                     #dist row
                image[y][x] ^= 1
                dist3 = opt_dist([row[x] for row in image], columns[x]) #dist col
                dist4 = opt_dist(image[y], rows[y])                     #dist row
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
                dist = opt_dist([row[x] for row in image], columns[x]) + opt_dist(image[y], rows[y])
                image[y][x] ^= 1
                delta = opt_dist([row[x] for row in image], columns[x]) + opt_dist(image[y], rows[y]) - dist
                image[y][x] ^= 1
                if delta < best_delta:
                    best_xs = [x]
                    best_delta = delta
                elif delta == best_delta:
                    best_xs.append(x)
            best_x = np.random.choice(best_xs)
            image[y][best_x] ^= 1

        draw(image)
    return image

def draw(image):
    for y in range(len(image)):
        for x in range(len(image[y])):
            print('#' if image[y][x] == 1 else '.', end='')
        print()
    print()

# with open("zad5_input.txt", "r") as in_f:
#     with open("zad5_output.txt", "w") as out_f:
#         w, h = [int(x) for x in next(in_f).split()]
#         r = [int(x) for x in in_f]
#         rows, cols = r[:w], r[w:]
#         image = nonogram(rows, cols)
#         for y in range(len(image)):
#             for x in range(len(image[y])):
#                 out_f.write('#' if image[y][x] == 1 else '.')
#             out_f.write("\n")


