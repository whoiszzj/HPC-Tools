#!/bin/bash
#SBATCH --job-name=zzj_gpu
#SBATCH --nodes=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:4
#SBATCH --ntasks=8
#SBATCH --comment=GxDVisionTasks
#SBATCH --output=/dev/null

python $HOME/work/MallocDevice/main.py
