# Moonshine

Moonshine is a randomness distiller. 
The purpose of Moonshine is to be applied to a dataset after bit extraction to increase the randomness of a bit stream.
Ideally, Moonshine would be attached dynamically after determining which parameters create the most randomness for your input stream.

## Dependencies

There are two components to this repository.
This repository contains the C code for Moonshine's algorithm and python scripts to run experiments on ascii bit streams.
Tools needed to run the code:

    - `GCC`
    - `Python3`
    - `make`

To properly generate the graphs for the NIST tests you must download the NIST test suite for randomness from [here](https://csrc.nist.gov/projects/random-bit-generation/documentation-and-software).


### Experiments' Dependencies

The python experiments do have a few dependencies due to the analysis we preform after running the experiments.
Therefore to install the dependencies run, `pip install -r ./requirements.txt`.

If you would like to generate your own graphs you will need the NIST test suite discussed above.
You also need to set up three enviromental variables.


### Build Moonshine

Moonshine does not have any inherient requirements.
On any system that has GCC, the user needs to just compile the code using this command, `make`.
That will create an output file called `Moonshine.o`, we will explain how to use Moonshine on it's own further down in this readme.

### Running Moonshine By Itself

This version of Moonshine takes 5 arguments,

`./Moonshine.o <inital bit sequence size> <New bit sequence size> <path to the original bit stream> <path to save moonshine's output> `

This version of moonshine is for experimental purposes using a file as a bit stream.
Moonshine could also be run dynamically in the background of a data gathering process as well.
If you want to use moonshine in real time, I would suggest extracting the algorithm code and writing code that will utilize it in realtime.
We present a very straight forward implementation that is designed to be reimplemented in other systems.


    