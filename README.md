# yt2am

**iOS only** script-shortcut combo to monitor music channels and create AM playlists.

`requests` and `bs4` packages are provided by the Pythonista app (so no `requirements.txt`).

## Usage

- Create AMbatch shortcut (see below; not shared here because reasons)
- Modify `channels.txt` to include your channels
    - No obvious way to create shortcut with `Run script` in the middle and not cause infinite loops; `run--shortcut` (with double hyphen) method fails
    - Not OK with passing script results over the clipboard
    - Hence, passing channels from the external file
- Create yt2am.py shortcut on the home screen (or use directly from the Pythonista app)

Requires *Pythonista* (paid) and *Shortcuts* apps.

## “Features”

- Gets the latest 30 videos from each new channel
- Remembers each channel's last video name from the previous search and searches newer videos
- Tries to guess song remixes and searches accordingly
- Simplifies search by removing additional artists (from “feat.” etc) both from artist name and from song title
- “Pre-installed” channels (EDM):
    - [xKito](https://www.youtube.com/user/nyuualiaslucy/)
    - [Diversity](https://www.youtube.com/user/DiavelNN)
    - [Kyra](https://www.youtube.com/user/NNKyra)
    - [Trap City](https://www.youtube.com/user/OfficialTrapCity)
    - [Tribal Trap](https://www.youtube.com/user/TribalTrapMusic)

## AMBatch shortcut

- Get Text from Input
- Split Text
    - Separator: *Custom – “;”*
- Repeat with Each
    - Search iTunes Store
        - Search: *Repeat Item* (found in “Variables”)
        - Category: *Music*
        - Search By: *All*
        - Results: *Songs*
        - Region: *%your region%*
        - *1 Item* (this is important)
    - Add to Playlist
        - Playlist: *%your playlist%*
- End Repeat
