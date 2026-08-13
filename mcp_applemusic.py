import json
import subprocess
import urllib.parse
import urllib.request

from mcp.server.fastmcp import FastMCP


def run_applescript(script: str) -> str:
    """Execute an AppleScript command via osascript and return its output."""
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr.strip()}"
    return result.stdout.strip()


# Instantiate the MCP server.
mcp = FastMCP("iTunesControlServer")


@mcp.tool()
def itunes_play() -> str:
    """Start playback in Music (iTunes)."""
    script = 'tell application "Music" to play'
    return run_applescript(script)


@mcp.tool()
def itunes_pause() -> str:
    """Pause playback in Music (iTunes)."""
    script = 'tell application "Music" to pause'
    return run_applescript(script)


@mcp.tool()
def itunes_next() -> str:
    """Skip to the next track."""
    script = 'tell application "Music" to next track'
    return run_applescript(script)


@mcp.tool()
def itunes_previous() -> str:
    """Return to the previous track."""
    script = 'tell application "Music" to previous track'
    return run_applescript(script)


@mcp.tool()
def itunes_search(query: str) -> str:
    """
    Search the Music library for tracks whose names contain the given query.
    Returns a list of tracks formatted as "Track Name - Artist".
    """
    script = f"""
    tell application "Music"
        set results to search playlist "Library" for "{query}"
        set output to ""
        repeat with t in results
            set output to output & name of t & " - " & artist of t & "\n"
        end repeat
        return output
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_search_catalog(query: str, limit: int = 5) -> str:
    """
    Search the global Apple Music / iTunes Store catalog (outside user library).

    Args:
        query: Search term (song title, artist, or album).
        limit: Number of results to return (default 5, max 25).

    Returns:
        Formatted list of matching tracks from the global Apple Music catalog.
    """
    safe_limit = min(max(1, limit), 25)
    encoded_query = urllib.parse.quote(query)
    url = f"https://itunes.apple.com/search?term={encoded_query}&media=music&entity=song&limit={safe_limit}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            results = data.get("results", [])
            if not results:
                return f"No tracks found in Apple Music catalog for: '{query}'"

            output = []
            for item in results:
                track_name = item.get("trackName", "Unknown")
                artist_name = item.get("artistName", "Unknown")
                collection_name = item.get("collectionName", "Unknown Album")
                release_date = item.get("releaseDate", "")[:4]
                output.append(f"{track_name} - {artist_name} ({collection_name}, {release_date})")

            return "\n".join(output)
    except Exception as e:
        return f"Error querying iTunes catalog: {str(e)}"



@mcp.tool()
def itunes_play_song(song: str) -> str:
    """
    Search for and play a specific song by name.
    Plays the first matching track found in the library.
    """
    script = f"""
    tell application "Music"
        set results to search playlist "Library" for "{song}"
        if results is not {{}} then
            play item 1 of results
            return "Now playing: " & name of item 1 of results & " - " & artist of item 1 of results
        else
            return "No tracks found matching: {song}"
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_create_playlist(name: str) -> str:
    """Create a new playlist in Music with the given name."""
    script = f"""
    tell application "Music"
        if not (exists playlist "{name}") then
            make new playlist with properties {{name:"{name}"}}
            return "Created playlist: {name}"
        else
            return "Playlist already exists: {name}"
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_add_to_playlist(song: str, playlist: str) -> str:
    """
    Search for a song by title across all playlists and add the first match
    to the named playlist.

    This tool searches across every user playlist (not just the main Library),
    which is necessary when tracks are sourced from Apple Music subscription
    or iCloud Music Library and may not appear in the default Library playlist.

    Args:
        song: The song title to search for.
        playlist: The name of the destination playlist.

    Returns:
        A status message indicating which track was added, or an error if not found.
    """
    script = f"""
    tell application "Music"
        set targetPlaylist to playlist "{playlist}"
        set searchTerm to "{song}"
        set seen to {{}}

        -- Search across all user playlists to handle iCloud/subscription tracks
        repeat with p in (every user playlist)
            try
                set allTracks to tracks of p
                repeat with t in allTracks
                    set tid to database ID of t as string
                    if seen does not contain tid then
                        set end of seen to tid
                        if (name of t) contains searchTerm then
                            duplicate t to targetPlaylist
                            return "Added: " & name of t & " - " & artist of t
                        end if
                    end if
                end repeat
            end try
        end repeat

        return "Not found: " & searchTerm
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_list_playlists() -> str:
    """
    List all playlists in the Music library with their track counts.

    Returns:
        A newline-separated list of playlists in the format "Playlist Name (N tracks)".
    """
    script = """
    tell application "Music"
        set output to ""
        repeat with p in (every user playlist)
            try
                set output to output & name of p & " (" & (count of tracks of p) & " tracks)\\n"
            end try
        end repeat
        return output
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_get_playlist_tracks(playlist: str) -> str:
    """
    Get all tracks in a named playlist.

    Args:
        playlist: The name of the playlist to inspect.

    Returns:
        A newline-separated list of tracks formatted as "Track Name - Artist".
    """
    script = f"""
    tell application "Music"
        if not (exists playlist "{playlist}") then
            return "Playlist not found: {playlist}"
        end if
        set output to ""
        repeat with t in (tracks of playlist "{playlist}")
            set output to output & name of t & " - " & artist of t & "\\n"
        end repeat
        return output
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_current_track() -> str:
    """Get information about the currently playing track."""
    script = """
    tell application "Music"
        if player state is playing then
            set t to current track
            return "Now playing: " & name of t & " - " & artist of t & " (" & album of t & ")"
        else
            return "Music is not currently playing."
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_set_volume(volume: int) -> str:
    """Set the Music app volume (0-100)."""
    if not 0 <= volume <= 100:
        return "Error: Volume must be between 0 and 100."
    script = f'tell application "Music" to set sound volume to {volume}'
    return run_applescript(script)


@mcp.tool()
def itunes_favorite_track(favorited: bool = True) -> str:
    """
    Favorite or unfavorite the currently playing track.

    Args:
        favorited: True to favorite/love the track, False to unfavorite.
    """
    val = "true" if favorited else "false"
    script = f"""
    tell application "Music"
        if player state is playing then
            set t to current track
            set favorited of t to {val}
            if {val} then
                set status to "Favorited"
            else
                set status to "Unfavorited"
            end if
            return status & ": " & name of t & " - " & artist of t
        else
            return "Music is not currently playing."
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_rate_track(stars: int) -> str:
    """
    Set a star rating (1 to 5 stars) for the currently playing track.

    Args:
        stars: Rating from 1 (lowest) to 5 (highest), or 0 to clear rating.
    """
    if not 0 <= stars <= 5:
        return "Error: Rating stars must be between 0 and 5."
    rating_val = stars * 20
    script = f"""
    tell application "Music"
        if player state is playing then
            set t to current track
            set rating of t to {rating_val}
            return "Set rating to " & {stars} & " star(s) for: " & name of t & " - " & artist of t
        else
            return "Music is not currently playing."
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_get_lyrics() -> str:
    """Get the lyrics for the currently playing track."""
    script = """
    tell application "Music"
        if player state is playing then
            set t to current track
            set l to lyrics of t
            if l is not "" then
                return "Lyrics for " & name of t & " - " & artist of t & ":\n\n" & l
            else
                return "No lyrics found in Music app for: " & name of t & " - " & artist of t
            end if
        else
            return "Music is not currently playing."
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_seek(seconds: int) -> str:
    """
    Seek/jump to a specific timestamp in seconds in the currently playing track.

    Args:
        seconds: Position in seconds from the start of the song.
    """
    if seconds < 0:
        return "Error: Seconds must be 0 or positive."
    script = f"""
    tell application "Music"
        if player state is playing then
            set player position to {seconds}
            return "Jumped to " & {seconds} & "s in: " & name of current track
        else
            return "Music is not currently playing."
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_get_position() -> str:
    """Get elapsed time and total duration for the currently playing track."""
    script = """
    tell application "Music"
        if player state is playing then
            set pos to player position as integer
            set dur to duration of current track as integer
            set posMin to pos div 60
            set posSec to pos mod 60
            set durMin to dur div 60
            set durSec to dur mod 60
            return "Position: " & posMin & "m" & posSec & "s / " & durMin & "m" & durSec & "s (" & name of current track & ")"
        else
            return "Music is not currently playing."
        end if
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_list_devices() -> str:
    """List all available AirPlay audio output devices and their selection state."""
    script = """
    tell application "Music"
        set output to ""
        repeat with d in (every AirPlay device)
            if selected of d then
                set sel to "[Active]"
            else
                set sel to "[Available]"
            end if
            set output to output & name of d & " " & sel & "\n"
        end repeat
        return output
    end tell
    """
    return run_applescript(script)



