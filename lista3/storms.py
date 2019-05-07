# wbite - pokazać

def B(i,j):
    return 'B_%d_%d' % (i,j)

def square(i, j):
    return [B(i,j), B(i+1,j), B(i,j+1), B(i+1,j+1)]

def srow(i, j):
    return [B(i,j), B(i+1,j), B(i+2,j)]

def row(j, w):
    return [B(i,j) for i in range(w)]

def scol(i, j):
    return [B(i,j), B(i,j+1), B(i,j+2)]

def col(i, h):
    return [B(i,j) for j in range(h)]

def squares(w, h):
    return [square(i, j) for j in range(h-1) for i in range(w-1)]

def srows(w, h):
    return [srow(i,j) for i in range(w-2) for j in range(h)]

def scols(w, h):
    return [scol(i,j) for i in range(w) for j in range(h-2)]

def p_in(el, s):
    return f'    tuples_in([[{", ".join(el)}]], {s}), '

def sums_to(arr, num):
    return f'    {" + ".join(arr)} #= {num},'

def storms(rows_input, cols_input, triples):
    writeln(':- use_module(library(clpfd)).')
    
    w = len(rows_input)
    h = len(cols_input)
    
    bs = [ B(i,j) for i in range(w) for j in range(h)]
    
    writeln('solve([' + ', '.join(bs) + ']) :- ')
    possible = [[0,0,0], [0,0,1], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]] # all but 010
    possible_sq = [[0,0,0,0], [0,0,0,1], [0,0,1,0], [0,0,1,1], [0,1,0,0], [0,1,0,1], [1,0,0,0], [1,0,1,0], [1,1,0,0], [1,1,1,1]]
    for b in bs:
        output.write(f'    {b} in 0..1, ')
    for s in squares(w, h):
        writeln(p_in(s, possible_sq))
    for c in scols(w, h):
        writeln(p_in(c, possible))
    for r in srows(w, h):
        writeln(p_in(r, possible))
    for j in range(h):
        writeln(sums_to(row(j, w), cols_input[j]))
    for i in range(w):
        writeln(sums_to(col(i, h), rows_input[i]))
    for c in triples:
        writeln(f'    {B(c[0], c[1])} #= {c[2]},')

    writeln('    labeling([ff], [' +  ', '.join(bs) + ']).' )
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")

def writeln(s):
    output.write(s + '\n')

with open('zad_input.txt') as input_file:
    txt = input_file.readlines()
with open('zad_output.txt', 'w') as output:
    rows_input = list(map(int, txt[0].split()))
    cols_input = list(map(int, txt[1].split()))
    triples = []

    for i in range(2, len(txt)):
        if txt[i].strip():
            triples.append(list(map(int, txt[i].split())))

    storms(rows_input, cols_input, triples)            

