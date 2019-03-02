#!/bin/bash
#set -e

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo ./$(basename $0) "<src_json_dir> <target_json_dir>"
    exit 1
fi

SRC_DIR=$1
TARGET_DIR=$2

find  $SRC_DIR -type f | while read file; do
  echo Parsing $file

  python3 extractJson.py $file

  python ~/HE_Parsers/yoav/hebdepparser/parse.py < /tmp/plainText.txt > /tmp/plainTextParsed.txt

  just_file_name=$(basename $file)
  output_file=${TARGET_DIR}/${just_file_name}.parsed
  python3 addAttrJson.py $file $output_file

  echo $output_file was created

done

