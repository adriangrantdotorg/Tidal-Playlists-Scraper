import asyncio
import csv
import json
import os
import datetime
from playwright.async_api import async_playwright

# Generate output filename with timestamp
# Format: tidal_tracks_SCRAPED MM-dd-yy__h.mm.ss a.csv
current_time = datetime.datetime.now().strftime("%m-%d-%y__%I.%M.%S %p")
output_file = f"tidal_tracks_SCRAPED {current_time}.csv"

def load_playlists(filename="playlists.json"):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return []
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []

async def scrape_playlist(page, playlist):
    print(f"Scraping: {playlist['name']} ({playlist['url']})")
    try:
        await page.goto(playlist['url'])
        # Wait for the tracklist to load. Adjust selector as needed based on Tidal's actual DOM.
        # Looking for a generic track row or waiting for network idle.
        try:
           await page.wait_for_selector('[data-test="tracklist-row"]', timeout=10000)
        except:
           print(f"  - Timeout waiting for tracklist on {playlist['name']}")
           return []

        # Extract tracks
        # This evaluation script runs in the browser context
        tracks_data = await page.evaluate('''() => {
            const tracks = [];
            // Using the selector found in debugging: data-test="tracklist-row" for rows
            const rows = document.querySelectorAll('[data-test="tracklist-row"]');
            
            rows.forEach(row => {
                // Selector found in debugging: data-test="track-row-date-added"
                const dateAddedCell = row.querySelector('[data-test="track-row-date-added"]');
                if (!dateAddedCell) return;
                
                const dateText = dateAddedCell.innerText.trim();
                const lowerDateText = dateText.toLowerCase();
                
                if (lowerDateText === "yesterday" || lowerDateText === "this week") {
                    const titleElement = row.querySelector('[data-test="table-row-title"] [data-test="table-cell-title"]');
                    
                    // Artist selector update: inside ._artistColumn_... -> span -> a
                    const artistElement = row.querySelector('[data-test="track-row-artist"] a'); 
                    
                    // Album selector update: inside ._albumColumn_... -> a
                    const albumElement = row.querySelector('[data-test="track-row-album"] a');
                    
                    tracks.push({
                        "Title": titleElement ? titleElement.innerText.trim() : "Unknown Title",
                        "Artist": artistElement ? artistElement.innerText.trim() : "Unknown Artist",
                        "Album": albumElement ? albumElement.innerText.trim() : "Unknown Album",
                        "Date Added": dateText
                    });
                }
            });
            return tracks;
        }''')
        
        print(f"  - Found {len(tracks_data)} matching tracks.")
        # Add source playlist to each track
        for track in tracks_data:
            track["Source Playlist"] = playlist['name']
            
        return tracks_data

    except Exception as e:
        print(f"  - Error scraping {playlist['name']}: {e}")
        return []

async def main():
    playlists = load_playlists()
    if not playlists:
        return

    all_tracks = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        for playlist in playlists:
            tracks = await scrape_playlist(page, playlist)
            all_tracks.extend(tracks)
        
        await browser.close()

    if all_tracks:
        print(f"\nTotal matches found before deduping: {len(all_tracks)}")
        
        # Remove duplicates based on Artist, Album, Title
        unique_tracks = []
        seen_tracks = set()
        
        for track in all_tracks:
            # Create a unique key for the track
            track_key = (track['Artist'], track['Album'], track['Title'])
            
            if track_key not in seen_tracks:
                seen_tracks.add(track_key)
                unique_tracks.append(track)
                
        print(f"Total unique matches found: {len(unique_tracks)}")

        # Write to CSV
        keys = ["Title", "Artist", "Album", "Source Playlist", "Date Added"]
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(unique_tracks)
        print(f"Saved to {output_file}")
        
        # Trigger Spotify Export
        print("\n--- Starting Spotify Export ---")
        import subprocess
        try:
            subprocess.run(["python3", "export_to_spotify.py", output_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running Spotify export: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    else:
        print("\nNo matching tracks found (Yesterday/This Week).")
        # Create empty CSV with headers just in case
        keys = ["Title", "Artist", "Album", "Source Playlist", "Date Added"]
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
        print(f"Created empty {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
