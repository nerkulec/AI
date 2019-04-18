with open('origin2.txt', 'r') as line_input:
    with open('origin.txt', 'w') as line_output:
        for line in line_input:
            if line == '\n':
                continue
            for c in ',.;:!?@#$%^&*()-_+=—…«»':
                line = line.replace(c, '')
            a = " ".join(line.strip().lower().split())+'\n'
            line_output.write(a)