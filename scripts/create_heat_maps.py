import os,sys
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import entropy
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import AxesGrid
import argparse

'''Parses the NIST output files'''

def parse_files():
    data_to_file = {}
    for (dirpath, dirnames, filenames) in os.walk('./nist_test_results'):
        for file_name in filenames:
            # if "audio" in file_name:
            with open(f'{dirpath}/{file_name}', 'r') as f:
                all_data = []
                for line in f:
                    if '/' in line and '<' not in line:
                        split_line = line.split(' ')
                        data = []
                        for ele in split_line:
                            if ele != '':
                                data.append(ele)
                        all_data.append(data)
                data_to_file[file_name] = all_data

    return data_to_file

'''
Calculates difference in bits in in the file before and after applying Moonshine
'''

def get_data_retained(k, s, sets, data):
    for j in data.keys():
        if s in j.lower() and "before" in j:
            total_before = 0
            total_after = 0
            with open(f"{path_to_files}/{j}", 'r') as f:
                for line in f:
                    for char in line:
                        total_before+=1
            with open(f"{path_to_files}/{k}", 'r') as f:
                for line in f:
                    for char in line:
                        total_after+=1

            percent = (total_before-total_after)/total_before
            return percent