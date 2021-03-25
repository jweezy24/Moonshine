import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import entropy
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import AxesGrid
import argparse

data_path = os.environ['DATAPATH']
'''
Parses the NIST output files
output:
    a dictionary that will be the filename is the key and the value at the index is the pass rate.
'''


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
input:
    k = filename of a completed moonshine application
    s = the name of the set as a string
    data = the dictionary contiaing all filenames as keys
output:
    percentage of data remaining of the given file as a float
'''


def get_data_retained(k, s, data):
    total_before = 0
    for j in data.keys():
        if s in j.lower() and "before" in j:
            total_after = 0
            if total_before == 0:
                with open(f"{data_path}/{j}", 'r') as f:
                    for line in f:
                        for char in line:
                            total_before += 1

            with open(f"{data_path}/{k}", 'r') as f:
                for line in f:
                    for char in line:
                        total_after += 1

            percent = (total_before-total_after)/total_before
            return percent


'''
This method creates all of the comparison heatmaps for the NIST test pass rates.
input:
    data = ditctionary where the key is the filename and the value at the index is the pass rate of the file.
'''


def heatmap_passrate(data):
    # Font removed to have less dependencies
    # To readd this code, you must install latex and then uncomment the lines below

    # font = {'family' : 'normal',
    #         'size'   : 18}

    # plt.rc('font', **font)
    # plt.rc('text', usetex=True)

    sets = []
    passing_rates = examine_data(data)
    for s in data.keys():
        lst = s.split("_")
        if "10" in lst[0] or "11" in lst[0] or "12" in lst[0]:
            if lst[0][2:].lower() not in sets and "before" not in s:
                sets.append(lst[0][2:].lower())
                print(lst)
        else:
            if lst[0][1:].lower() not in sets and "before" not in s:
                sets.append(lst[0][1:].lower())

    heats = [[[0 for i in range(0, 10)] for i in range(0, 11)]
             for i in range(0, len(sets))]

    sets.sort()
    mapping = 0
    discard = 0
    for s in range(0, len(sets)):
        for k in data.keys():
            if sets[s] in k.lower() and "before" not in k:
                discard = int(k[0])
                for ele in k.split("_"):
                    if "after" in ele:
                        ele = ele.replace(".txt", '').replace("after", "")
                        mapping = int(ele)
                        check = True
                        break
                heats[s][mapping-2][discard] = passing_rates[k]

    fig = plt.figure()

    grid = AxesGrid(fig, 111, nrows_ncols=(1, len(sets)),
                    axes_pad=0.1, cbar_mode="single")

    x_ticks = [1, 3, 5, 7, 9]
    x_ticksl = ["3", "5", "7", "9", "11"]

    i = 0
    for val, ax in zip(heats, grid):
        im = ax.imshow(val, vmin=0, vmax=1)
        proper_name = get_proper_name(sets[i])
        ax.title.set_text(proper_name)
        ax.set(aspect='equal')
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_ticksl)
        ax.set_ylim([0, 10])
        i += 1
    grid.cbar_axes[0].colorbar(im, ticks=[0, 0.5, 1])

    plt.xlabel("Bit Sequence Length")
    plt.ylabel("Bits Discarded")
    plt.ylim(0, 11)
    if not os.path.isdir("./figures"):
        os.system("mkdir ./figures")
    plt.savefig("./figures/passrate.pdf")

    print(sets)


'''
This method creates all of the comparison heatmaps for the data retention after applying moonshine.
input:
    data = ditctionary where the key is the filename and the value at the index is the pass rate of the file.
'''


def heatmap_data_ret(data):
    # Font removed to have less dependencies
    # To readd this code, you must install latex and then uncomment the lines below

    # font = {'family' : 'normal',
    #         'size'   : 18}

    # plt.rc('font', **font)
    # plt.rc('text', usetex=True)

    sets = []
    sets2 = []
    passing_rates = examine_data(data)
    for s in data.keys():
        lst = s.split("_")
        if "10" in lst[0] or "11" in lst[0] or "12" in lst[0]:
            if lst[0][2:].lower() not in sets and "before" not in s:
                sets.append(lst[0][2:].lower())
                print(lst)
        else:
            if lst[0][1:].lower() not in sets and "before" not in s:
                sets.append(lst[0][1:].lower())

    heats = [[[0 for i in range(0, 10)] for i in range(0, 11)]
             for i in range(0, len(sets))]
    sets.sort()
    mapping = 0
    discard = 0
    for s in range(0, len(sets)):
        for k in data.keys():
            if sets[s] in k.lower() and "before" not in k:
                print(get_data_retained(k, sets[s], data))
                discard = int(k[0])
                for ele in k.split("_"):
                    if "after" in ele:
                        ele = ele.replace(".txt", '').replace("after", "")
                        mapping = int(ele)
                        check = True
                        break
                heats[s][mapping-2][discard] = 1 - \
                    get_data_retained(k, sets[s], data)

    fig = plt.figure()
    grid = AxesGrid(fig, 111, nrows_ncols=(1, len(sets)),
                    axes_pad=0.1, cbar_mode="single")

    i = 0
    x_ticks = [1, 3, 5, 7, 9]
    x_ticksl = ["3", "5", "7", "9", "11"]
    for val, ax in zip(heats, grid):
        im = ax.imshow(val, vmin=0, vmax=0.5)
        proper_name = get_proper_name(sets[i])
        ax.title.set_text(proper_name)
        ax.set(aspect='equal')
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_ticksl)
        ax.set_ylim([0, 10])
        i += 1
    grid.cbar_axes[0].colorbar(im, ticks=[0, 0.5, 1])

    plt.ylim(0, 11)
    if not os.path.isdir("./figures"):
        os.system("mkdir ./figures")
    plt.savefig("./figures/data_retention.pdf")


'''
This method will return the proper label based on the data set's file name.
input:
    name = a string of a filename of which gets mapped to a label.
'''


def get_proper_name(name):
    names = ['officeSH', 'audio', 'OfficeTR', 'AeroKey',
             'raw', 'CarSH', 'MobileTR', 'MobileS']
    if name == "office1".lower():
        return "Office 1"
    elif name == "audio".lower():
        return "Audio"
    elif name == "Office2".lower():
        return "Office 2"
    elif name == "rf".lower():
        return "RF Frequencies"
    elif name == "voltkey".lower():
        return "Voltkey"
    elif "car".lower() in name:
        return "Car"
    elif name == "Mobile1".lower():
        return "Mobile 1"
    elif name == "Mobile2".lower():
        return "Mobile 2"


def examine_data(data):
    failure_rate = {}
    for key in data:
        passes = 0
        fails = 0
        nonoverlapping = 126
        nonoverlapping_fails = 0
        for ele in data.get(key):
            stars = [i for i, e in enumerate(ele) if '*' in e]
            if (11 in stars and 13 in stars) and 'NonOverlappingTemplate\n' not in ele[-1] and "RandomExcursionsVariant" not in ele[-1]:
                fails += 1
            elif 'NonOverlappingTemplate\n' in ele[-1] and (11 in stars and 13 in stars):
                nonoverlapping_fails += 1
            elif 'NonOverlappingTemplate\n' in ele[-1] or "RandomExcursionsVariant" in ele[-1]:
                continue
            else:
                passes += 1

        if nonoverlapping_fails/nonoverlapping >= .5:
            fails += 1
        else:
            passes += 1

        try:
            failure_rate[key] = (passes/(passes+fails))
        except:
            failure_rate[key] = "NA"

    return failure_rate
