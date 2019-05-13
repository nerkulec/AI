from time import time
from functools import wraps
from tqdm import tqdm
from random import randrange as rand

def timeit(func, runs={}, times={}):
    if func=='SHOW':
        sum_times = sum(times[k] for k in times)
        for fun, t in times.items():
            print(f'{fun:14} took {t*1.0:>5.2f} seconds in {runs[fun]:8} runs which is {t/sum_times:>6.2%} total time')
    else:
        name = func.__name__
        if name not in runs:
            runs[name] = 0
            times[name] = 0
        @wraps(func)
        def timed(*args, silent=True, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            end = time()
            runs[name] += 1
            times[name] += end-start
            if not silent:
                print(f'{end-start}')
            return result
        return timed

def cacheit(func): 
    # TODO: make it possible to use a file to cache
    # TODO: change lists to tuples
    @wraps(func)
    def cached(*args, cache={}, **kwargs):
        if args in cache:
            return cache[args]
        else:
            value = func(*args, **kwargs)
            cache[args] = value
            return value
    return cached

if __name__ == '__main__':

    @cacheit
    def fact_cached(n):
        result = 1
        for i in range(n):
            result *= i
            result %= 1000
        return result

    def fact(n):
        result = 1
        for i in range(n):
            result *= i
            result %= 1000
        return result

    @cacheit
    def exp2_cached(n):
        result = 1
        for i in range(n):
            result *= 2
            result %= 1000
        return result

    def exp2(n):
        result = 1
        for i in range(n):
            result *= 2
            result %= 1000
        return result

    @timeit
    def test_exp2(reps, arg, cached):
        v = 0
        for i in tqdm(range(reps)):
            if cached:
                v += exp2_cached(arg+rand(arg))
            else:
                v += exp2(arg+rand(arg))
            v %= 10000
        return v

    @timeit
    def test_fact(reps, arg, cached):
        v = 0
        for i in tqdm(range(reps)):
            if cached:
                v += fact_cached(arg+rand(arg))
            else:
                v += fact(arg+rand(arg))
            v %= 10000
        return v

    test_exp2(10000, 1000, True)
    test_exp2(10000, 1000, False)
    test_fact(10000, 1000, True)
    test_fact(10000, 1000, False)

    timeit('SHOW')