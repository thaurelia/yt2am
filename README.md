# yt2am

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

**iOS only** script-shortcut combo to monitor music channels and create AM playlists.

`requests` and `bs4` packages are provided by the Pythonista app (so no `requirements.txt`).

## Usage

- Create AMbatch shortcut (see below; not shared here because reasons)
- Modify `sources.json` to include your channels
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

## AMBatch shortcut

- Text - Split `Shortcut Input` by `Custom` - `;`
- Scripting - Repeat with each item in `Split text`
    - iTunes Store - Search iTunes Store for `Repeat Item`
        - Category: *Music*
        - Search By: *All*
        - Results: *Songs*
        - Region: *%your region%*
        - *1 Item* (this is important)
    - Music - Add `iTunes Products` to *%your playlist%*
- End Repeat
