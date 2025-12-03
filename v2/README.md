# M3U Playlist Filter Script

This directory contains a Python script to filter M3U playlists by removing series and movies, keeping only live TV channels. The script now supports **streaming mode** for processing large M3U files without loading them entirely into memory.

## Features

- ✅ **Memory-efficient streaming** for large files (>100MB)
- ✅ **Automatic file size detection** with smart mode selection
- ✅ **Command line arguments** for input/output files
- ✅ **Makefile automation** for easy setup and usage
- ✅ **Fallback to standard mode** for smaller files
- ✅ **Progress tracking** for large file processing
- ✅ **Group title analysis** - list and analyze all group categories

## Quick Start

The easiest way to use this script is with the provided Makefile:

```bash
# Set up environment and dependencies
make setup

# Run with default files
make run

# Run with custom input file
make run INPUT_FILE=my_playlist.m3u

# Run with custom input and output files
make run INPUT_FILE=source.m3u OUTPUT_FILE=filtered_output.m3u

# List all group titles from a playlist
python filter_live_channels.py --list-groups large_playlist.m3u

# Or use Makefile for easier access
make groups INPUT_FILE=large_playlist.m3u

# Or use the shorter alias
make filter INPUT_FILE=playlist.m3u
```

## Makefile Commands

- `make setup` - Set up virtual environment and install dependencies
- `make run` - Run the M3U filter script with default files
- `make run INPUT_FILE=input.m3u` - Run with custom input file
- `make run OUTPUT_FILE=output.m3u` - Run with custom output file
- `make run INPUT_FILE=in.m3u OUTPUT_FILE=out.m3u` - Run with both custom files
- `make filter` - Alias for `make run` (also supports custom files)
- `make groups` - List all group titles from default input file
- `make groups INPUT_FILE=playlist.m3u` - List group titles from custom file
- `make analyze` - Alias for `make groups` (group analysis)
- `make clean` - Remove generated files and virtual environment
- `make reinstall` - Clean and setup again
- `make check` - Check if prerequisites are met
- `make status` - Show environment and file status
- `make help` - Show all available commands

## Manual Usage

If you prefer to run the script directly without the Makefile:

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install m3u_parser

# Run with default files (automatic mode selection)
python filter_live_channels.py

# Run with custom input file
python filter_live_channels.py my_input.m3u

# Run with custom input and output files
python filter_live_channels.py input.m3u output.m3u

# Force streaming mode (for large files)
python filter_live_channels.py large_file.m3u output.m3u --streaming

# Force standard mode (for small files)
python filter_live_channels.py small_file.m3u output.m3u --no-streaming

# List all group titles from a file (analysis mode)
python filter_live_channels.py --list-groups playlist.m3u

# List group titles and save to file
python filter_live_channels.py --list-groups --groups-output groups.txt playlist.m3u

# Filter by specific groups from file
python filter_live_channels.py input.m3u output.m3u --filter-by-groups allowed_groups.txt

# Show help
python filter_live_channels.py --help
```

## Processing Modes

### **Streaming Mode (Default for large files)**
- ✅ **Memory efficient** - processes files line by line
- ✅ **No memory limits** - can handle multi-GB files
- ✅ **Progress tracking** - shows progress every 10,000 lines
- ✅ **Real-time output** - writes results as it processes
- 📊 **Auto-enabled** for files > 100MB

### **Standard Mode (Default for small files)**
- ✅ **Full compatibility** - uses m3u_parser library
- ✅ **Rich metadata** - preserves all M3U attributes
- ✅ **Fast processing** - loads entire file into memory
- 📊 **Auto-enabled** for files ≤ 100MB

## Group Analysis

The script includes a powerful group analysis feature to help you understand your playlist structure:

```bash
# Analyze group titles in any M3U file
python filter_live_channels.py --list-groups your_playlist.m3u
```

**Group Analysis Features:**
- ✅ **Complete group listing** - All unique group-title values
- ✅ **Smart processing** - Uses appropriate mode based on file size  
- ✅ **Statistics** - Total entries, unique groups, and group counts
- ✅ **Prefix analysis** - Shows most common group prefixes/categories
- ✅ **Sorted output** - Alphabetically sorted for easy browsing
- ✅ **Progress tracking** - Shows progress for large files

**Console Output Example:**
```
Found 538 unique group titles in 1,112,954 entries:
============================================================
  1. AF | AFRICA
  2. AM | BRAZIL  
  3. AR | ARABIC SPORTS
  ...
Most common group prefixes:
------------------------------
VOD: 150 groups (Video On Demand)
EU: 142 groups (Europe)
SRS: 73 groups (Series)
AM: 66 groups (Americas)
```

**File Output Example (--groups-output groups.txt):**
```
# M3U Playlist Group Analysis
# Input: filtered.m3u
# Generated: 2024-01-15 14:30:45
# Total entries: 1,112,954
# Unique groups: 538
#
AF | AFRICA
AM | BRAZIL
AR | ARABIC SPORTS
EU | GERMANY
VOD | ACTION MOVIES
...
```

This feature is perfect for:
- 📊 **Understanding playlist structure** before filtering
- 🔍 **Identifying unwanted categories** to improve filtering
- 📈 **Analyzing content distribution** across regions/types
- ⚙️ **Customizing filter rules** based on actual group names
- 🤖 **Script automation** - generate group lists for other tools to process

## Groups-Based Filtering

Filter playlists to include only specific groups/categories:

```bash
# Create a file with allowed group titles (one per line)
echo "AM | CA | NEWS" > allowed_groups.txt
echo "EU | DEUTSCHLAND | SPORT" >> allowed_groups.txt

