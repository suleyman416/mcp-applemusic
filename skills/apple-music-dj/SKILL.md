---
name: apple-music-dj
description: Controls Apple Music on macOS and acts as an autonomous AI DJ. Use when the user asks to play music, search songs or albums, control volume or AirPlay devices, manage playlists, view listening history or replay stats, fetch lyrics, import Spotify links, or perform seamless harmonic mixing and beat-matched transitions.
license: MIT
compatibility: macOS with Music.app, uv package manager, and apple-music-mcp
metadata:
  author: suleyman416
  version: "1.0.0"
  repository: https://github.com/suleyman416/mcp-applemusic
---

# Apple Music DJ & Playback Controller

A production-grade agent skill to control Apple Music natively on macOS and deliver professional, beat-matched DJ sets using the `mcp-applemusic` FastMCP server.

---

## 1. Prerequisites & Environment Setup

This skill communicates with macOS **Music.app** via AppleScript through the `mcp-applemusic` server.

### Agent MCP Configuration
To equip your agent with the tools, ensure `apple-music-mcp` is configured in your agent's MCP settings:

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "applemusic": {
      "command": "uvx",
      "args": ["apple-music-mcp"]
    }
  }
}
```

**For Cursor / Windsurf / VS Code** (`.cursor/mcp.json` or Cline settings):
```json
{
  "mcpServers": {
    "applemusic": {
      "command": "uvx",
      "args": ["apple-music-mcp"]
    }
  }
}
```

> **macOS Permission Note**: On first execution, macOS will prompt to grant the host application permission to control "Music". Users must click **Allow** (or toggle it on under **System Settings → Privacy & Security → Automation**).

---

## 2. Tool Reference & Execution Workflows

### Playback & Audio Controls
* **Play / Resume**: Call `itunes_play` or `itunes_play_song(song_name, artist_name)`.
* **Pause / Stop**: Call `itunes_pause`.
* **Skip / Previous**: Call `itunes_next` or `itunes_previous`.
* **Volume Control**: Call `itunes_set_volume(volume)` (0–100 scale).
* **Multi-Room & AirPlay Devices**: Call `itunes_list_devices` to inspect connected devices, and `itunes_set_device(device_name)` or `itunes_set_device_volume(device_name, volume)` to adjust remote AirPlay endpoints.
* **Equalizer & Modes**: Call `itunes_set_eq(preset)` (e.g. "Hip-Hop", "Electronic", "Acoustic"), `itunes_set_shuffle_mode(mode)`, and `itunes_repeat(mode)`.

### Search & Music Discovery
* **Local Library Search**: Call `itunes_search(query)` for locally added/downloaded music.
* **Apple Music Catalog Search**: Call `itunes_search_catalog(query, entity)` to search the entire worldwide Apple Music streaming catalog.
* **Charts & New Releases**: Call `itunes_get_top_charts(genre)` or `itunes_get_new_releases()`.
* **Universal Share Links**: Call `itunes_generate_share_link(song_name, artist)` to create a universal `song.link` / Odesli link spanning Spotify, YouTube Music, and Tidal.
* **Spotify Importer**: Call `itunes_import_from_spotify(spotify_url)` to parse public Spotify playlists/albums and import matching tracks into Apple Music without API keys.
* **Synchronized Lyrics**: Call `itunes_get_lyrics(song_name, artist_name)` to pull synced lyrics from LRCLIB.

### Playlist Engineering & Deduplication
* **Create & Organize**: Call `itunes_create_playlist(name, description)` or create folders with `itunes_create_playlist_folder(folder_name)`.
* **Deduplication**: Run `itunes_find_duplicates(playlist_name)` followed by `itunes_remove_from_playlist(playlist_name, track_id)`.
* **Smart Sorting**: Call `itunes_sort_playlist(playlist_name, sort_by)` (e.g., BPM, release date, artist).
* **Exporting**: Call `itunes_export_playlist(playlist_name, format)` (`json`, `csv`, or `markdown`).

### Listening Analytics & Replay Journal
* **Current Status**: Call `itunes_current_track` to get the playing title, artist, album, duration, and elapsed time.
* **Listening History**: Call `itunes_get_listening_history(limit)`.
* **Monthly Replay**: Call `itunes_get_monthly_replay(month, year)` to view top artists, top tracks, total listening minutes, and genre breakdown.
* **Personality Profile**: Call `itunes_get_listening_personality()` to generate an auditory persona based on listening trends.

---

## 3. Autonomous Smart DJ Protocol

When the user asks you to act as a DJ, create a mix, transition tracks, or manage tempos, strictly enforce these rules:

### A. Phrasing & Downbeat Timing
Music (especially hip-hop, electronic, grime, pop, and house) is built on **4-bar (16-beat)** and **8-bar (32-beat)** phrases.
1. **Never cut mid-sentence into an instrumental buffer.** An abrupt cut in the middle of a verse breaks the groove.
2. **Transition Type A — Vocal Drop on the One (Vocal-to-Vocal):**
   * Wait until the outgoing track completes its 8-bar verse or chorus on Beat 4.
   * Start the incoming track on Beat 1 directly on its opening vocal.
3. **Transition Type B — Instrumental Beat Bridge (Beat-to-Beat):**
   * If the incoming track begins with a drum intro before vocals, wait until the outgoing track hits an instrumental breakdown or outro before triggering the transition.

### B. Energy Escalation & Progressive BPM Stepping
Escalate tempo progressively to build dancefloor momentum:
* **Warmup / Groove**: 108–118 BPM (Afrobeats, R&B, slow-burn funk)
* **Mid-Tempo Bounce**: 120–130 BPM (House, UK Funky, Afro-house)
* **Peak Energy**: 138–144 BPM (Grime, UK Drill, Techno)
* **Overdrive**: 146–152 BPM (High-tempo grime, drum & bass half-time)

Avoid jarring negative BPM drops unless executing an intentional half-time switch (e.g., 140 BPM drill transitioning into a 70/140 BPM trap beat).

### C. Zero-Latency Execution Pipeline
1. **Pre-Warming**: Pre-resolve the incoming track pointer (`tNext`) while the current track is actively playing.
2. **Pre-Set Offsets**: Pre-calculate and configure `itunes_set_track_start_finish(track_id, start_sec, finish_sec)` ahead of time to eliminate intro silence or outro dead air.
3. **Atomic Execution**: At transition time, trigger only the atomic switch to avoid latency spikes.

### D. Volume & Dynamics Discipline
* Maintain steady master volume (75–80%).
* Never plummet volume to 0% and surge to 100% on every song switch. Energy is created through track selection, bassline shifts, and tempo climb, not fader bouncing.

---

## 4. Troubleshooting & Best Practices

1. **"Not authorized to send Apple events to Music"**:
   * Open **System Settings → Privacy & Security → Automation**.
   * Locate the calling client (Terminal, Claude, Cursor, Windsurf) and ensure the checkmark next to **Music** is turned ON.
2. **Track Not Found in Catalog**:
   * Fallback: query with just the title or alternate spelling, or check local library using `itunes_search`.
3. **Zero Hallucination Policy**:
   * Never fabricate lyrics or playback statuses. Always pull real-time data from `itunes_current_track` or `itunes_get_lyrics`.
