# Privacy Policy for MCP-AppleMusic

**Last Updated:** September 2026

`mcp-applemusic` is an open-source Model Context Protocol (MCP) server for macOS designed to enable AI assistants (including Claude Desktop, Cursor, and custom agents) to interact with the local Apple Music application.

Your privacy and security are foundational principles of this project.

---

## 1. Local-First Architecture & Data Storage

* **100% Local Execution:** `mcp-applemusic` executes locally on your macOS machine via standard input/output (`stdio`).
* **Listening Journal:** If listening history is logged or synced, playback timestamps, track names, and artist information are stored in a local SQLite database located on your machine at `~/.apple_music_history.db`.
* **Zero Cloud Data Exfiltration:** The local database is never uploaded, synced to external cloud databases, or shared with third-party tracking services.

---

## 2. External Network Communications

The server makes outbound network requests only when explicitly instructed to invoke tools that require public data. All external communications are **anonymous HTTP GET requests** and do not transmit personal user credentials or Apple ID data:

* **LRCLIB (`lrclib.net`):** Used exclusively to fetch public synchronized and plain text song lyrics.
* **Apple iTunes Search API (`itunes.apple.com`):** Used to query public track previews and catalog metadata.
* **Apple Marketing Feeds (`rss.applemarketingtools.com`):** Used to retrieve public Top Charts and New Releases.
* **Spotify Public Web (`open.spotify.com`):** Used to parse publicly accessible tracks and albums for cross-platform migration.
* **Songlink / Odesli (`api.song.link`):** Used to generate universal shareable streaming links.
* **MusicBrainz (`musicbrainz.org`):** Used as an optional fallback for public track BPM calculations.

---

## 3. Credentials & Apple ID Security

* `mcp-applemusic` **never** requests, accesses, stores, or transmits your Apple ID password, credit card information, or auth tokens.
* All Apple Music playback and library actions are executed locally through macOS AppleScript / Apple Events system permissions (`osascript`).

---

## 4. Telemetry & Analytics

* `mcp-applemusic` contains **zero telemetry, tracking beacons, or analytics SDKs**.

---

## 5. Contact & Audits

For questions or security disclosures, please open an issue on the official GitHub repository:
[https://github.com/suleyman416/mcp-applemusic](https://github.com/suleyman416/mcp-applemusic)
