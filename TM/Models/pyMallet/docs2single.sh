#!/bin/bash


# That script is for merging multiple docs to 1 single doc for pyMallet format.
# every doc in the given directory, will be a line at the output file.

if [[ $# -ne 2 ]]; then
    echo "Usage: ${0} <input_dir> <output_file>"
    exit 1
fi

input_dir=$1
output_file=$2

# clean output file
[ -e $output_file ] && rm $output_file
touch $output_file

# iterate over docs
for filename in $input_dir/*; do
    cat $filename >> ${output_file}
done

echo Done.