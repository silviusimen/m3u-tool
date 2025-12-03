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
"""

import m3u_parser
import os
import json
import sys
import argparse


def filter_live_channels(input_file="filtered.m3u", output_file="live_channels.m3u"):
    """
    Filter M3U playlist to exclude series and movies, keeping only live channels.
    
    Args:
        input_file (str): Path to input M3U file
        output_file (str): Path to output M3U file
    
    Returns:
        dict: Statistics about the filtering process
    """
    
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found")
    
    # Parse the M3U file
    print(f"Reading M3U file: {input_file}")
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
        'other_filtered': 0
    }
    
    # Create a list to store live channels
    live_channels = []
    
    print("Filtering entries...")
    
    for entry in playlist:
        is_filtered = False
        filter_reason = ""
        
        # Get entry details
        title = entry.get('name', '')
        url = entry.get('url', '')
        category = entry.get('category', '')
        
        # Check if it's a series (multiple indicators)
        if (category and "SRS" in category.upper()) or \
           (url and "/series/" in url) or \
           (title and any(pattern in title.upper() for pattern in ["S0", "E0", "SEASON", "EPISODE"])):
            stats['series_filtered'] += 1
            is_filtered = True
            filter_reason = "series"
        
        # Check if it's a movie (multiple indicators)
        elif (category and "VOD" in category.upper()) or \
             (url and "/movie/" in url) or \
             (title and any(year in title for year in [str(y) for y in range(1950, 2030)])) or \
             (category and any(keyword in category.upper() 
                              for keyword in ["MOVIE", "FILM", "CINEMA"])):
            stats['movies_filtered'] += 1
            is_filtered = True
            filter_reason = "movie"
        
        # Check for other VOD content
        elif category and any(keyword in category.upper() 
                             for keyword in ["DOWNLOAD", "ON DEMAND", "RENTAL"]):
            stats['other_filtered'] += 1
            is_filtered = True
            filter_reason = "other VOD"
        
        # If not filtered, it's considered a live channel
        if not is_filtered:
            live_channels.append(entry)
            stats['live_channels'] += 1
            print(f"✓ Keeping: {title[:60]}{'...' if len(title) > 60 else ''}")
        else:
            print(f"✗ Filtered ({filter_reason}): {title[:60]}{'...' if len(title) > 60 else ''}")
    
    # Write the filtered playlist manually since the library might not support writing
    print(f"\nWriting filtered playlist to: {output_file}")
    write_m3u_file(live_channels, output_file)
    
    return stats


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
    print("-"*50)
    print(f"Total filtered out:          {stats['series_filtered'] + stats['movies_filtered'] + stats['other_filtered']:,}")
    
    if stats['total_entries'] > 0:
        live_percentage = (stats['live_channels'] / stats['total_entries']) * 100
        filtered_percentage = ((stats['series_filtered'] + stats['movies_filtered'] + stats['other_filtered']) / stats['total_entries']) * 100
        print(f"Live channels percentage:    {live_percentage:.1f}%")
        print(f"Filtered content percentage: {filtered_percentage:.1f}%")


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
        
        print("M3U Playlist Filter - Remove Series and Movies")
        print("=" * 50)
        print(f"Input file:  {input_file}")
        print(f"Output file: {output_file}")
        print("=" * 50)
        
        # Run the filtering
        stats = filter_live_channels(input_file, output_file)
        
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