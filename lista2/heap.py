class Heap:
    def __init__(self):
        self.tab = ['bartek']
    
    def push(self, a):
        self.tab.append(a)
        pos = len(self.tab)-1
        while pos > 1:
            if self.tab[pos][0] < self.tab[pos//2][0]:
                self.tab[pos], self.tab[pos//2] =  self.tab[pos//2], self.tab[pos]
                pos = pos // 2
            else:
                break
    
    def pop(self):
        a = self.tab[1]
        self.tab[1], self.tab[len(self.tab)-1] = self.tab[len(self.tab)-1], self.tab[1]
        self.tab.pop()
        pos = 1
        while 2*pos < len(self.tab):
            mn = pos*2
            if 2*pos+1 < len(self.tab):
                if self.tab[2*pos+1] < self.tab[mn]:
                    mn = pos*2+1
            if self.tab[pos][0] > self.tab[mn][0]:
                self.tab[pos], self.tab[mn] =  self.tab[mn], self.tab[pos]
                pos = mn
            else:
                break
        return a

    def __bool__(self):
        return len(self.tab) > 1
