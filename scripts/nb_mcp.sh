#!/bin/bash

# Initialize Conda for the current shell session
source "/opt/anaconda3/etc/profile.d/conda.sh"

# Activate your desired Conda environment
conda activate talent_net

# Run the notebook-mcp command
cursor-notebook-mcp --transport sse --log-level DEBUG --allow-root "/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE" --port 8081 &
