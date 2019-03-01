#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Please provide a snapshot name"
    exit
fi
rm -rf archive/ runinfo/
easypy network_ops_profile.py -html_logs . -testbed_file ../default_testbed.yaml
ARCHIVE_FILE=`find . -name network_ops_profile*.zip`
echo $ARCHIVE_FILE
mkdir -p snapshots
mkdir -p reports
unzip "$ARCHIVE_FILE" pts
mv pts "snapshots/$1.pts"
mv TaskLog.html "reports/$1.html"
open "reports/$1.html"
