#!/bin/bash -l
#SBATCH --job-name=shuffle
#SBATCH --output=/cellar/users/snwright/Data/RareCommon/slurm/shuffle_%A.out
#SBATCH --error=/cellar/users/snwright/Data/RareCommon/slurm/shuffle_%A.err
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=100GB
#SBATCH --time=24:00:00

net_input=$1
DATADIR=/cellar/users/snwright/Data/RareCommon/inputs
execdir=/cellar/users/snwright/Git/rare_common/carva
OUTDIR=/cellar/users/snwright/Data/RareCommon/inputs/shuffled_nets

net_file=$DATADIR/$net_input

python $execdir/network_shuffle.py -o $OUTDIR \
	--nSwaps 0.1 --testMode 0 --verbose 1 $net_file

