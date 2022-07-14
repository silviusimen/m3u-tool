<?php
    require_once "m3u-utils.php";
  

    function is_live_url($url) 
    {
        if (strpos($url, '/series/') !== FALSE)
        {
            return false;
        }

        if (strpos($url, '/movie/') !== FALSE)
        {
            return false;
        }
        return true;
    }

    function filter_live_entries($m3u_entries) 
    {
        $filtered_entries = array();
        foreach ($m3u_entries as $entry)
        {
            if (is_live_url($entry['url']))
            {
                $filtered_entries[] = $entry;
            }
        }
        return $filtered_entries;
    }

    if ($argv[1] == "trim-file")
    {
        /*
        $m3u_string = file_get_contents("KY.m3u");
        $m3u_entries = m3u_to_json($m3u_string);
        //$filtered_entries = filter_live_entries($m3u_entries);
        $filtered_entries = $m3u_entries;
        render_m3u($filtered_entries);
        */
    }

    if ($argv[1] == "list-groups")
    {
        $m3u_string = file_get_contents("KY.m3u");
        $m3u_entries = m3u_to_json($m3u_string);
        $groups = get_list_of_groups($m3u_entries);
        foreach($groups as $g) 
        {
            echo "$g".PHP_EOL;
        }
    }


?>