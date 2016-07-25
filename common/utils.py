from time import time


def timeit(func):
    def wrapper(*args):
        start = time()
        result = func(*args)
        end = time()
        print('{0}(): Execution time: {1:2f} s'.format(func.__name__, end - start))
        return result
    return wrapper