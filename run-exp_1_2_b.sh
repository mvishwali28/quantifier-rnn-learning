#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=144:00:00
#SBATCH --mem=40GB
#SBATCH --job-name=conservativity
#SBATCH --mail-type=END
#SBATCH --mail-user=netID@nyu.edu
#SBATCH --output=exp_1_2_b.out
#SBATCH --gres=gpu:1

# Activate the conda environment
source activate nlu

# Run the training script
PYTHONPATH=$PYTHONPATH:. python quant_verify_exp2.py --exp one_b --out_path data/2/exp-1-b

# The output will be dumped into a file called terminal_results.run_context
# touch terminal_results.txt
# cat exp_1_2_b.out > terminal_results.txt
