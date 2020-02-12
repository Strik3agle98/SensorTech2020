import numpy as np

while True:
    L = [int(i) for i in input().split()]
    L = np.array(L)
    S = np.sum(L)
    print(L/S)