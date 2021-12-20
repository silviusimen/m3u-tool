<?php

    function out($msg)
    {
        echo "$msg".PHP_EOL."<BR>";
    }

    function preout($msg)
    {
        echo PHP_EOL."<pre>$msg</pre>".PHP_EOL."<BR>";
    }

    if (!function_exists('str_starts_with')) {
        function str_starts_with($haystack, $needle) {
            return (string)$needle !== '' && strncmp($haystack, $needle, strlen($needle)) === 0;
        }
    }

    function read_m3u($url, $cache)
    {
        if ($cache == "no")
        {
            return file_get_contents($url);
        }

        $hash = sha1($url);
        $cache_file = "/tmp/$hash.txt";

        if ($cache == "force_clear")
        {
            unlink($cache_file);
        }

        $cached_data = @file_get_contents($cache_file);
        if ($cached_data === false)
        {
            $m3u = file_get_contents($url);
            file_put_contents($cache_file,$m3u);
        }
        else
        {
            $m3u = $cached_data;
        }

        return $m3u;
    }

    function split_m3u_by_entry($m3u_string)
    {
        $lines = explode("\n", $m3u_string);

        $entries = array();
        $extinf = "";

        foreach ($lines as $line)
        {
            if (str_starts_with($line, '#EXTINF:'))
            {
                $extinf = $line;
            }
            if (str_starts_with($line, 'http://') || str_starts_with($line, 'https://') )
            {
                $entries[] = array("extinf" => $extinf, "url" => $line);
            }
        }

        return $entries;
    }

    function entry_should_be_included($entry, $groups)
    {
        $desc = $entry["extinf"];
        foreach ($groups as $group)
        {
            $pos = strpos($desc, "group-title=\"$group\"");
            if ($pos !== false) 
            {
                return true;
            }
        }
        return false;
    }
    
    function get_list_of_groups($m3u_entries)
    {
        $groups = array();
        $group_tag = "group-title=\"";
        foreach ($m3u_entries as $entry)
        {
            $desc = $entry["extinf"];
            $pos1 = strpos($desc, $group_tag);
            $pos2 = strpos($desc, ",", $pos1);
            $pos1 += strlen($group_tag);
            $group = substr($desc, $pos1, $pos2-$pos1-1);
            $groups[$group] = $entry;
        }
        return array_keys($groups);
    }

    function filter_m3u_by_groups($m3u_entries, $groups)
    {
        $filtered_entries = array();
        foreach ($m3u_entries as $entry)
        {
            if (entry_should_be_included($entry, $groups))
            {
                $filtered_entries[] = $entry;
            }
        }
        return $filtered_entries;
    }

    function render_m3u($m3u_entries)
    {
        $buffer = "";
        $buffer .= "#EXTM3U".PHP_EOL;
        foreach ($m3u_entries as $entry)
        {
            $buffer .= $entry["extinf"].PHP_EOL;
            $buffer .= $entry["url"].PHP_EOL;
        }

        return $buffer;
    }


    $debug = @urldecode($_REQUEST['debug']);
    $cache = @urldecode($_REQUEST['cache']);
    $url = urldecode($_REQUEST['url']);
    $groups = explode(",",urldecode($_REQUEST['groups']));
    $m3u_string = read_m3u($url, $cache);
    $m3u = split_m3u_by_entry($m3u_string);
    $filtered = filter_m3u_by_groups($m3u, $groups);

    if ($debug == "true")
    {
        out("Requested groups=".print_r($groups, true));
        out("m3u was read from $url");
        out("Initial count=".count($m3u));
        out("Filtered count=".count($filtered));
        preout("Available groups=".print_r(get_list_of_groups($m3u), true));
    }
    else
    {
        echo render_m3u($filtered);
    }

?>