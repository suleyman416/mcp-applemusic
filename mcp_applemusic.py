import subprocess

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
def itunes_shuffle(enabled: bool) -> str:
    """Enable or disable shuffle mode in Music."""
    val = "true" if enabled else "false"
    script = f'tell application "Music" to set shuffle enabled to {val}'
    return run_applescript(script)


def main():
    mcp.run()


if __name__ == "__main__":
    main()

