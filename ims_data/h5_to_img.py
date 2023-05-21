import sys
import random

import numpy as np
import matplotlib.pyplot as plt

import png 
import h5py

usage = "usage: python3 h5_to_img.py  h5_file_path  h5_dataset_name  img_format[='png']  num_samples[=5]  output_file_prefix[='img_from_h5']"
if len(sys.argv) < 3  or  '?' in sys.argv[1]:
    print(usage)
    exit()
    

h5_file_path       = sys.argv[1]
h5_dataset_name    = sys.argv[2]
img_format         = sys.argv[3]  if  len(sys.argv) > 3  else  'png'
num_samples        = sys.argv[4]  if  len(sys.argv) > 4  else  5
output_file_prefix = sys.argv[5]  if  len(sys.argv) > 5  else  'img_from_h5'

images = h5py.File(h5_file_path, "r").get(h5_dataset_name)

sample_indices = random.sample(range(images.shape[1]), num_samples)

for i,ind in enumerate(sample_indices):
    
    plt.imsave(f"{output_file_prefix}_{i}.{img_format}", images[0,ind,:,:,:])

