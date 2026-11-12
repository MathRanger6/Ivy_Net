#!/bin/bash

# Define the path to your conda installation directory 
# CONDA_INSTALL_PATH=" /opt/miniconda3"


# Source the conda.sh script to initialize conda functions for the current shell session
source /opt/miniconda3/etc/profile.d/conda.sh

# Check if the activation was successful
#if [ $? -ne 0 ]; then
#	echo "Error: could not source /opt/miniconda3/etc/profile.d/conda.sh"
#	exit 1
#fi

# Now activate my environment
conda activate TALNET39

# Check if the activation was successful
#if [ $? -ne 0 ]; then
#	echo "Error: Could not activate Conda environment 'TALNET39'"
#	exit 1
#fi

# Your commands within the activated environment go here
#echo "Conda environment 'TALNET39' activated."
#conda activate TALNET39
