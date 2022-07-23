#!/bin/bash

if [ ! -f KY-panel.json ]; then
    echo "curl -s '$KY_PANEL_URL' > KY-panel.json"
    curl -s "$KY_PANEL_URL" > KY-panel.json
fi

if [ ! -f KY-full.m3u ]; then
    echo "curl -s '$KY_URL' > KY-full.m3u"
    curl -s "$KY_URL" > KY-full.m3u
fi
