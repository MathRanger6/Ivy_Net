#!/bin/bash
rm export_dir_link/*.*
cp 951*.* export_dir_link/
cp run*.* export_dir_link/
cp output*.* export_dir_link/
cp funct*.* export_dir_link/
cp bash_commands.txt export_dir_link/
./compress_export_folder.sh 
dir export_dir_link/ -l
