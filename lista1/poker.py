import numpy as np

kolory = ['P', 'I', 'T', 'A']
figury = [x for x in range(11, 15)]
blotki = [x for x in range(2, 11)]

talia_f = [{'rank':f, 'suit':k} for f in figury for k in kolory]
talia_b = [{'rank':b, 'suit':k} for b in blotki for k in kolory]

def value(hand):
    """
    poker - 8
    kareta - 7
    full - 6
    kolor - 5
    strit - 4
    trójka - 3
    dwie pary - 2
    para - 1
    figura - 0
    """
    hand = sorted(hand, key=lambda c: c['rank'])
    ranks = [card['rank'] for card in hand]
    suits = [card['suit'] for card in hand]
    ordered = all([ranks[i]+1 == ranks[i+1] for i in range(4)])
    colored = all([suits[0] == suits[i] for i in range(1, 5)])
    four = max(ranks.count(ranks[0]), ranks.count(ranks[1]))
    three = max(four, ranks.count(ranks[2]))
    two = max(three, ranks.count(ranks[3]))
    four = four >= 4
    three = three >= 3
    two = two >= 2
    different = len(set(ranks))
    if ordered:
        if colored:
            return 8
        return 4
    if colored:
        return 5
    if four:
        return 7
    if three and different == 2:
        return 6
    if three and different == 3:
        return 3
    if two and different == 3:
        return 2
    if two and different == 4:
        return 1
    return 0

def test(okrojona_talia_b):
    bwins = 0
    total_games = 1000
    for _ in range(total_games):
        f_hand = np.random.choice(talia_f, 5, replace=False)
        b_hand = np.random.choice(okrojona_talia_b, 5, replace=False)
        if value(b_hand) > value(f_hand) + 0.5:
            bwins += 1

    print(f'Blotkarz wygrał {bwins/total_games:.2%} gier')

def get_all_hands(deck):
    l = len(deck)
    for a in range(0, l):
        for b in range(a+1, l):
            for c in range(b+1, l):
                for d in range(c+1, l):
                    for e in range(d+1, l):
                        yield [deck[a], deck[b], deck[c], deck[d], deck[e]]

def count():
    counts_b = [0]*9
    counts_f = [0]*9
    lb = 0
    lf = 0
    for hand in get_all_hands(talia_b):
        counts_b[value(hand)] += 1
        lb += 1
    for hand in get_all_hands(talia_f):
        counts_f[value(hand)] += 1
        lf += 1
    c = 0
    for j in range(9):
        for i in range(j+1, 9):
            c += counts_b[i]*counts_f[j]
    print(c/(lb*lf))

count()

# test(talia_b)
# test([x for x in talia_b if x['suit'] == 'P']) # jeden kolor
# test([x for x in talia_b if x['suit'] == 'P' or x['suit'] == 'I']) # dwa kolory
# test([x for x in talia_b if x['rank'] >= 7]) # 7+
# test([x for x in talia_b if x['rank'] >= 8]) # 8+
# test([x for x in talia_b if x['rank'] >= 9]) # 9+
# test([x for x in talia_b if x['rank'] >= 6 and x['suit'] == 'P']) # 5 kart poker
# test([x for x in talia_b if x['rank'] >= 6 and x['suit'] == 'P' or x['suit'] == 'I']) # 10 kart dwa pokery
# test([x for x in talia_b if x['rank'] >= 8 and x['suit'] != 'P']) # trzy kolory 8+
# test([x for x in talia_b if x['rank'] >= 9 and x['suit'] != 'P']) # trzy kolory 9+ (6 kart)
# test([x for x in talia_b if (x['suit'] == 'P' or x['suit'] == 'I') and x['rank'] >= 6]) # dwa kolory 6+
