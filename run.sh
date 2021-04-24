#!/bin/bash

ulimit -c unlimited
ulimit -n 8192

if [ $# -ne 1 ]; then
  echo "Usage: ./run.sh <'crawler' or 'index'>"
  exit 1
fi
if [ "$1" = "crawler" ]; then
  cd ~/crawler
  threads=800
  echo -e "Crawler Started         @[$(date)]" >> crawlerLog.txt
  ./TestSingleCrawler $THIS_CRAWLER_ID $TOTAL_CRAWLERS $threads 2> err1 1> /dev/null
  echo -e "Crawler Exited ( $? )    @[$(date)]" >> crawlerLog.txt
elif [ "$1" = "index" ]; then
  cd ~/index
  echo -e "Index Started         @[$(date)]" >> indexLog.txt
  ./index chunks 5000 2> errs 1> /dev/null
  echo -e "Index Exited ( $? )    @[$(date)]" >> indexLog.txt
else
  echo "Usage: ./run.sh <'crawler' or 'index'>"
  exit 1
fi
read -t 20 -p "enter 'q' to stop" inputVar
if [ "$inputVar" = "q" ]; then
  exit 0
~/monitoring/run.sh $1