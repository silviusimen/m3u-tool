#!/bin/bash

if [ ! -f KY-panel.json ]; then
    echo "File KY-panel.json must be present, run first ky-data-fetch.sh"
    exit 1
fi

python3 process.py
