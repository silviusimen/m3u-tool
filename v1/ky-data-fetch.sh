#!/bin/bash

# if [ "$KY_URL" == "" ]; then
#     echo "Must set KY_URL"
#     exit 1
# fi

if [ "$KY_PANEL_URL" == "" ]; then
    echo "Must set KY_PANEL_URL"
    exit 1
fi

if [ ! -f KY-panel.json ]; then
    echo "curl -s '$KY_PANEL_URL' > KY-panel.json"
    curl -s "$KY_PANEL_URL"  | jq '.' > KY-panel.json
fi

# if [ ! -f KY-full.m3u ]; then
#     echo "curl -s '$KY_URL' > KY-full.m3u"
#     curl -s "$KY_URL" > KY-full.m3u
# fi
