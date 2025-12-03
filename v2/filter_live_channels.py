#!/usr/bin/env python3
"""
M3U Playlist Filter Script

This script reads an M3U playlist file and filters out series and movies,
keeping only live TV channels. It uses the m3u_parser library for parsing
and creates a new filtered playlist.

Requirements:
    pip install m3u_parser

Usage:
    python filter_live_channels.py [input_file] [output_file]
    python filter_live_channels.py filtered.m3u live_channels.m3u
    python filter_live_channels.py --list-groups input.m3u
"""

import m3u_parser
import os
import json
import sys
import argparse
import re

  
def filter_live_channels(input_file="filtered.m3u", output_file="live_channels.m3u", use_streaming=True, groups_filter_file=None):
    """
    Filter M3U playlist to exclude series and movies, keeping only live channels.
    Uses streaming processing to handle large files efficiently by default.
    
    Args:
        input_file (str): Path to input M3U file
        output_file (str): Path to output M3U file
        use_streaming (bool): Use streaming mode for large files (default: True)
        groups_filter_file (str, optional): Path to file containing allowed group titles
    
    Returns:
        dict: Statistics about the filtering process
    """
    
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found")
    
    # Check file size to determine processing method
    file_size = os.path.getsize(input_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"Reading M3U file: {input_file}")
    print(f"File size: {file_size_mb:.1f} MB")
    
    # Auto-detect if streaming should be used for large files
    if file_size_mb > 1:  # Files larger than 100MB
        use_streaming = True
        print("Large file detected - using streaming mode for memory efficiency")
    elif not use_streaming:
        print("Using standard mode (loads file into memory)")
    else:
        print("Using streaming mode")
    
    # Load allowed groups if specified
    allowed_groups = None
    if groups_filter_file:
        allowed_groups = load_allowed_groups(groups_filter_file)
        if allowed_groups is not None:
            print(f"Group filter loaded: {len(allowed_groups)} allowed groups")
    
    if use_streaming:
        return filter_live_channels_streaming(input_file, output_file, allowed_groups)
    else:
        return filter_live_channels_standard(input_file, output_file, allowed_groups)


def load_allowed_groups(groups_file):
    """
    Load allowed group titles from a file.
    
    Args:
        groups_file (str): Path to file containing group titles (one per line)
    
    Returns:
        set: Set of allowed group titles, or None if file cannot be loaded
    """
    try:
        with open(groups_file, 'r', encoding='utf-8') as f:
            groups = set()
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    groups.add(line)
            return groups
    except FileNotFoundError:
        print(f"❌ Groups filter file not found: {groups_file}")
        return None
    except Exception as e:
        print(f"❌ Error reading groups filter file: {e}")
        return None


