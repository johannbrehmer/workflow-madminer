from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
#import matplotlib
#from matplotlib import pyplot as plt
#%matplotlib inline
import sys 
import yaml
from madminer.core import MadMiner
from madminer.plotting import plot_2d_morphing_basis
from madminer.sampling import combine_and_shuffle
from madminer.sampling import SampleAugmenter


input_file = str(sys.argv[1])
with open(input_file) as f:
    dict_all = yaml.safe_load(f)

njobs =  int(sys.argv[2])

h5_file = str(sys.argv[3])

mg_dir = '/madminer/software/MG5_aMC_v2_6_2'

miner = MadMiner()#(debug=False)

miner.load(h5_file)

##################################################################################
#signal


benchmarks = [str(i) for i in miner.benchmarks]
m = len(benchmarks)

print('list of benchmarks', benchmarks)


miner.run_multiple(
    only_prepare_script=True,
    #sample benchmarks from already stablished benchmarks in a democratic way
    sample_benchmarks=benchmarks[0:njobs%m]+benchmarks*int(njobs/m), #[', '.join(benchmarks) for i in range(int(njobs/m))].extend(benchmarks[0:njobs%m]),
    mg_directory=mg_dir,
    mg_process_directory='/madminer/code/mg_processes/signal',
    proc_card_file='/madminer/code/cards/proc_card_signal.dat',
    param_card_template_file='/madminer/code/cards/param_card_template.dat',
    run_card_files=['/madminer/code/cards/run_card_signal.dat'],
    pythia8_card_file='/madminer/code/cards/pythia8_card.dat',
    log_directory='/madminer/code/logs/signal')
    #initial_command='source activate python2'

print(benchmarks[0:njobs%m]+benchmarks*int(njobs/m))

#create file to link benchmark_i to run_i.sh
for i in range(njobs):
    j = i%m
    f = open("/madminer/code/mg_processes/signal/madminer/cards/benchmark_"+str(i)+".dat","w+")
    f.write( "{}".format(benchmarks[j]) )
    print('generate.py', i, benchmarks[j])
    f.close()

#background
miner.run_multiple(
    is_background=True,
    only_prepare_script=True,
    sample_benchmarks=[', '.join(benchmarks) for i in range(int(njobs/m))].extend(benchmarks[0:njobs%m]), #['sm' for i in range(njobs)],
    mg_directory=mg_dir,
    mg_process_directory='/madminer/code/mg_processes/background',
    proc_card_file='/madminer/code/cards/proc_card_background.dat',
    param_card_template_file='/madminer/code/cards/param_card_template.dat',
    run_card_files=['/madminer/code/cards/run_card_background.dat'],
    pythia8_card_file='/madminer/code/cards/pythia8_card.dat',
    log_directory='/madminer/code/logs/background')

for i in range(njobs):
    j = i%m
    print('generate.py',i, benchmarks[j])
    f= open("/madminer/code/mg_processes/background/madminer/cards/benchmark_"+str(i)+".dat","w+")
    f.write( "{}".format(benchmarks[j]) )
    f.close()
