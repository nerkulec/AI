# wbite - pokazać

import random
from itertools import product
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable):
        l = len(iterable)
        for i, e in enumerate(iterable):
            print('{}/{}'.format(i, l))
            yield e
try:
    from util import timeit
except:
    from util_pypy import timeit
import pickle

gamma = 0.99

class Car:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self, a, o=None):
        if track[self.y][self.x] == 'o':
            if o is None:
                self.vx += random.choice([-1,0,1])
                self.vy += random.choice([-1,0,1])
            else:
                ox, oy = o
                self.vx += ox
                self.vy += oy
        ax, ay = a
        self.vx += ax
        self.vy += ay
        if self.vx > 3: self.vx=3
        if self.vx < -3: self.vx=-3
        if self.vy > 3: self.vy=3
        if self.vy < -3: self.vy=-3
        self.x += self.vx
        self.y += self.vy
        return self

    def copy(self):
        return Car(self.x, self.y, self.vx, self.vy)

    def __repr__(self):
        return 'Car({}, {}, {}, {})'.format(self.x, self.y, self.vx, self.vy)
    
    def __hash__(self):
        return hash((self.x, self.y, self.vx, self.vy))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.vx == other.vx and self.vy == other.vy

def next_S(s, a):
    f = track[s.y][s.x]
    if f == 'o':
        states = []
        for o in O:
            states.append(s.copy().move(a, o))
        return states
    elif f in 's#':
        return [s.copy().move(a)]
    assert False

def T(s, a, new_s): # assume possible transition
    if track[s.y][s.x] == 'o':
        return 1/9
    else:
        return 1

def reward(s, a, new_s):
    if not (0<=new_s.x<len(track[0]) and 0<=new_s.y<len(track)):
        return -100
    f = track[new_s.y][new_s.x]
    if f in '#os':
        return 0
    elif f=='.':
        return -100
    elif f=='e':
        return 100
    assert False

class Value:
    def __init__(self, track):
        self.track = track
        self.width = len(track[0])
        self.height = len(track)
        self.values = {s: 0 for s in S}

    def update_all(self):
        old_values = self.values.copy()
        for s in S:
            max_value = float('-inf')
            for a in A:
                value = 0
                for new_s in next_S(s, a):
                    r = reward(s, a, new_s)
                    if abs(r) == 100:
                        old_value = 0
                    else:
                        old_value = old_values[new_s]
                    value += T(s, a, new_s)*(r+gamma*old_value)
                if value>max_value:
                    max_value = value
            self.values[s] = max_value
        return max(abs(self.values[s]-old_values[s]) for s in S)

    def Q(self, s, a):
        q = 0
        for new_s in next_S(s, a):
            if new_s in S:
                q += T(s, a, new_s)*(reward(s, a, new_s) + gamma*self.values[new_s])
            else:
                q += T(s, a, new_s)*reward(s, a, new_s)
        return q

    def get_policy(self):
        self.policy = {}
        for s in S:
            a_r = [(a_, self.Q(s, a_)) for a_ in A] # move (-1, 0) has value 100.0 and move (1, 0) has value 100
            if len(set(x[1] for x in a_r)) >= 2:
                a = max(a_r, key=lambda x: x[1])[0]
                self.policy[s] = a
        return self.policy
        

if __name__ == '__main__':
    for track_num in [1,2,3,6,8,9,10,11]:
        with open('chars_test1/task{}.txt'.format(track_num)) as f:
            track = []
            for line in f:
                track.append(line[:-1])
            x, y = [(x,y) for y in range(len(track)) for x in range(len(track[0])) if track[y][x] == 's'][0]
            all_states = product(range(len(track[0])), range(len(track)), range(-3, 4), range(-3, 4))
            S = [Car(*s) for s in all_states if track[s[1]][s[0]] not in '.e']
            A = list(product([-1,0,1], repeat=2))
            O = list(product([-1,0,1], repeat=2))
            V = Value(track)
            max_change = 100000000
            while max_change>0.01:
                max_change = V.update_all()
                print(max_change)
            with open('chars_test1/policy_for_task{}.txt'.format(track_num), 'w') as output:
                P = V.get_policy()
                for s in P:
                    a = P[s]
                    output.write('{:2} {:2} {:2} {:2}    {:2} {:2}\n'.format(s.x, s.y, s.vx, s.vy, a[0], a[1]))
        