def filter_live_channels_streaming(input_file, output_file, allowed_groups=None):
    """Streaming version for large files."""
    print("Processing entries (streaming mode)...")
    
    # Initialize counters
    stats = {
        'total_entries': 0,
        'live_channels': 0,
        'series_filtered': 0,
        'movies_filtered': 0,
        'other_filtered': 0,
        'group_filtered': 0
    }
    
    # Process the file line by line and write output simultaneously
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        # Write M3U header
        outfile.write("#EXTM3U\n")
        
        # State tracking for line-by-line processing
        current_extinf = None
        line_count = 0
        
        for line_num, line in enumerate(infile, 1):
            line = line.strip()
            line_count += 1
            
            # Progress indicator for large files
            if line_count % 10000 == 0:
                print(f"  Processed {line_count:,} lines...")
            
            # Skip empty lines and non-EXTINF comments
            if not line or (line.startswith('#') and not line.startswith('#EXTINF')):
                continue
            
            # Parse EXTINF line
            if line.startswith('#EXTINF'):
                current_extinf = parse_extinf_line_streaming(line)
                continue
            
            # This should be a URL line following an EXTINF
            if current_extinf and not line.startswith('#'):
                url = line
                stats['total_entries'] += 1
                
                # Apply filtering logic
                should_keep, filter_reason = should_keep_entry(
                    current_extinf['name'], url, current_extinf['category'], allowed_groups
                )
                
                if should_keep:
                    stats['live_channels'] += 1
                    # Write the entry to output file immediately
                    write_extinf_line(outfile, current_extinf)
                    outfile.write(f"{url}\n")
                    print(f"✓ Keeping: {current_extinf['name'][:60]}{'...' if len(current_extinf['name']) > 60 else ''}")
                else:
                    if filter_reason == "series":
                        stats['series_filtered'] += 1
                    elif filter_reason == "movie":
                        stats['movies_filtered'] += 1
                    elif filter_reason == "group_not_allowed":
                        stats['group_filtered'] += 1
                    else:
                        stats['other_filtered'] += 1
                    print(f"✗ Filtered ({filter_reason}): {current_extinf['name'][:60]}{'...' if len(current_extinf['name']) > 60 else ''}")
                
                # Reset for next entry
                current_extinf = None
    
    print(f"\nFiltered playlist written to: {output_file}")
    return stats


def filter_live_channels_standard(input_file, output_file, allowed_groups=None):
    """Standard version using m3u_parser library (for smaller files)."""
    parser = m3u_parser.M3uParser()
    parser.parse_m3u(input_file)
    
    # Get the playlist as a list
    playlist = parser.get_list()
    
    # Initialize counters
    stats = {
        'total_entries': len(playlist),
        'live_channels': 0,
        'series_filtered': 0,
        'movies_filtered': 0,
        'other_filtered': 0,
        'group_filtered': 0
    }
    
    # Create a list to store live channels
    live_channels = []
    
    print("Filtering entries...")
    
    for entry in playlist:
        # Get entry details
        title = entry.get('name', '')
        url = entry.get('url', '')
        category = entry.get('category', '')
        
        # Apply filtering logic
        should_keep, filter_reason = should_keep_entry(title, url, category, allowed_groups)
        
        if should_keep:
            live_channels.append(entry)
            stats['live_channels'] += 1
            print(f"✓ Keeping: {title[:60]}{'...' if len(title) > 60 else ''}")
        else:
            if filter_reason == "series":
                stats['series_filtered'] += 1
            elif filter_reason == "movie":
                stats['movies_filtered'] += 1
            elif filter_reason == "group_not_allowed":
                stats['group_filtered'] += 1
            else:
                stats['other_filtered'] += 1
            print(f"✗ Filtered ({filter_reason}): {title[:60]}{'...' if len(title) > 60 else ''}")
    
    # Write the filtered playlist
    print(f"\nWriting filtered playlist to: {output_file}")
    write_m3u_file(live_channels, output_file)
    
    return stats


def parse_extinf_line_streaming(extinf_line):
    """
    Parse an EXTINF line to extract channel metadata for streaming processing.
    
    Args:
        extinf_line (str): EXTINF line from M3U file
        
    Returns:
        dict: Channel metadata
    """
    channel = {
        'name': '',
        'logo': '',
        'category': '',
        'tvg_id': '',
        'tvg_name': ''
    }
    
    # Extract tvg-id
    tvg_id_match = re.search(r'tvg-id="([^"]*)"', extinf_line)
    if tvg_id_match:
        channel['tvg_id'] = tvg_id_match.group(1)
    
    # Extract tvg-name
    tvg_name_match = re.search(r'tvg-name="([^"]*)"', extinf_line)
    if tvg_name_match:
        channel['tvg_name'] = tvg_name_match.group(1)
    
    # Extract tvg-logo
    logo_match = re.search(r'tvg-logo="([^"]*)"', extinf_line)
    if logo_match:
        channel['logo'] = logo_match.group(1)
    
    # Extract group-title
    group_match = re.search(r'group-title="([^"]*)"', extinf_line)
    if group_match:
        channel['category'] = group_match.group(1)
    
    # Extract channel name (everything after the last comma)
    name_match = re.search(r',(.+)$', extinf_line)
    if name_match:
        channel['name'] = name_match.group(1)
    
    return channel


