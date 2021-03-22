import os
from subprocess import Popen, PIPE


NIST_test_path = os.environ['NIST-PATH']
data_path = os.environ['DATA-PATH']
moonshine_directory_absolute_path = os.environ["MOONSHINE"]

'''
Runs Moonshine on all available text files in the user's data_path
'''
def part1():
    
    for i in range(2,13):
        for discard in range(0,13):
            for (dirpath, dirnames, filenames) in os.walk("./data"):
                for file_ in filenames:
                    if 'before' in file_:
                        new_file_name = file_.replace("before",f"after{i}")
                        new_file_name = f"{discard}{new_file_name}"
                        os.system(f"./Moonshine.o {i} {i-1} {discard} {data_path}/{file_} {data_path}/{new_file_name}")
                    
                break

def part2():
    path = 'Other/sts-2.1.2/sts-2.1.2/data'
    file_size_example = ''' ./data/acc_after.txt | wc -c'''

     
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file_ in filenames:
            path2 = f"{path}/{file_}"
            p1 = Popen(["cat", f"{path2}"], stdout=PIPE,cwd=f"{moonshine_directory_absolute_path}")
            p2 = Popen(["wc", "-c"], stdin=p1.stdout, stdout=PIPE,cwd=f"{moonshine_directory_absolute_path}" )
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            output = int(p2.communicate()[0].decode('UTF-8'))
            bit_stream_len,bits = get_bit_stream_len(output)
            if bit_stream_len == 0 or bits == 0:
                continue
            print(f"{file_}:\t{output}")
            
            p1 = Popen(["echo", f"0\n./data/{file_}\n1\n0\n{bits}\n0\n" ], stdout=PIPE,cwd=f"{NIST_test_path}")
            p2 = Popen(["./assess", f"{bit_stream_len}"], stdin=p1.stdout, stdout=PIPE,cwd=f"{NIST_test_path}")
            output = p2.communicate()[0]
            print(output)
            os.system(f"cp {NIST_test_path}experiments/AlgorithmTesting/finalAnalysisReport.txt nist_test_results/{file_}")

def clear_out_old_tests():

    for (dirpath, dirnames, filenames) in os.walk("nist_test_results"):
        for file_ in filenames:
                if "after" in file_ and "before" not in file_:
                    print(f"rm {path2}/{file_}")
                    os.system(f"rm {path}/{file_}")
    
    for (dirpath, dirnames, filenames) in os.walk(NIST_test_path):
        for file_ in filenames:
                if "after" in file_ and "before" not in file_:
                    print(f"rm {path2}/{file_}")
                    os.system(f"rm {path2}/{file_}")
    


def execute_experiments(path_to_data, path_to_nist_executable, path_to_results):
    clear_out_old_tests()
    part1()
    part2()

