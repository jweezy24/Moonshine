import os
from subprocess import Popen, PIPE
from create_heat_maps import *


NIST_test_path = os.environ['NISTPATH']
data_path = os.environ['DATAPATH']
moonshine_path = os.environ["MOONSHINE"]

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
                       stdout=PIPE, cwd=f"{NIST_test_path}")
            p2 = Popen(["./assess", f"{bit_stream_len}"],
                       stdin=p1.stdout, stdout=PIPE, cwd=f"{NIST_test_path}")
            output = p2.communicate()[0]
            os.system(
                f"cp {NIST_test_path}/experiments/AlgorithmTesting/finalAnalysisReport.txt nist_test_results/{file_}")


def clear_out_old_tests():

    for (dirpath, dirnames, filenames) in os.walk("nist_test_results"):
        for file_ in filenames:
            if "after" in file_ and "before" not in file_:
                print(f"rm nist_test_results/{file_}")
                os.system(f"rm nist_test_results/{file_}")

    for (dirpath, dirnames, filenames) in os.walk(f"{NIST_test_path}/data"):
        for file_ in filenames:
            if "after" in file_ and "before" not in file_:
                print(f"rm {NIST_test_path}/data/{file_}")
                os.system(f"rm {NIST_test_path}/data/{file_}")

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
