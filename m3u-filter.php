<?php

    require_once "m3u-utils.php";

    function out($msg)
    {
        echo "$msg".PHP_EOL."<BR>";
    }

    function preout($msg)
    {
        echo PHP_EOL."<pre>$msg</pre>".PHP_EOL."<BR>";
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

    $debug = @urldecode($_REQUEST['debug']);
    $cache = @urldecode($_REQUEST['cache']);
    $url = urldecode($_REQUEST['url']);
    $groups = explode(",",urldecode($_REQUEST['groups']));
    $m3u_string = read_m3u($url, $cache);
    $m3u = m3u_to_json($m3u_string);
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