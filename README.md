# MCP-AppleMusic

A FastMCP server for controlling Apple Music on macOS.

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

The following **60 tools** are available through the MCP server:

```python
# 1. Playback & Track Control
itunes_play()                              # Start playback
itunes_pause()                             # Pause playback
itunes_next()                              # Skip to next track
itunes_previous()                          # Go to previous track
itunes_current_track()                     # Get currently playing track info
itunes_set_volume(volume)                  # Set volume (0–100)
itunes_mute(muted)                         # Mute or unmute audio
itunes_shuffle(enabled)                    # Enable or disable shuffle
itunes_set_shuffle_mode(mode)              # Set shuffle granularity ('songs', 'albums', 'groupings')
itunes_repeat(mode)                        # Set repeat mode ('off', 'one', 'all')
itunes_seek(seconds)                       # Seek/jump to timestamp in seconds
itunes_get_position()                      # Get elapsed position & total duration
itunes_favorite_track(favorited)           # Favorite or unfavorite currently playing track
itunes_favorite_song(song, favorited)      # Favorite or unfavorite any song by title
itunes_dislike_track(disliked)             # Mark current track as Disliked for algorithms
itunes_rate_track(stars)                   # Set star rating (1–5 stars)
itunes_favorite_album(favorited)           # Star or unstar currently playing album
itunes_rate_album(stars)                   # Set star rating on currently playing album
itunes_get_lyrics(song)                    # Get lyrics with global database fallback
itunes_set_eq(preset)                      # Set Equalizer preset (e.g. 'Hip-Hop', 'Bass Booster')
itunes_open_location(url)                  # Stream audio URL or music:// link
itunes_get_stream_info()                   # Get live radio / stream station title & URL

# 2. Audio Quality & Technical Inspection
itunes_get_track_audio_info(song)          # Inspect bit rate, sample rate, BPM, cloud status, format
itunes_set_track_bpm(bpm, song)            # Set BPM tempo on a track
itunes_set_track_start_finish(start, finish, song) # Set custom start/finish offsets
itunes_set_track_volume_adjustment(adj, song) # Set track volume adjustment (-100% to +100%)

# 3. Deep Tagging & Metadata Editor
itunes_get_track_metadata(song)            # Inspect genre, composer, track/disc numbers, comments, dates
itunes_edit_track_metadata(song, genre, composer, comment, year, track_number) # Update metadata tags
itunes_get_artwork_info(song)              # Inspect album artwork format, description & status

# 4. Library, Catalog & Artist Discovery
itunes_search(query)                       # Search local/iCloud library for tracks
itunes_search_catalog(query, limit)        # Search global Apple Music catalog (100M+ tracks)
itunes_get_artist_top_tracks(artist, limit)# Get top songs for any artist worldwide
itunes_get_artist_albums(artist, limit)    # Get official albums for any artist worldwide
itunes_play_song(song)                     # Find and play a specific song

# 5. Playlist & Folder Management
itunes_create_playlist(name)               # Create a new playlist
itunes_create_playlist_folder(name)        # Create a playlist folder
itunes_move_playlist_to_folder(playlist, folder) # Move playlist into a folder
itunes_set_playlist_description(playlist, description) # Set playlist description
itunes_add_to_playlist(song, playlist)     # Add a song to a named playlist (cross-playlist search)
itunes_remove_from_playlist(song, playlist)# Remove a track from a playlist by song title
itunes_move_playlist_track(playlist, from, to) # Move track position in playlist
itunes_sort_playlist(playlist, sort_by)    # Sort playlist by 'title', 'artist', or 'album'
itunes_favorite_playlist(playlist, favorited)# Star or unstar a playlist in sidebar
itunes_duplicate_playlist(source, new_name)# Clone an existing playlist into a new one
itunes_merge_playlists(play_a, play_b, new)# Merge two playlists into a new master playlist
itunes_find_duplicates(playlist, remove)   # Detect duplicate tracks in a playlist
itunes_delete_playlist(playlist)           # Delete a user playlist
itunes_list_playlists()                    # List all playlists with track counts
itunes_get_playlist_tracks(playlist)       # Get all tracks in a playlist
itunes_export_playlist(playlist, format)   # Export playlist to JSON, CSV, or Markdown

# 6. Listening Journal & Replay Analytics
itunes_get_monthly_replay(year, month)     # Generate Apple Music Replay report (hours, top songs/artists)
itunes_get_listening_history(limit, artist)# Chronological playback journal with timestamps & skips
itunes_get_listening_stats_by_date(start, end) # Custom date-range listening analytics & top charts
itunes_log_current_play()                  # Manually record current track to journal database

# 7. Audio Devices & UI Controls
itunes_list_devices()                      # List AirPlay audio output devices & active status
itunes_set_device(device_name)             # Switch audio output device (AirPods, HomePod, TV)
itunes_set_device_volume(device, volume)   # Set individual volume for specific AirPlay device
itunes_get_selected_tracks()               # Get tracks highlighted by user in Music window
itunes_set_miniplayer(enabled)             # Toggle MiniPlayer window mode
itunes_reveal_track(song)                  # Reveal & highlight track in Music window
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
git clone https://github.com/suleyman416/mcp-applemusic.git
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
