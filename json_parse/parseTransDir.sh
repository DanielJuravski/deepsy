#!/bin/bash
#set -e

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo ./$(basename $0) "<src_json_dir> <target_json_dir>"
    exit 1
fi

SRC_DIR=$1
TARGET_DIR=$2
JSON_PARESE_DIR=~/deepsy/json_parse
YOAV_PARSER=~/HE_Parsers/yoav/hebdepparser

rm -rf $TARGET_DIR
mkdir -p $TARGET_DIR

find  $SRC_DIR -type f | while read file; do
  echo Parsing $file

  python3 $JSON_PARESE_DIR/extractJson.py $file

  python $YOAV_PARSER/parse.py < /tmp/plainText.txt > /tmp/plainTextParsed.txt

  just_file_name=$(basename $file)
  output_file=${TARGET_DIR}/${just_file_name}.parsed
  python3 $JSON_PARESE_DIR/addAttrJson.py $file $output_file

  echo $output_file was created

done

