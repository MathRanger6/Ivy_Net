#!/bin/bash

# Reverse synch: update ./winbucket_link/*.sql files with newer versions
# from ./sql_scripts/*.sql
src_dir="./sql_scripts"
dest_dir="./winbucket_link"
# Create destination directory if it doesn't exist
mkdir -p "$dest_dir"
# Loop through each .sql file in ./sql_scripts
for src_file in "$src_dir"/*.sql; do
	filename=$(basename "$src_file")
	dest_file="$dest_dir/$filename"

	# If destination does not exist or if src file is newer, copy it
	if [ ! -f "$dest_file" ]; then
		echo "Copying new file: $filename"
		cp "$src_file" "$dest_file"
	elif [ "$src_file" -nt "$dest_file" ]; then
		echo "Updating modified file: $filename"
		cp "$src_file" "$dest_file"
	fi
done
echo "Reverse sych complete."