def should_keep_entry(title, url, category, allowed_groups=None):
    """
    Determine if an entry should be kept based on filtering criteria.
    
    Args:
        title (str): Channel title/name
        url (str): Channel URL
        category (str): Channel category/group
        allowed_groups (set, optional): Set of allowed group titles
        
    Returns:
        tuple: (should_keep: bool, filter_reason: str)
    """
    # Check if group is allowed (if groups filter is specified)
    if allowed_groups is not None:
        if not category or category not in allowed_groups:
            return False, "group_not_allowed"
    
    # Check if it's a series (multiple indicators)
    if (category and "SRS" in category.upper()) or \
       (url and "/series/" in url) or \
       (title and any(pattern in title.upper() for pattern in ["S0", "E0", "SEASON", "EPISODE"])) or \
       (title and re.search(r'S\d+\s*E\d+', title.upper())):
        return False, "series"
    
    # Check if it's a movie (multiple indicators)
    elif (category and "VOD" in category.upper()) or \
         (url and "/movie/" in url) or \
         (title and re.search(r'\b(19|20)\d{2}\b', title)) or \
         (category and any(keyword in category.upper() 
                          for keyword in ["MOVIE", "FILM", "CINEMA"])):
        return False, "movie"
    
    # Check for other VOD content
    elif category and any(keyword in category.upper() 
                         for keyword in ["DOWNLOAD", "ON DEMAND", "RENTAL"]):
        return False, "other VOD"
    
    # If none of the above, keep it (it's a live channel)
    return True, ""


def write_extinf_line(outfile, channel):
    """
    Write an EXTINF line to the output file.
    
    Args:
        outfile: File handle for writing
        channel (dict): Channel metadata
    """
    title = channel.get('name', '')
    category = channel.get('category', '')
    logo = channel.get('logo', '')
    tvg_id = channel.get('tvg_id', '')
    tvg_name = channel.get('tvg_name', '')
    
    # Write EXTINF line
    extinf_line = '#EXTINF:-1'
    
    if tvg_id:
        extinf_line += f' tvg-id="{tvg_id}"'
    if tvg_name:
        extinf_line += f' tvg-name="{tvg_name}"'
    if logo:
        extinf_line += f' tvg-logo="{logo}"'
    if category:
        extinf_line += f' group-title="{category}"'
    
    extinf_line += f',{title}\n'
    outfile.write(extinf_line)


