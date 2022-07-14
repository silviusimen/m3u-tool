<?php

$filters = "KY-reruns.json,KY-discover.json,KY-news.json,KY-sports.json,KY-romania.json,KY-french.json";

header("Location: m3u-filter.php?m3u=KY.m3u&filters=$filters"); 

?>