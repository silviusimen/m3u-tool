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


    $debug = @urldecode($_REQUEST['debug']);
    $m3u = urldecode($_REQUEST['m3u']);
    $filters = explode(",",urldecode($_REQUEST['filters']));

    $m3u_string = file_get_contents($m3u);
    $m3u_entries = m3u_to_json($m3u_string);

    $filtered_entries = array();
    foreach ($filters as $filter)
    {
        $filter_cfg = load_json_from_file($filter);
        $new_entries = filter_entries($m3u_entries, $filter_cfg);
        $filtered_entries = array_merge($filtered_entries, $new_entries);
    }
    
    render_m3u($filtered_entries);

?>