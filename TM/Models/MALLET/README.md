# Training Topic-Modeling
Run the following cmds from the relevant /result dir.

`mallet import-dir --input ../Documents/ --output trans.mallet --keep-sequence --stoplist-file ../../../pre_process/STOP_WORDS_DIRS/by_words/ALL_STOP.txt`

* ALL_STOP.txt is in ../../../pre_process/STOP_WORDS_DIRS/2019_08_01_19_09_14/
* Documents is in Dirs_of_Docs/

`mallet train-topics --input trans.mallet --inferencer-filename inferencer_100.mallet --output-state topic-state_100.gz --output-topic-keys keys_100.txt --output-doc-topics composition_100.txt --optimize-interval 20 --num-iterations 1000 --optimize-burn-in 50 --num-topics 100`


# Inference on Other Documents
Run the following cmds from the relevant /result dir.

`mallet import-dir --input ../Documents/ --output trans.mallet --keep-sequence --stoplist-file ALL_STOP.txt --use-pipe-from TRAINED_DOCS/trans.mallet`

* Make sure loading the documents with the same stop words as the trained documents
* --use-pipe-from: use the trained .mallet object

`mallet infer-topics --input trans.mallet --inferencer TRAINED_DOCS/inferencer.mallet --output-doc-topics inferencer.txt`

* --inferencer: use the train documents inferencer object