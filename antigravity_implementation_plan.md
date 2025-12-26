# Tidal Multi-Playlist CSV Export Plan (Source Column Update)

## Goal Description
Update the consolidated CSV to include a column for "Source Page" (the name of the playlist the track was found on).

## User Review Required
None.

## Proposed Steps

### 1. Re-Scrape with Source Name
- Launch Browser Subagent.
- **Process List**: Same 4 URLs.
- **Action per Playlist**:
    - Navigate.
    - Extract **Playlist Name** (from page top `<h1>` or metadata).
    - Sort terms: "Date Added".
    - Filter: "Yesterday" OR "This Week".
    - Extract: Title, Artist, Album, **Source Page** (Playlist Name).

### 2. Export Update
- Overwrite `tidal_tracks_consolidated_2025-12-20.csv`.
- Format: `Title,Artist,Album,Source Page`.

### 3. Verification
- Verify "Source Page" column exists and is populated.
- Reveal in Finder.
