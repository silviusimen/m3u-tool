<?php

    require_once "m3u-utils.php";
  
    function load_json_from_file($filename) 
    {
        $contents = @file_get_contents($filename);
        $json = json_decode($contents, true);

        if ($json === NULL)
        {
            $json = array();
        }
        
        return $json;
    } 

    $filter_cfg = load_json_from_file("KY-reruns.json");
    $m3u_string = file_get_contents("KY.m3u");
    $m3u_entries = m3u_to_json($m3u_string);
    //$groups = get_list_of_groups($m3u_entries);
    //print_r($groups);
    //print_r($filter_cfg);

    $filtered_entries = filter_entries($m3u_entries, $filter_cfg);
    //print_r($filtered_entries);
    debug_list_m3u($filtered_entries);

?>