#!/bin/bash -l
#SBATCH --job-name=qnetcoloc
#SBATCH --output qnetcoloc_%A_%a.out
#SBATCH --error qnetcoloc_%A_%a.err
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --mem-per-cpu=24G
#SBATCH --array=0-50%10

uuid=''
PWD=$(pwd)
outdir=$PWD/../outputs
netdir=$PWD/../outputs
execdir=$PWD/../carva

config=$1
source run_configs/$1

traitsR=($(cat $trait_listR))
traitsC=($(cat $trait_listC))

tR=${traitsR[$SLURM_ARRAY_TASK_ID]}
tC=${traitsC[$SLURM_ARRAY_TASK_ID]}

echo $tR $tC $q $transform $normalization ${SLURM_ARRAY_JOB_ID}_$SLURM_ARRAY_TASK_ID >> $trait_list.slurmIDs

outdir=$outdir/$name

mkdir -p $outdir

#echo -e "Trait_Common\tTrait_Rare\tNetwork\tMean_NPS\tNull_NPS\tp_NPS\tSize\tNull_Size\tp_Size" > $OUTDIR/netcoloc/pilot_netcoloc_results_$t_$t.txt

file_list=${outdir}/${SLURM_ARRAY_JOB_ID}.files

if [[ "$overlap" == 'bin' ]]; then
	overlap_control=bin
else
	overlap_control=remove
fi


/usr/bin/time -v srun -l python $execdir/do_carva_netcoloc.py --outdir $outdir \
	--indir $datadir --trait_rare $tR --trait_common $tC \
	--netdir $netdir --binsize 20 \
	--net_name $name --transform $transform \
	--normalization $normalization --quant --min-genes 3 \
	--overlap_control $overlap_control

echo qnetcoloc_${tR}_${tC}__q_${transform}_${normalization}.txt >> $file_list
