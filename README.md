# M3U Filtering Tool

## Overview

This script is meant to be used to select from an M3U file only the entries which have the group-title in a list of specified pre-sets.

## Usage

Deploy the ```m3u-filter.php``` file to a PHP server. 

Note that the M3U files can contain credentials, thus it is important to make sure that the server does not log the requests and the connectivity to the server is secured through some means.

The script accepts the following URI query parameters:
* url - the URL of the original M3U file that needs to be filtered
* groups - the list of groups to be kept (comma separated)
* debug - set to true to suppress the normal output and get some diagnostic info
* cache - controls the use of caching. Values are 
    - "yes" (default) - use cache if present, fetch and update cache if not
    - "no" - always fetch from remote, ignore any local data
    - "force_clear" - clear local cache before fetching from remote

Note that all parameters need to be URL encoded.

Point your client to the m3u-filter.php location including all the parameters:
```
http://192.168.0.10/m3u-filter.php?url=http%3A%2F%2Fciao.ok2.se%2Fget.php%3Fusername%3Duser%26password%3Dpass%26type%3Dm3u_plus%26output%3Dts&groups=ENGLISH,FRENCH
```

## Examples

### Getting some debug info from the tool
http://192.168.0.10/m3u-filter.php?url=http%3A%2F%2Fciao.ok2.se%2Fget.php%3Fusername%3Duser%26password%3Dpass%26type%3Dm3u_plus%26output%3Dts&groups=ENGLISH,FRENCH&debug=true

### Example of an M3U entry
```
#EXTINF:-1 tvg-ID="ctvhalifax.ca" tvg-name="CTV HALIFAX" tvg-logo="https://s3.amazonaws.com/ok2logo/ctv.png" group-title="ENGLISH",CTV HALIFAX
http://ciao.ok2.se:80/USER/PASS/4074
```


### Filter a m3u file by a predefined filter
```
http://localhost:8123/m3u-filter2.php?m3u=KY-test.m3u&filter=KY-discover.json
http://localhost:8123/m3u-filter2.php?m3u=KY-test.m3u&filter=KY-sports.json
http://localhost:8123/m3u-filter2.php?m3u=KY-test.m3u&filter=KY-reruns.json
```


KY curl
code refact
startrek
kodi tv guide
