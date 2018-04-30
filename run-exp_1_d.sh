#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=144:00:00
#SBATCH --mem=40GB
#SBATCH --job-name=conservativity
#SBATCH --mail-type=END
#SBATCH --mail-user=netID@nyu.edu
#SBATCH --output=exp_1_d.out
#SBATCH --gres=gpu:1

# Activate the conda environment
source activate nlu

# Run the training script
PYTHONPATH=$PYTHONPATH:. python quant_verify_exp1.py --exp one_d --out_path data/1/exp-1-d

# The output will be dumped into a file called terminal_results_1.run_context
# touch terminal_results_1.txt
# cat exp_1_d.out > terminal_results_1.txt
