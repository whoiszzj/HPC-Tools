# MallocDevice in HPC

这个东西的功能是申请资源的脚本 malloc_1gpu 就是申请一块gpu，以此类推。malloc_cpu 就是只申请cpu。

## 详情解析

```bash
#!/bin/bash
#SBATCH --job-name=zzj_gpu  # 资源名称
#SBATCH --nodes=1   # 开辟几个节点 默认是1
#SBATCH --partition=gpu  # 资源类型
#SBATCH --gres=gpu:1  # 几块gpu
#SBATCH --ntasks=8  # cpu数目
#SBATCH --comment=GxDVisionTasks  # 使用的账户
#SBATCH --output=/dev/null  # 输出的log目录
python $HOME/work/MallocDevice/main.py  # 循环执行脚本，不要动，但是要改一下目录
```

## 添加alias

```bash
alias malloc_cpu='sbatch $HOME/work/MallocDevice/malloc_cpu.sh'
alias malloc_1gpu='sbatch $HOME/work/MallocDevice/malloc_1gpu.sh'
alias malloc_2gpu='sbatch $HOME/work/MallocDevice/malloc_2gpu.sh'
alias malloc_3gpu='sbatch $HOME/work/MallocDevice/malloc_3gpu.sh'
alias malloc_4gpu='sbatch $HOME/work/MallocDevice/malloc_4gpu.sh'

alias mysqueue='squeue -u $USER'  # 查看自己已经申请的资源列表
```

## 一般使用场景

```bash
zzj@workstation malloc_1gpu
zzj@workstation mysqueue
## output
     JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
    126686       gpu  zzj_gpu ud202381  R    5:06:00      1 gpu3

zzj@workstation ssh gpu3
zzj@gpu3 nrun ./xxx.sh
zzj@gpu3 scancel $SLURM_JOB_ID  # 释放本资源
zzj@workstation
```

