import os
import argparse


parser = argparse.ArgumentParser(description='Moonshine experiment customization.')
parser.add_argument('--data-path', type=str, help='The path the user would like to store their data')
parser.add_argument('--NIST-path', type=str, help="The path the user's NIST test suite lives.")
parser.add_argument('--Moonshine-path', type=str, help="The path the user's Moonshine root directory is located.")

args = parser.parse_args()


def initalize_experiment_information(data_path,nist_path,):
    pass


if __name__ == "__main__":
    print(args)