# Moonshine

Moonshine is a randomness distiller. 
The purpose of Moonshine is to be applied to a dataset after bit extraction to increase the randomness of a bit stream.
Ideally, Moonshine would be run in real-time and create a mapping after a "warmup" period has passed which allowed for

This repositiory currently supports linux and MacOS.
Windows support could be apart of future releases if there is requested support.

### Dependencies

There are two components to this repository.
This repository contains the C code for Moonshine's algorithm and python scripts to run experiments on ascii bit streams.
Tools needed to run the code:

    - GCC
    - Python3
    - make 

The version of the graphs in the paper are ordered differently and have a different font.
To change the font, you must install `texlive`.
You can still compile and run everything without texlive.
There is commented code in the create_heat_maps.py file which, if uncommented, will apply a Latex font to the graphs.

The python experiments do have a few dependencies due to the analysis we preform after running the experiments.
Therefore to install the dependencies run, `pip install -r ./requirements.txt`.

If you would like to generate your own graphs you will need the NIST test suite discussed above.
You also need to set up three enviromental variables.


### Build Moonshine and Run Moonshine

Moonshine does not have any inherient requirements.
On any system that has GCC, the user needs to just compile the code using this command, `make -C src`.
That will create an output file called `Moonshine.o`.
To make it available in the 'bin' folder, type `make -C src install`.

This version of Moonshine takes 5 arguments,

`./Moonshine.o <inital bit sequence size> <New bit sequence size> <path to the original bit stream> <path to save moonshine's output> `

This version of moonshine is for experimental purposes using a file as a bit stream.
Moonshine could also be run dynamically in the background of a data gathering process as well.
If you want to use moonshine in real time, I would suggest extracting the algorithm code and writing code that will utilize it in realtime.
We present a very straight forward implementation that is designed to be reimplemented in other systems.

### Running all experiments

To run experiments, you can enter the command `python3 scripts/run_experiments.py`.
The script will pull and install the NIST test suite and it will pull the datasets we used to evaluate Moonshine.
The script will also compile Moonshine.
The finaly thing the script will do is generate the graphs used in our work.
The Graphs generated will be sized differently than the ones in the paper, to size them to your comfort or to take a closer look, use the plt.show() above the plt.savefig() command in the `create_heat_maps.py` file.

By default, our experiments script will setup directories in the Moonshine git repository directory.
You can change paths by adding any of these arguments to the python command in the sh file, `--data_path '<path>' --NIST_path '<path>' --Moonshine_path '<path>'`.


### Disclaimer

THIS PROCESS WILL TAKE A VERY LONG TIME TO COMPLETE.
IF YOU ARE USING VISUAL STUDIO YOU MAY EXPERIENCE SOME RAM ISSUES IF YOU HAVE VSCODE OPEN WHILE RUNNING THE EXPERIMENTS.


### Author 

[Jack West](jacksonwaynewest.com) - [Github](https://github.com/jweezy24) - [jwest1@luc.edu](jwest1@luc.edu)

    
