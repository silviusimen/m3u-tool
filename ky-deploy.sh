#!/bin/bash

if [ ! -f ky-filter-1.m3u ]; then
    echo "File ky-filter-1.m3u must be present, run first ky-process.sh"
    exit 1
fi

scp ky-no-sports.m3u ssimen-lt-second:public_html/m3u-tool/
scp ky-sports.m3u ssimen-lt-second:public_html/m3u-tool/
scp ky-filter_all.m3u ssimen-lt-second:public_html/m3u-tool/