#!/bin/bash

RAY_TMP_DIR="/tmp/ray_tmp"
# Note: Ray uses /tmp/ray_tmp by default, not /tmp/ray
# This script cleans the actual Ray temp directory

if [ ! -d "$RAY_TMP_DIR" ]; then
	echo "Directory "$RAY_TMP_DIR" does not exist."
	exit 1
fi

# Show size
echo "Current size of $RAY_TMP_DIR:"
du -sh "$RAY_TMP_DIR"

# Ask for confirmation
read -p "Do you want to delete all the contents of $RAY_TMP_DIR? [y/N] " answer

# Convert to lowercase and act on yes
case "$answer" in
	[yY][eE][sS]|[yY])
		echo "Deleting contents of $RAY_TMP_DIR..."
		rm -rf "$RAY_TMP_DIR"/*
		echo "Done."
		;;
	*)
		echo "Aborted. No files were deleted."
		;;
esac		
