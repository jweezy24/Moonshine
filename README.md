# Moonshine

Moonshine is a randomness distiller. 
The purpose of Moonshine is to be applied to a dataset after bit extraction to increase the randomness of a bit stream.
Ideally, Moonshine would be attached dynamically after determining which parameters create the most randomness for your input stream.

## Dependencies

There are two components to this repository.
This repository contains the C code for Moonshine's algorithm and python scripts to run experiments on ascii bit streams.
To compile the C code one has to have GCC, the python code is writen in python3.

### Build Moonshine

Moonshine does not have any inherient requirements.
On any system that has GCC, the user needs to just compile the code using this command, `make`.
That will create an output file called Moonshine.o, we will explain how to use Moonshine on it's own further down in this readme.

### Experiments' Dependencies

The python experiments do have a few dependencies due to the analysis we preform after running the experiments.
Therefore to install the dependencies run, `pip install -r ./requirements.txt`.

    