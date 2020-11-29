import numpy as np
from glob import glob
import os

base_path = os.path.join('dataset', '*/*.npz')

file_list = glob(base_path)

for file_path in file_list:
    data = np.load(file_path)
    inputs = data['inputs']
    outputs = data['outputs']

    for input, output in zip(inputs, outputs):
        print(input)
        print(output)
        print('=======')

    print('=================')
    break