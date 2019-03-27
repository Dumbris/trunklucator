#!/bin/sh

ls -1 data | sed 's#^\(.*\)$#{"html":"<img src=\\"/data/\1\\">", "file":"\1"}#' | DATA_DIR=data python3 main.py
