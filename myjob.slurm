#!/bin/bash

#Submit this script with: sbatch myjob.slurm

#SBATCH --time=1:00:00   # job time limit
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # number of tasks per node
#SBATCH --cpus-per-task=1   # number of CPU cores per task
#SBATCH --partition=standard   # partition
#SBATCH -J "tenure_net_env_install"   # job name
#SBATCH --mail-user=dzk3ja@virginia.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --constraint=rivanna   # cluster
#SBATCH --account=ConnectedDataHub   # allocation name


# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE

module load miniforge
cd ~/Ivy_Net
conda env create -f environment-tenure_net.yml
