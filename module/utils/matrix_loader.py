import numpy as np
import json

def load_batch(path):
    return np.load(path)

def load_attr(path):
    sul = []
    m=np.load(path)
    for i in range(100):
        sul.append([i, m[i,2]])

    return sul
