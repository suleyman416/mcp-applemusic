[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/kennethreitz-mcp-applemusic-badge.png)](https://mseep.ai/app/kennethreitz-mcp-applemusic)

# MCP-AppleMusic

A FastMCP server implementation for controlling Apple Music (formerly iTunes) on macOS through AppleScript commands.

## Requirements

- Python 3.13+
- macOS with Apple Music app installed
- MCP library ≥1.2.1

## Installation

First, ensure you have uv installed:
```bash
$ brew install uv
```

Then, with **Claude Desktop**, add the following to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "iTunesControlServer": {
      "command": "uvx",
      "args": ["-p", "3.13", "-n", "mcp-applemusic"]
    }
  }
}
```

> **Note:** If you encounter an `ImportError` for `mcp.server.fastmcp` (removed in `mcp` SDK ≥ 1.9), install the standalone package: `pip install fastmcp`. The server will automatically fall back to it.

## Available Commands

The following commands are available through the MCP server:

```python
# Playback control
itunes_play()                              # Start playback
itunes_pause()                             # Pause playback
itunes_next()                              # Skip to next track
itunes_previous()                          # Go to previous track
itunes_current_track()                     # Get currently playing track info
itunes_set_volume(volume)                  # Set volume (0–100)
itunes_shuffle(enabled)                    # Enable or disable shuffle

# Library & search
itunes_search(query)                       # Search library for tracks
itunes_play_song(song)                     # Find and play a specific song

# Playlist management
itunes_create_playlist(name)               # Create a new playlist
itunes_add_to_playlist(song, playlist)     # Add a song to a named playlist
itunes_list_playlists()                    # List all playlists with track counts
itunes_get_playlist_tracks(playlist)       # Get all tracks in a playlist
```

## Usage

Start the server:

```bash
python mcp_applemusic.py
```

Example interactions:

```python
# Search for a song
results = itunes_search("Funky Friday")

# Play a specific song
itunes_play_song("Funky Friday")

# Check what's playing
itunes_current_track()

# Create a playlist and add songs to it
itunes_create_playlist("My Favourites")
itunes_add_to_playlist("Funky Friday", "My Favourites")
itunes_add_to_playlist("Essence", "My Favourites")

# See all your playlists
itunes_list_playlists()

# See what's in a playlist
itunes_get_playlist_tracks("My Favourites")

# Control playback
itunes_set_volume(80)
itunes_shuffle(True)
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/kennethreitz/mcp-applemusic.git
cd mcp-applemusic
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Notes

- This tool only works on macOS systems due to its AppleScript dependency
- Requires Apple Music (formerly iTunes) to be installed
- Apple Music subscription and iCloud Music Library tracks are fully supported
