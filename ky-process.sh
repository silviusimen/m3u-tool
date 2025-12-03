#!/bin/bash

if [ ! -f KY-panel.json ]; then
    echo "File KY-panel.json must be present, run first ky-data-fetch.sh"
    exit 1
fi

export OUT_M3U_FILE=ky-no-sports.m3u
export PANEL_FILTER_FILE=KY-filter_no_sports.json
python3 process.py

export OUT_M3U_FILE=ky-sports.m3u
export PANEL_FILTER_FILE=KY-filter_sports.json
python3 process.py

export OUT_M3U_FILE=ky-filter_all.m3u
export PANEL_FILTER_FILE=KY-filter_all.json
python3 process.py
