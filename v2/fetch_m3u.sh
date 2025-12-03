#!/bin/bash

URL=http://supott74.xyz:80

# Enable automatic export of all variables defined after this point
set -o allexport

# Source the .env file
source ./.env

# Disable automatic export
set +o allexport

echo curl -v -A "TV-Lite custom build" "$URL/get.php?username=${USER}&password=${PASS}&type=m3u_plus&output=ts"
curl -v -A "TV-Lite custom build" "$URL/get.php?username=${USER}&password=${PASS}&type=m3u_plus&output=ts" > full_playlist.m3u

