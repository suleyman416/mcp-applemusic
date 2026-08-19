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

The following **40 tools** are available through the MCP server:

```python
# Playback & track control
itunes_play()                              # Start playback
itunes_pause()                             # Pause playback
itunes_next()                              # Skip to next track
itunes_previous()                          # Go to previous track
itunes_current_track()                     # Get currently playing track info
itunes_set_volume(volume)                  # Set volume (0–100)
itunes_shuffle(enabled)                    # Enable or disable shuffle
itunes_repeat(mode)                        # Set repeat mode ('off', 'one', 'all')
itunes_seek(seconds)                       # Seek/jump to timestamp in seconds
itunes_get_position()                      # Get elapsed position & total duration
itunes_favorite_track(favorited)           # Favorite or unfavorite currently playing track
itunes_favorite_song(song, favorited)      # Favorite or unfavorite any song by title
itunes_dislike_track(disliked)             # Mark current track as Disliked for algorithms
itunes_rate_track(stars)                   # Set star rating (1–5 stars)
itunes_get_lyrics(song)                    # Get lyrics for currently playing track or searched song
itunes_set_eq(preset)                      # Set Apple Music Equalizer preset (e.g. 'Hip-Hop', 'Bass Booster')

# Library, catalog & artist search
itunes_search(query)                       # Search local/iCloud library for tracks
itunes_search_catalog(query, limit)        # Search global Apple Music catalog (100M+ tracks)
itunes_get_artist_top_tracks(artist, limit)# Get top 10 songs for any artist in global catalog
itunes_get_artist_albums(artist, limit)    # Get official albums for any artist in global catalog
itunes_play_song(song)                     # Find and play a specific song

# Playlist & export management
itunes_create_playlist(name)               # Create a new playlist
itunes_add_to_playlist(song, playlist)     # Add a song to a named playlist (cross-playlist search)
itunes_remove_from_playlist(song, playlist)# Remove a track from a playlist by song title
itunes_move_playlist_track(playlist, from, to) # Move track from one position to another
itunes_sort_playlist(playlist, sort_by)    # Sort playlist by 'title', 'artist', or 'album'
itunes_favorite_playlist(playlist, favorited)# Star or unstar a playlist in the sidebar
itunes_duplicate_playlist(source, new_name)# Clone an existing playlist into a new one
itunes_merge_playlists(play_a, play_b, new)# Merge two playlists into a new master playlist
itunes_find_duplicates(playlist, remove)   # Detect duplicate tracks in a playlist
itunes_delete_playlist(playlist)           # Delete a user playlist
itunes_list_playlists()                    # List all playlists with track counts
itunes_get_playlist_tracks(playlist)       # Get all tracks in a playlist
itunes_export_playlist(playlist, format)   # Export playlist to JSON, CSV, or Markdown

# Listening journal & monthly replay (NEW)
itunes_get_monthly_replay(year, month)     # Generate Apple Music Replay report (hours, top songs/artists)
itunes_get_listening_history(limit, artist)# Chronological playback journal with timestamps & skips
itunes_get_listening_stats_by_date(start, end) # Custom date-range listening analytics & top charts
itunes_log_current_play()                  # Manually record current track to journal database

# Audio output & library analytics
itunes_list_devices()                      # List AirPlay audio output devices & active status
itunes_set_device(device_name)             # Switch audio output device (AirPods, HomePod, TV)
itunes_get_stats()                         # Generate library analytics (tracks, hours, favorites)
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
- `itunes_search_catalog` queries the global Apple Music store (100M+ tracks) for metadata & discovery. Playback and playlist modifications (`itunes_add_to_playlist`) apply to tracks saved in your Apple Music Library due to AppleScript macOS boundaries.
