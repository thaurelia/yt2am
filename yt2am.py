import json
import re
import webbrowser
from itertools import takewhile
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

ARTIST_TITLE_PAT = re.compile(r"(?P<artist>.*) [-–—] (?P<title>.*)")
ARTIST_PATS = [
    re.compile(r"(?P<artist>.*)" + tail)
    for tail in (r",.*", r"\sft.*", r"\sfeat.*", r"\sx\s.*", r"\s&.*")
]
TITLE_PATS = [
    re.compile(r"(.*) " + tail)
    for tail in (r"\(?ft.*", r"\(?feat.*", r"\| .*", r"\(.*\)")
]
REMIX_PAT = re.compile(r"(.*) \((?P<remix>.*) remix\)")


def get_video_names(link: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    for tg in soup.find_all("h3", class_="yt-lockup-title"):
        yield tg.findChild("a").get("title")


def split_artist_title(name):
    m = re.match(ARTIST_TITLE_PAT, name)
    return m.group("artist"), m.group("title")


def cleanup_artist(text):
    text = text.lower()
    matches = [re.match(p, text) for p in ARTIST_PATS]
    if not any(matches):
        n = text
    else:
        m = next(filter(None, matches))
        n = m.group("artist")

    return n


def cleanup_title(text):
    text = text.lower()
    m = re.match(REMIX_PAT, text)
    if m is not None:
        remix = m.group("remix")
        text = re.sub(REMIX_PAT, r"\1", text)
    else:
        remix = ""

    for p in TITLE_PATS:
        text = re.sub(p, r"\1", text)

    return f"{text} {remix}".strip()


def title_to_search_terms(video_title):
    a, t = split_artist_title(video_title)
    clean_a = cleanup_artist(a)
    clean_t = cleanup_title(t)
    return f"{clean_a} {clean_t}"


def main():
    with open("channels.txt") as f:
        channels = f.read().splitlines()
    try:
        with open("latest.json") as f:
            latest = json.load(f)
    except FileNotFoundError:
        latest = {ch: "" for ch in channels}

    to_add = set()
    for ch in channels:
        link = f"https://www.youtube.com/user/{ch}/videos"
        video_names = list(
            takewhile(lambda x: x != latest.get(ch), get_video_names(link))
        )
        if video_names:
            latest[ch] = video_names[0]
        to_add.update((title_to_search_terms(t) for t in video_names))

    with open("latest.json", "w") as f:
        json.dump(latest, f)

    songs = quote(";".join(to_add))
    url = f"shortcuts://run-shortcut?name=AMbatch&input={songs}"
    webbrowser.open(url)


if __name__ == "__main__":
    main()
