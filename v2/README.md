# M3U Playlist Filter Script

This directory contains a Python script to filter M3U playlists by removing series and movies, keeping only live TV channels.

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

# Run with default files (filtered.m3u -> live_channels.m3u)
python filter_live_channels.py

# Run with custom input file
python filter_live_channels.py my_input.m3u

# Run with custom input and output files
python filter_live_channels.py input.m3u output.m3u

# Show help
python filter_live_channels.py --help
```

## Script Details

### `filter_live_channels.py`

**Requirements:**
- Python 3.6+
- m3u_parser library

**Features:**
- Uses the robust m3u_parser library for parsing
- Handles complex M3U file structures
- More reliable parsing of metadata

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