#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=144:00:00
#SBATCH --mem=40GB
#SBATCH --job-name=conservativity
#SBATCH --mail-type=END
#SBATCH --mail-user=netid@nyu.edu
#SBATCH --output=experiment_oneb.out
#SBATCH --gres=gpu:1


# Activate the conda environment
source activate nlu

# Run the training script (change <dir> to output directory)
#uncomment the below line to start the training after specifying the <dir> to store the results
#PYTHONPATH=$PYTHONPATH:.python quant_verify_exp1.py --exp one_b --out_path data/<dir>


#The terminal results would be dumped into the file called terimal_results.run_context
#This would help to debug if there are any issues.
touch terminal_results.txt
cat experiment_oneb.out > terminal_results.txt
