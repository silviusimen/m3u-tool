<?php
    if (!function_exists('str_starts_with')) {
        function str_starts_with($haystack, $needle) {
            return (string)$needle !== '' && strncmp($haystack, $needle, strlen($needle)) === 0;
        }
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

    function get_tag_value_from_extinf($extinf, $tag_name)
    {
        $tag = "$tag_name=\"";
        $pos1 = strpos($extinf, $tag);
        if ($pos1 !== false)
        {
            $pos2 = strpos($extinf, '"', $pos1 + strlen($tag) );
            $pos1 += strlen($tag);
            $value = substr($extinf, $pos1, $pos2-$pos1);
    
            return $value;
        }
        else
        {
            return "";
        }
    }

    function m3u_to_json($m3u_string)
    {
        $entries = split_m3u_by_entry($m3u_string);
        foreach ($entries as &$entry)
        {
            $entry['group'] = get_tag_value_from_extinf($entry["extinf"], "group-title");
            $entry['name'] = get_tag_value_from_extinf($entry["extinf"], "tvg-name");
            $entry['id'] = get_tag_value_from_extinf($entry["extinf"], "tvg-id");
            $entry['logo'] = get_tag_value_from_extinf($entry["extinf"], "tvg-logo");
        }
        // #EXTINF:-1 tvg-id="" tvg-name="24/7 Wild Nile" tvg-logo="" group-title="24/7 Shows",24/7 Wild Nile
        // http://ky-iptv.com:80/srM6sUk8hD/9gCrWW2Rqq/388512.ts

        return $entries;
    }

    function entry_belongs_to_groups($entry, $groups_list)
    {
        $entry_group = $entry["group"];
        $result = array_search($entry_group, $groups_list);
        return  ( $result !== false);
    }
    
    function get_list_of_groups($m3u_entries)
    {
        $groups = new \Ds\Set;
        foreach ($m3u_entries as $entry)
        {
            $group = get_tag_value_from_extinf($entry["extinf"], "group-title");
            $groups->add($group);
        }
        return $groups->toArray();
    }

    function filter_m3u_by_groups($m3u_entries, $group_list)
    {
        $filtered_entries = array();
        foreach ($m3u_entries as $entry)
        {
            if (entry_belongs_to_groups($entry, $group_list))
            {
                $filtered_entries[] = $entry;
            }
        }
        return $filtered_entries;
    }

    function render_m3u_entry_extinf($entry)
    {
        $buffer = "#EXTINF:-1 ";
        $buffer .= 'tvg-id="'.$entry['id'].'" ';
        $buffer .= 'tvg-name="'.$entry['name'].'" ';
        $buffer .= 'tvg-logo="'.$entry['logo'].'" ';
        $buffer .= 'group-title="'.$entry['group'].'"';
        $buffer .= ',' . $entry['name'];
        return $buffer;
    }

    function render_m3u($m3u_entries)
    {
        $buffer = "";
        $buffer .= "#EXTM3U".PHP_EOL;
        foreach ($m3u_entries as $entry)
        {
            $buffer .= render_m3u_entry_extinf($entry).PHP_EOL;
            $buffer .= $entry["url"].PHP_EOL;
        }

        echo $buffer;
    }

    function debug_list_m3u($m3u_entries)
    {
        foreach ($m3u_entries as $entry)
        {
            echo $entry["group"]. " - " . $entry["name"] . PHP_EOL;
        }
    }


    function m3u_entry_matches_filter_spec_entry_group($filter_spec_entry, $m3u_entry)
    {
        if (!isset($filter_spec_entry['group_name']) )
            return false;
        return 
            ($filter_spec_entry['group_name'] == $m3u_entry['group']) || 
            ($filter_spec_entry['group_name'] == '*');
    }

    function m3u_entry_matches_name_regexp($m3u_entry, $name_regexp)
    {
        $search_result = preg_grep("/$name_regexp/", array($m3u_entry['name']));
        return count($search_result) > 0;
    }

    function m3u_entry_matches_filter_spec_entry_names($filter_spec_entry, $m3u_entry)
    {
        if (!isset($filter_spec_entry['name_matches']) )
            return true;
        foreach ($filter_spec_entry['name_matches'] as $filter_name) 
        {
            if (m3u_entry_matches_name_regexp($m3u_entry, $filter_name))
            {
                return true;
            }
        }
        return false;
    }

    function entry_belongs_to_filter_spec($m3u_entry, $filter_spec)
    {
        foreach($filter_spec['groups'] as $filter_spec_entry)
        {

            if (m3u_entry_matches_filter_spec_entry_group($filter_spec_entry, $m3u_entry)) 
            {
                if (m3u_entry_matches_filter_spec_entry_names($filter_spec_entry, $m3u_entry))
                {
                    return true;
                }
            }
        }
        return false;
    }

    function process_entry_for_filter($entry, $filter_json_spec) 
    {
        $entry['group'] = $filter_json_spec['new_group_name'];
        //print_r($entry);
        return $entry;
    }

    function get_entries_mathcing_group_name($m3u_entries, $group_name) 
    {
        $filtered_entries = array();
        foreach ($m3u_entries as $entry)
        {
            if ($entry['group'] == $group_name)
            {
                $filtered_entries[] = $entry;
            }
        }
        return $filtered_entries;
    }


    function filter_entries($m3u_entries, $filter_json_spec) 
    {
        $filtered_entries = array();
        foreach ($m3u_entries as $entry)
        {
            if (entry_belongs_to_filter_spec($entry, $filter_json_spec))
            {
                $filtered_entries[] = process_entry_for_filter($entry, $filter_json_spec);
            }
        }
        return $filtered_entries;
    }

?>