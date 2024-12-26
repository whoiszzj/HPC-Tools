#!/bin/bash
#SBATCH --job-name=zzj_gpu
#SBATCH --nodes=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:3
#SBATCH --ntasks=6
#SBATCH --comment=GxDVisionTasks
#SBATCH --output=/dev/null

python $HOME/work/MallocDevice/main.py