def write_m3u_file(channels, output_file):
    """Write channels to M3U file format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        for channel in channels:
            title = channel.get('name', '')
            url = channel.get('url', '')
            category = channel.get('category', '')
            logo = channel.get('logo', '')
            tvg = channel.get('tvg', {})
            tvg_id = tvg.get('id', '') if tvg else ''
            tvg_name = tvg.get('name', '') if tvg else ''
            
            # Write EXTINF line
            extinf_line = f'#EXTINF:-1'
            
            if tvg_id:
                extinf_line += f' tvg-id="{tvg_id}"'
            if tvg_name:
                extinf_line += f' tvg-name="{tvg_name}"'
            if logo:
                extinf_line += f' tvg-logo="{logo}"'
            if category:
                extinf_line += f' group-title="{category}"'
            
            extinf_line += f',{title}\n'
            f.write(extinf_line)
            
            # Write URL line
            f.write(f"{url}\n")


def print_statistics(stats):
    """Print filtering statistics in a formatted way."""
    print("\n" + "="*50)
    print("FILTERING STATISTICS")
    print("="*50)
    print(f"Total entries processed:     {stats['total_entries']:,}")
    print(f"Live channels kept:          {stats['live_channels']:,}")
    print(f"Series filtered out:         {stats['series_filtered']:,}")
    print(f"Movies filtered out:         {stats['movies_filtered']:,}")
    print(f"Other content filtered out:  {stats['other_filtered']:,}")
    if 'group_filtered' in stats and stats['group_filtered'] > 0:
        print(f"Groups filtered out:         {stats['group_filtered']:,}")
    print("-"*50)
    total_filtered = stats['series_filtered'] + stats['movies_filtered'] + stats['other_filtered']
    if 'group_filtered' in stats:
        total_filtered += stats['group_filtered']
    print(f"Total filtered out:          {total_filtered:,}")
    
    if stats['total_entries'] > 0:
        live_percentage = (stats['live_channels'] / stats['total_entries']) * 100
        filtered_percentage = ((stats['series_filtered'] + stats['movies_filtered'] + stats['other_filtered']) / stats['total_entries']) * 100
        print(f"Live channels percentage:    {live_percentage:.1f}%")
        print(f"Filtered content percentage: {filtered_percentage:.1f}%")


def list_group_titles(input_file, output_file=None):
    """
    List all unique group-title values from the input M3U file.
    
    Args:
        input_file (str): Path to input M3U file
        output_file (str, optional): Path to output file for group titles
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found")
    
    # Check file size to determine processing method
    file_size = os.path.getsize(input_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"File size: {file_size_mb:.1f} MB")
    
    group_titles = set()  # Use set to store unique group titles
    total_entries = 0
    
    if file_size_mb > 100:  # Use streaming for large files
        print("Processing large file in streaming mode...")
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            line_count = 0
            for line in infile:
                line = line.strip()
                line_count += 1
                
                # Progress indicator
                if line_count % 10000 == 0:
                    print(f"  Processed {line_count:,} lines...")
                
                # Parse EXTINF lines
                if line.startswith('#EXTINF'):
                    total_entries += 1
                    channel_data = parse_extinf_line_streaming(line)
                    category = channel_data.get('category', '').strip()
                    if category:  # Only add non-empty categories
                        group_titles.add(category)
    else:
        print("Processing file with m3u_parser library...")
        try:
            parser = m3u_parser.M3uParser()
            parser.parse_m3u(input_file)
            playlist = parser.get_list()
            
            for entry in playlist:
                total_entries += 1
                category = entry.get('category', '').strip()
                if category:  # Only add non-empty categories
                    group_titles.add(category)
        except Exception as e:
            print(f"Error parsing with m3u_parser, falling back to streaming mode: {e}")
            # Fallback to streaming mode
            return list_group_titles_streaming(input_file)
    
    # Sort group titles for better readability
    sorted_groups = sorted(group_titles, key=str.lower)
    
    # Prepare output content
    output_lines = []
    
    if output_file:
        # For file output, create script-friendly format
        output_lines.append(f"# M3U Playlist Group Analysis")
        output_lines.append(f"# Input: {input_file}")
        output_lines.append(f"# Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append(f"# Total entries: {total_entries:,}")
        output_lines.append(f"# Unique groups: {len(sorted_groups):,}")
        output_lines.append(f"#")
        
        # Add each group title (one per line, no numbering for scripts)
        for group in sorted_groups:
            output_lines.append(group)
        
        # Write to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines) + '\n')
            print(f"\n📁 Group titles written to: {output_file}")
            print(f"   Format: One group per line (script-friendly)")
            print(f"   Groups: {len(sorted_groups)} unique titles")
        except Exception as e:
            print(f"❌ Error writing to file: {e}")
            return
    
    # Always show summary on console
    print(f"\nFound {len(sorted_groups)} unique group titles in {total_entries:,} entries:")
    
    if not output_file:
        # Full console output only when not writing to file
        print("=" * 60)
        
        # Display group titles with numbering
        for i, group in enumerate(sorted_groups, 1):
            print(f"{i:3d}. {group}")
    else:
        # Abbreviated console output when writing to file
        print("=" * 60)
        print("First 10 groups:")
        for i, group in enumerate(sorted_groups[:10], 1):
            print(f"{i:3d}. {group}")
        if len(sorted_groups) > 10:
            print(f"    ... and {len(sorted_groups) - 10} more (see output file)")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print(f"Total entries: {total_entries:,}")
    print(f"Unique groups: {len(sorted_groups):,}")
    print(f"Entries with groups: {sum(1 for entry in sorted_groups if entry):,}")
    
    # Show most common group prefixes
    prefixes = {}
    for group in sorted_groups:
        if ' | ' in group:
            prefix = group.split(' | ')[0]
        elif ' - ' in group:
            prefix = group.split(' - ')[0]
        else:
            prefix = group.split()[0] if group.split() else group
        
        prefixes[prefix] = prefixes.get(prefix, 0) + 1
    
    if prefixes:
        print(f"\nMost common group prefixes:")
        print("-" * 30)
        for prefix, count in sorted(prefixes.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"{prefix}: {count} groups")


def main():
    """Main function to run the filtering process."""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Filter M3U playlist to remove series and movies, keeping only live channels",
        epilog="Examples:\n  python filter_live_channels.py\n  python filter_live_channels.py input.m3u output.m3u",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "input_file", 
        nargs="?", 
        default="filtered.m3u",
        help="Input M3U file path (default: filtered.m3u)"
    )
    
    parser.add_argument(
        "output_file", 
        nargs="?", 
        default="live_channels.m3u",
        help="Output M3U file path (default: live_channels.m3u)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--no-streaming",
        action="store_true",
        help="Disable streaming mode (use standard mode for small files)"
    )
    
    parser.add_argument(
        "--streaming",
        action="store_true",
        help="Force streaming mode (useful for large files)"
    )
    
    parser.add_argument(
        "--list-groups",
        action="store_true",
        help="List all unique group-title values from the input file and exit"
    )
    
    parser.add_argument(
        "--groups-output",
        type=str,
        metavar="FILE",
        help="Write group titles to specified file (works with --list-groups)"
    )
    
    parser.add_argument(
        "--filter-by-groups",
        type=str,
        metavar="FILE",
        help="Filter entries to only include groups listed in the specified file"
    )
    
    args = parser.parse_args()
    
    try:
        # Get the directory of the current script if relative paths are used
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Handle relative paths
        input_file = args.input_file
        output_file = args.output_file
        
        if not os.path.isabs(input_file):
            input_file = os.path.join(script_dir, input_file)
        if not os.path.isabs(output_file):
            output_file = os.path.join(script_dir, output_file)
        
        # Handle --list-groups option
        if args.list_groups:
            print("M3U Playlist Group Titles Listing")
            print("=" * 50)
            print(f"Input file: {input_file}")
            if args.groups_output:
                print(f"Output file: {args.groups_output}")
            print("=" * 50)
            list_group_titles(input_file, args.groups_output)
            return
        
        print("M3U Playlist Filter - Remove Series and Movies")
        print("=" * 50)
        print(f"Input file:  {input_file}")
        print(f"Output file: {output_file}")
        if args.filter_by_groups:
            print(f"Groups filter: {args.filter_by_groups}")
        print("=" * 50)
        
        # Determine streaming mode
        use_streaming = True  # Default to streaming
        if args.no_streaming:
            use_streaming = False
        elif args.streaming:
            use_streaming = True
        
        # Run the filtering
        stats = filter_live_channels(input_file, output_file, use_streaming, args.filter_by_groups)
        
        # Print statistics
        print_statistics(stats)
        
        print(f"\n✅ Filtering complete!")
        print(f"📺 Live channels playlist saved as: {output_file}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"Make sure the input file exists: {args.input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()