#!/bin/bash

if [ "$KY_PANEL_URL" == "" ]; then
    echo "Must set KY_PANEL_URL"
    exit 1
fi

if [ ! -f KY-panel.json ]; then
    echo "curl -s '$KY_PANEL_URL' > KY-panel.json"
    curl -s "$KY_PANEL_URL"  | jq '.' > KY-panel.json
fi
