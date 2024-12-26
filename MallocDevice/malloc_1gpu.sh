#!/bin/bash
#SBATCH --job-name=zzj_gpu
#SBATCH --nodes=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --ntasks=2
#SBATCH --comment=GxDVisionTasks
#SBATCH --output=/dev/null
python $HOME/work/MallocDevice/main.py
