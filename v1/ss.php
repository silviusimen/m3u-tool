<?php

$filter_list = array (
    "KY-reruns.json",
    "KY-discover.json",
    "KY-canada.json",
    "KY-news.json",
    "KY-sports.json",
    "KY-romania.json",
    "KY-french.json"
);

$filters = implode(",", $filter_list);

header("Location: m3u-filter.php?m3u=KY.m3u&filters=$filters"); 

?>