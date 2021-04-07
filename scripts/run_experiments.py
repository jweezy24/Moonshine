'''
Copyright 2021 Jack West

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import os
import wget
import zipfile
import argparse
from subprocess import Popen, PIPE

nist_url = "https://csrc.nist.gov/CSRC/media/Projects/Random-Bit-Generation/documents/sts-2_1_2.zip"
moonshine_data_url = "https://zenodo.org/record/4579975/files/moonshine.zip"

parser = argparse.ArgumentParser(
    description='Moonshine experiment customization.')
parser.add_argument('--data_path', default='', type=str,
                    help='The path the user would like to store their data')
parser.add_argument('--nist_path', default='', type=str,
                    help="The path the user's NIST test suite lives.")
parser.add_argument('--Moonshine_path', default='', type=str,
                    help="The path the user's Moonshine root directory is located.")


args = parser.parse_args()


nist_test_path = ''
data_path = ''
moonshine_path = ''

'''
Runs Moonshine on all available text files in the user's data_path
'''


def part1():

    for i in range(2, 13):
        for discard in range(0, 13):
            for (dirpath, dirnames, filenames) in os.walk(f"{data_path}"):
                for file_ in filenames:
                    if 'before' in file_:
                        new_file_name = file_.replace("before", f"after{i}")
                        new_file_name = f"{discard}{new_file_name}"
                        os.system(
                            f"./Moonshine.o {i} {i-1} {discard} {data_path}/{file_} {data_path}/{new_file_name}")

                break


def part2():

    for (dirpath, dirnames, filenames) in os.walk(data_path):
        for file_ in filenames:
            path2 = f"{data_path}/{file_}"
            p1 = Popen(["cat", f"{path2}"], stdout=PIPE,
                       cwd=f"{moonshine_path}")
            p2 = Popen(["wc", "-c"], stdin=p1.stdout,
                       stdout=PIPE, cwd=f"{moonshine_path}")
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            output = int(p2.communicate()[0].decode('UTF-8'))
            bit_stream_len, bits = get_bit_stream_len(output)
            if bit_stream_len == 0 or bits == 0:
                continue
            print(f"{file_}:\t{output}")

            p1 = Popen(["echo", f"0\n{data_path}/{file_}\n1\n0\n{bits}\n0\n"],
                       stdout=PIPE, cwd=f"{nist_test_path}")
            p2 = Popen(["./assess", f"{bit_stream_len}"],
                       stdin=p1.stdout, stdout=PIPE, cwd=f"{nist_test_path}")
            output = p2.communicate()[0]
            os.system(
                f"cp {nist_test_path}/experiments/AlgorithmTesting/finalAnalysisReport.txt nist_test_results/{file_}")


def clear_out_old_tests():

    for (dirpath, dirnames, filenames) in os.walk("nist_test_results"):
        for file_ in filenames:
            if "after" in file_ and "before" not in file_:
                print(f"rm nist_test_results/{file_}")
                os.system(f"rm nist_test_results/{file_}")

    for (dirpath, dirnames, filenames) in os.walk(f"{nist_test_path}/data"):
        for file_ in filenames:
            if "after" in file_ and "before" not in file_:
                print(f"rm {nist_test_path}/data/{file_}")
                os.system(f"rm {nist_test_path}/data/{file_}")

    for (dirpath, dirnames, filenames) in os.walk(f"{data_path}"):
        for file_ in filenames:
            if "after" in file_ and "before" not in file_:
                print(f"rm {data_path}/{file_}")
                os.system(f"rm {data_path}/{file_}")


def get_bit_stream_len(length):

    bit_stream_len = int(length/1000) * 10
    if bit_stream_len > 1000:
        return (bit_stream_len, 100)
    else:
        divisor = 90
        while bit_stream_len < 1000:
            bit_stream_len = int(length/divisor)
            divisor -= 10
            if divisor == 0:
                break
        if divisor == 0:
            return(0, 0)
    return(bit_stream_len, divisor)


def execute_experiments():
    # Delete past experiment files
    clear_out_old_tests()
    # Run Moonshine on all binary streams in the data path
    part1()
    # run the NIST tests on the files generated from part1
    part2()
    # Parses all files in the nist_test_results folder
    data = parse_files()
    # Generates heatmaps of nist test pass rates
    heatmap_passrate(data)
    # Generates heatmaps of data retention after using Moonshine
    heatmap_data_ret(data)


def install(data_path, nist_path, moonshine_path):

    if not os.path.exists("./nist_test_results"):
        os.system("mkdir ./nist_test_results")

    # wgetting NIST test suite from website
    if nist_path != "":
        if os.path.isdir(nist_path):
            wget.download(nist_url, out=nist_path)
            nist_path += "/sts-2_1_2.zip"
        else:
            raise Exception("Given path is not a directory.")
    else:
        wget.download(nist_url, out="./")
        nist_path = os.path.abspath("./sts-2_1_2.zip")

    # Extract files within the zip
    with zipfile.ZipFile(nist_path, 'r') as zip_ref:
        zip_ref.extractall("./")

    os.remove(nist_path)
    nist_path = os.path.abspath("./sts-2.1.2/sts-2.1.2")

    print(f"\n{nist_path}\n")
    print(f"cd {nist_path} & make")

    # install the NIST suite
    os.system(f"cd {nist_path} && make")

    if data_path != "":
        if os.path.isdir(data_path):
            wget.download(moonshine_data_url, out=data_path)
            data_zip = os.path.abspath(f"{data_path}/moonshine.zip")
        else:
            raise Exception("Given path is not a directory.")
    else:
        if not os.path.exists("./data"):
            os.system("mkdir ./data")

        wget.download(moonshine_data_url, out="./data")
        data_zip = os.path.abspath("./data/moonshine.zip")
        data_path = os.path.abspath("./data/")

    with zipfile.ZipFile(data_zip, 'r') as zip_ref:
        zip_ref.extractall(f"{data_path}")

    os.remove(f"{data_zip}")

    if moonshine_path != "":
        if not os.path.isdir(moonshine_path):
            raise Exception("Given path is not a directory.")
    else:
        moonshine_path = os.path.abspath("./")
        os.system("make")

    os.environ["NISTPATH"] = nist_path
    os.environ["DATAPATH"] = data_path
    os.environ["MOONSHINE"] = moonshine_path


if __name__ == "__main__":
    install(args.data_path, args.nist_path, args.Moonshine_path)
    nist_test_path = os.environ['NISTPATH']
    data_path = os.environ['DATAPATH']
    moonshine_path = os.environ["MOONSHINE"]
    from create_heat_maps import *
    execute_experiments()
