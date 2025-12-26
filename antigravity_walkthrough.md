# Multi-Playlist CSV Export Walkthrough

I have successfully exported tracks from 4 Tidal playlists, matching "Yesterday" (2025-12-19) or "This Week".

## Process
1.  **Playlists Scanned**:
    - `https://tidal.com/playlist/496b977b-dd14-4ce7-9cb3-bfbd3e950229` (New West Coast)
    - `https://tidal.com/playlist/117dd55c-2c0b-453f-87c7-8b453286e92d` (New South)
    - `https://tidal.com/playlist/6896171c-2b4a-47bf-b044-ae3886a521d7` (New Midwest - No matches)
    - `https://tidal.com/playlist/7da79d8b-32d5-4d0e-be93-5021761805c4` (New East Coast)
2.  **Filter Applied**: "Date Added" contains "Yesterday" OR "This Week".
3.  **Result**: 18 Tracks Found.

## Verification
- **CSV Content (Expanded with Source Page)**:
```csv
Title,Artist,Album,Source Page
The Smooth Kind,Larry June,The Smooth Kind,New West Coast
Cavier x Cartier,"The Game, DJ Drama, Mike & Keys",Gangsta Grillz: Every Movie Needs A Trailer,New West Coast
Disappear (feat. Cypress Moreno & Zoe Osama),"MoneySign Suede, Cypress Moreno, zoe osama",Parkside Santa 2,New West Coast
Red Rose White Ceiling_BLUE,"REASON, Jayson Cash",Everything In My Soul_BLUE (Extended),New West Coast
Hayward Nights,ALLBLACK,Hayward Nights,New West Coast
Watch It Burn,PayGotti,Watch It Burn,New West Coast
REAL NIGGA DIARY. FT. JEEZY.,"YFN Lucci, Jeezy",ALREADY LEGEND. (GIFTED Edition),New South
Top Cobain,YoungBoy Never Broke Again,Top Cobain,New South
Out Ya Business,DaBaby,Out Ya Business,New South
My Life,Hurricane Wisdom,My Life,New South
Ro Come Bacc,Z-RO,Unappreciated,New South
Bad Terms,YTB FATT,Bad Terms,New South
Him Not Them,Lil Migo,Him Not Them,New South
Ain't Never Slowing Down,"Kevangotbandz, BigXthaPlug",Ain't Never Slowing Down,New South
Kill Confirmed,Wee2Hard,Flight Risk,New South
IIGHT IIGHT,Benny The Butcher,EL CARNICERO,New East Coast
The Dog,A$AP Twelvyy,The Dog,New East Coast
I'm A Problem,"Don Q, Goldie",From Dust To Don,New East Coast
```
- **Finder**: Validated file existence and revealed in Finder.

![Scraping Recording](/Users/adriangrant/.gemini/antigravity/brain/1b240ad9-fa83-47e5-90a7-525343d3b9af/scrape_multi_tidal_playlists_1766288588970.webp)
