#!/bin/bash
#SBATCH --job-name=zzj_cpu
#SBATCH --nodes=1
#SBATCH --partition=cpu
#SBATCH --ntasks=4
#SBATCH --comment=GxDVisionTasks
#SBATCH --output=/dev/null

python $HOME/work/MallocDevice/main.py