@mcp.tool()
def itunes_set_device(device_name: str) -> str:
    """
    Switch audio output to a specific AirPlay device by name (e.g. HomePod, AirPods, TV).

    Args:
        device_name: The exact name of the AirPlay device.
    """
    script = f"""
    tell application "Music"
        try
            set selected of (first AirPlay device whose name is "{device_name}") to true
            return "Selected AirPlay device: {device_name}"
        on error
            return "AirPlay device not found: {device_name}"
        end try
    end tell
    """
    return run_applescript(script)


@mcp.tool()
def itunes_export_playlist(playlist: str, format: str = "json") -> str:
    """
    Export all tracks in a named playlist to JSON, CSV, or Markdown.

    Args:
        playlist: The name of the playlist to export.
        format: Export format: 'json', 'csv', or 'markdown' (default 'json').
    """
    script = f"""
    tell application "Music"
        if not (exists playlist "{playlist}") then
            return "Playlist not found: {playlist}"
        end if
        set output to ""
        repeat with t in (tracks of playlist "{playlist}")
            set output to output & (name of t) & "|||" & (artist of t) & "|||" & (album of t) & "\n"
        end repeat
        return output
    end tell
    """
    raw = run_applescript(script)
    if raw.startswith("Playlist not found") or raw.startswith("Error:"):
        return raw

    items = []
    for line in raw.strip().splitlines():
        parts = line.split("|||")
        if len(parts) == 3:
            items.append({"title": parts[0], "artist": parts[1], "album": parts[2]})

    fmt = format.lower().strip()
    if fmt == "csv":
        lines = ["Title,Artist,Album"]
        for i in items:
            t = i["title"].replace('"', '""')
            a = i["artist"].replace('"', '""')
            al = i["album"].replace('"', '""')
            lines.append(f'"{t}","{a}","{al}"')
        return "\n".join(lines)
    elif fmt == "markdown" or fmt == "md":
        lines = [f"# Playlist: {playlist}", "", "| # | Title | Artist | Album |", "|---|---|---|---|"]
        for idx, i in enumerate(items, 1):
            lines.append(f'| {idx} | {i["title"]} | {i["artist"]} | {i["album"]} |')
        return "\n".join(lines)
    else:
        return json.dumps({"playlist": playlist, "count": len(items), "tracks": items}, indent=2)


@mcp.tool()
def itunes_get_stats() -> str:
    """Generate analytics summary of the Music library (total tracks, playlists, favorites, and hours)."""
    script = """
    tell application "Music"
        set totalT to count of tracks of playlist "Library"
        set totalP to count of user playlists
        set totalDur to 0
        set favCount to 0
        
        repeat with t in (tracks of playlist "Library")
            try
                set totalDur to totalDur + (duration of t)
            end try
            try
                if favorited of t is true then set favCount to favCount + 1
            end try
        end repeat
        
        set totalHours to (totalDur / 3600) as integer
        return "Library Statistics:\n" & "- Total Tracks: " & totalT & "\n- Total Playlists: " & totalP & "\n- Favorited Tracks: " & favCount & "\n- Total Playtime: ~" & totalHours & " hours"
    end tell
    """
    return run_applescript(script)


def main():
    mcp.run()


if __name__ == "__main__":
    main()


