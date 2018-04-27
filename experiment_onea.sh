#!/bin/bash
#SBATCH --gres=gpu:1  # Request 1 GPU
#SBATCH --mem=8000  # Request 8GB of memory
#SBATCH -t24:00:00  # Request run time of 24 hours

# Activate the conda environment
source activate nlu

# Run the training script (change <dir> to output directory)
#PYTHONPATH=$PYTHONPATH:. python -u quant_verify.py --exp one_a --out_path data/<dir>