# Filter playlist to keep only these groups
python filter_live_channels.py input.m3u output.m3u --filter-by-groups allowed_groups.txt
```

**Groups Filtering Features:**
- ✅ **Targeted filtering** - Keep only specified group titles
- ✅ **File-based configuration** - Manage allowed groups in separate files
- ✅ **Comment support** - Use # for comments in groups files
- ✅ **Exact matching** - Groups must match exactly as they appear in the playlist
- ✅ **Combined filtering** - Works with series/movies filtering (removes both unwanted groups AND unwanted content types)
- ✅ **Statistics tracking** - Shows how many entries were filtered by group vs content type

**Common Workflow:**
```bash
# 1. Analyze playlist to see all available groups
python filter_live_channels.py --list-groups --groups-output all_groups.txt playlist.m3u

# 2. Create custom allowed groups file from the analysis
grep "EU |" all_groups.txt > european_groups.txt

# 3. Filter to keep only European channels
python filter_live_channels.py playlist.m3u european_only.m3u --filter-by-groups european_groups.txt
```

### **Makefile Integration**

Both group analysis and groups-based filtering are available through convenient Makefile commands:

```bash
# Group Analysis Commands
make groups                                    # Analyze and save to groups.txt
make groups INPUT_FILE=my_playlist.m3u         # Custom input file
make groups-console                            # Console output only

# Groups-Based Filtering Commands
make filter-by-groups                          # Filter using allowed_groups.txt
make filter-by-groups GROUPS_FILTER_FILE=european_groups.txt  # Custom filter file

# Combined workflow example
make groups INPUT_FILE=large_playlist.m3u GROUPS_OUTPUT_FILE=all_groups.txt
grep "EU |" all_groups.txt > european_only.txt
make filter-by-groups GROUPS_FILTER_FILE=european_only.txt OUTPUT_FILE=european_channels.m3u
```

**Benefits of using Makefile:**
- ✅ **Automatic prerequisite checking** - ensures dependencies are installed
- ✅ **Consistent environment** - uses the project's virtual environment
- ✅ **Simple syntax** - no need to remember Python command syntax
- ✅ **File validation** - checks if input file exists before running
- ✅ **Flexible output** - supports both console and file output modes

## Script Details

### `filter_live_channels.py`

**Requirements:**
- Python 3.6+
- m3u_parser library

**Features:**
- **Dual processing modes**: Streaming for large files, standard for small files
- **Automatic mode detection**: Based on file size (100MB threshold)
- **Memory efficient**: Can process multi-gigabyte files
- **Progress tracking**: Visual progress for large file processing
- **Command line flexibility**: Override files and processing modes

**File Size Handling:**
- Files ≤ 100MB: Standard mode (m3u_parser library)
- Files > 100MB: Streaming mode (line-by-line processing)
- Manual override: `--streaming` or `--no-streaming` flags

1. **Series/TV Shows:**
   - URLs containing `/series/`
   - Group titles containing "SRS"
   - Names containing season/episode patterns (S01E01, etc.)

2. **Movies:**
   - URLs containing `/movie/`
   - Group titles containing "VOD"
   - Names containing years (1950-2030)
   - Categories containing movie-related keywords

3. **Other VOD Content:**
   - Categories containing "DOWNLOAD", "ON DEMAND", "RENTAL"

## Input/Output

- **Default input file:** `filtered.m3u`
- **Default output file:** `live_channels.m3u`
- **Custom files:** Can be specified via command line arguments or Makefile variables

### Command Line Usage
```bash
python filter_live_channels.py [input_file] [output_file]
```

### Makefile Usage
```bash
make run INPUT_FILE=source.m3u OUTPUT_FILE=destination.m3u
```

## Filtering Logic

The scripts use multiple criteria to identify content to filter:

### Series Detection
- Group title contains "SRS"
- URL path contains "/series/"
- Title contains season/episode indicators (S01, E01, "Season", "Episode")
- Title matches SxxExx pattern

### Movie Detection
- Group title contains "VOD"
- URL path contains "/movie/"
- Title contains a 4-digit year (1950-2030)
- Group title contains movie keywords ("MOVIE", "FILM", "CINEMA")

### Live Channel Detection
- Any entry that doesn't match series or movie criteria
- Typically includes live TV broadcasts, news channels, sports channels, etc.

## Customization

You can modify the filtering criteria by editing the filtering logic in the script:

1. **Add new keywords** to detect movies or series
2. **Modify year range** for movie detection
3. **Add new URL patterns** for different streaming services
4. **Customize category filters** based on your playlist structure

## Notes

- The script preserves the original M3U format with all metadata (logos, categories, TVG info)
- Recommended to use a virtual environment for dependency management