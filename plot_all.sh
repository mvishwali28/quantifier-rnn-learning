#!/bin/sh

mkdir -p plots_testing/10k/
mkdir -p plots_testing/30k/
mkdir -p plots_training/10k/
mkdir -p plots_training/30k/

exps="one_a one_b one_c one_d one_e two_a two_b two_c two_d two_e"

for name in $exps
do
	python analysis.py --exp $name
done
