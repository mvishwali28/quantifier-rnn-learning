#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=144:00:00
#SBATCH --mem=40GB
#SBATCH --job-name=conservativity
#SBATCH --mail-type=END
#SBATCH --mail-user=netID@nyu.edu
#SBATCH --output=exp_1_2_5k_d.out.txt
#SBATCH --gres=gpu:1

# Activate the conda environment
source activate nlu

# Run the training script
PYTHONPATH=$PYTHONPATH:. python quant_verify_exp_1_2_5k.py --exp one_d --out_path data/5k/exp-1-d
