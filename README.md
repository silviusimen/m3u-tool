# M3U Filtering Tool

## Overview

This script is meant to be used to select from an M3U file only the entries which have the group-title in a list of specified pre-sets.

## Usage

```shell
export KY_PANEL_URL='http://ky-tv.cc:25461/panel_api.php?username=USERNAME&password=PASSWORD'

./ky-data-fetch.sh

# Update KY-panel_filters.json as needed

./ky-process.sh

# Deploy ky-filter-1.m3u to web server
./ky-deploy.sh

```

