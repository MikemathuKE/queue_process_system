from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        results = []
        for i in range (1, 5):
            result = pool.apply_async(f, (i,))
            results.append(result)
        for result in results:
            print(result.get(timeout=1))        # raises multiprocessing.TimeoutError