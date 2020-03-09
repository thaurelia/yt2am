import json
import re
import webbrowser
from itertools import takewhile
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

EMOJIS = re.compile(
    '['
    '\U0001F600-\U0001F64F'
    '\U0001F300-\U0001F5FF'
    '\U0001F680-\U0001F6FF'
    '\U0001F1E0-\U0001F1FF'
    '\U0001F1F2-\U0001F1F4'
    '\U0001F1E6-\U0001F1FF'
    '\U0001F600-\U0001F64F'
    '\U00002702-\U000027B0'
    '\U000024C2-\U0001F251'
    '\U0001f926-\U0001f937'
    '\U0001F1F2'
    '\U0001F1F4'
    '\U0001F620'
    '\u200d'
    '\u2640-\u2642'
    ']+',
    flags=re.UNICODE,
)

ARTIST_TITLE_PAT = re.compile(r'(?P<artist>.*) [-–—] (?P<title>.*)')
ARTIST_PATS = [
    re.compile(r'^(?P<artist>.*)' + tail)
    for tail in (
        r',.*',
        r'\sft.*',
        r'\sfeat.*',
        r'\sx\s.*',
        r'\s&.*',
        r'\s\(f.*',
    )
]
TITLE_PATS = [
    re.compile(r'(.*) ' + tail)
    for tail in (r'\(?ft.*', r'\(?feat.*', r'\| .*', r'\(.*\)', r'\[.*\]')
]
REMIX_PATS = [
    re.compile(r'(.*) ' + tail)
    for tail in (r'\[(?P<remix>.*) remix\]', r'\((?P<remix>.*) remix\)')
]


def get_video_names(link: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    for tg in soup.find_all('h3', class_='yt-lockup-title'):
        yield tg.findChild('a').get('title')


def split_artist_title(name):
    m = re.match(ARTIST_TITLE_PAT, name)
    if m is None:
        return None, None
    return m.group('artist'), m.group('title')


def cleanup_artist(text):
    text = text.lower()
    matches = [re.match(p, text) for p in ARTIST_PATS]
    if not any(matches):
        n = text
    else:
        m = next(filter(None, matches))
        n = m.group('artist')
    if ' x ' in n:
        return cleanup_artist(n)
    return n


def cleanup_title(text):
    text = text.lower()
    remixes = {
        p: re.match(p, text)
        for p in REMIX_PATS
        if re.match(p, text) is not None
    }
    if remixes:
        pat, m = remixes.popitem()
        remix = m.group('remix')
        text = re.sub(pat, r'\1', text)
    else:
        remix = ''

    for p in TITLE_PATS:
        text = re.sub(p, r'\1', text)

    return f'{text} {remix}'.strip()


def title_to_search_terms(video_title):
    a, t = split_artist_title(video_title)
    if not all((a, t)):
        return None
    clean_a = cleanup_artist(a)
    clean_t = cleanup_title(t)
    return f'{clean_a} {clean_t}'


def main():
    with open('sources.json') as f:
        sources = json.load(f)

    # Construct links for each source
    links = {
        name: f'https://www.youtube.com/{stype}/{id_}/videos'
        for stype, sdict in sources.items()
        for name, id_ in sdict.items()
    }

    try:
        with open('latest.json') as f:
            latest = json.load(f)
    except FileNotFoundError:
        latest = {name: '' for name in links}

    to_add = set()
    for name, link in links.items():
        video_names = list(
            takewhile(lambda x: x != latest.get(name), get_video_names(link))
        )
        if video_names:
            latest[name] = video_names[0]
        to_add.update((title_to_search_terms(t) for t in video_names))

    with open('latest.json', 'w') as f:
        json.dump(latest, f)

    to_add = (EMOJIS.sub(r'', item).strip() for item in filter(None, to_add))
    songs = quote(';'.join(to_add))
    url = f'shortcuts://run-shortcut?name=AMbatch&input={songs}'
    webbrowser.open(url)


if __name__ == '__main__':
    main()
