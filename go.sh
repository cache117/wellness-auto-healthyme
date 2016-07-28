#!/bin/bash -x 

./dailygoals2json.sh `date -d "$(date +%Y-%m-01)" +%F` `date -d "$(date +%Y-%m-01) +1 month -1 day" +%F`; ./run-chrome.sh
