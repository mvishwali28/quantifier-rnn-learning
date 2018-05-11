#!/bin/sh

mkdir -p plots_testing/30k/
mkdir -p plots_training/30k/

exps="a b c d e"

for name in $exps
do
	python analysis.py --exp $name
done
