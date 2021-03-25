import os
import wget
import zipfile
import argparse


NIST_url = "https://csrc.nist.gov/CSRC/media/Projects/Random-Bit-Generation/documents/sts-2_1_2.zip"
moonshine_data_url = "https://zenodo.org/record/4579975/files/moonshine.zip"

parser = argparse.ArgumentParser(description='Moonshine experiment customization.')
parser.add_argument('--data_path', type=str, help='The path the user would like to store their data')
parser.add_argument('--NIST_path', type=str, help="The path the user's NIST test suite lives.")
parser.add_argument('--Moonshine_path', type=str, help="The path the user's Moonshine root directory is located.")

args = parser.parse_args()


def install(data_path,nist_path,moonshine_path):
    
    if not os.path.exists("./nist_test_results"):
        os.system("mkdir ./nist_test_results")
    
    # wgetting NIST test suite from website
    if nist_path != "":
        if os.path.isdir(nist_path): 
            wget.download(NIST_url, out=nist_path)
            nist_path += "/sts-2_1_2.zip"
        else:
            raise Exception("Given path is not a directory.")
    else:
        wget.download(NIST_url, out="./")
        nist_path = os.path.abspath("./sts-2_1_2.zip")
    
    #Extract files within the zip
    with zipfile.ZipFile(nist_path, 'r') as zip_ref:
        zip_ref.extractall("./")
    
    os.remove(nist_path)
    nist_path = os.path.abspath("./sts-2.1.2/sts-2.1.2")
    
    print(f"\n{nist_path}\n")
    print(f"cd {nist_path} & make")

    #install the NIST suite
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
    install(args.data_path, args.NIST_path, args.Moonshine_path)
    from run_experiments import *
    execute_experiments()