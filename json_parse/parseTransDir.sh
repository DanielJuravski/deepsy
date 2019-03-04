#!/bin/bash
#set -e

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo ./$(basename $0) "<parser_type ('yoav' or 'reut')> <src_json_dir> <target_json_dir>"
    exit 1
fi

PARSER=$1
SRC_DIR=$2
TARGET_DIR=$3
JSON_PARSE_DIR=~/deepsy/json_parse
YOAV_PARSER=~/HE_Parsers/yoav/hebdepparser
REUT_PARSER=~/HE_Parsers/reut/yapproj

rm -rf $TARGET_DIR
mkdir -p $TARGET_DIR

find  $SRC_DIR -type f | while read file; do
  echo Parsing $file

  python3 $JSON_PARSE_DIR/extractJson.py $file
  
  if [ $PARSER == "yoav" ]; then
  	python $YOAV_PARSER/parse.py < /tmp/plainText.txt > /tmp/plainTextParsed.txt
  elif [ $PARSER == "reut" ]; then
	${REUT_PARSER}/src/yap/yap hebma -raw /tmp/plainTextWordSplited.txt -out /tmp/plainTextParsed.lattice
	${REUT_PARSER}/src/yap/yap joint -in /tmp/plainTextParsed.lattice -os /tmp/plainTextParsed.segmentation -om /tmp/plainTextParsed.mapping -oc /tmp/plainTextParsed.txt
  fi

  just_file_name=$(basename $file)
  output_file=${TARGET_DIR}/${just_file_name}.parsed
  python3 $JSON_PARSE_DIR/addAttrJson.py $file $output_file

  echo $output_file was created

done

