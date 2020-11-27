import codecs
import re
import requests
import json
from bs4 import BeautifulSoup
from collections import OrderedDict
import sys

BASE_URL = "http://dreambank.net/random_sample.cgi"
DREAMBANK = "%s?series={0}&min=1&max=100000&n=" % BASE_URL # n= loads all dreams in series

NUMBER_RE = r'^\#\(?(\S+)\)?'

HEAD_RE = r'^\((.+?)\)(\w)'

def process_dream_span(span):
    text = span.text.strip()
    # remove number
    number_groups = re.match(NUMBER_RE, text)
    if number_groups == None:
        raise Exception("ParseException")

    number = number_groups.group(1).strip()

    text = re.sub(NUMBER_RE, '', text).strip()

    # remove word count
    text = re.sub(r'\s*\(\d+\s+words\)\s*$', '', text, re.I)

    # Split nb-space as paragraphs
    text = re.sub('\\s*?(\xc2\xa0)+\\s*', '\n', text).strip()

    # sep desc
    head_match = re.match(HEAD_RE, text)
    if head_match is None:
        return OrderedDict([
            ('number', number),
            ('content', text)])

    head = head_match.group(1).strip()
    text = re.sub(HEAD_RE, lambda x: x.group(2), text).strip()

    return OrderedDict([
        ('number', number),
        ('head', head),
        ('content', text)])

def process_dream_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    dreams = soup.find_all('span')
    for dream in dreams:
        try:
            data = process_dream_span(dream)
            if data is not None:
                yield data
        except:
            print("Error: Could not process dream %s" % str(dream))
            continue

def download_dreams(dreamer):
    url = DREAMBANK.format(dreamer)
    r = requests.get(url)
    if r.status_code != 200:
        print("error getting dreams")
        return None
    return r.text

def collect_dreams(dreamer, desc):
    text = download_dreams(dreamer)
    return OrderedDict([
        ('dreamer', dreamer),
        ('description', desc),
        ('dreams', list(process_dream_page(text)))])

def load_dreamers():
    r = requests.get(BASE_URL)
    if r.status_code != 200:
        print("error getting dreamers")
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    dreamers = soup.find('select', {"name":"series"})
    dreamers = dreamers.find_all('option')
    dreamers = map(lambda option: (option.get("value"), option.get_text()), dreamers)
    dreamers = filter(lambda dreamer: dreamer[0] != "" and dreamer[0] is not None, dreamers)
    return dict(dreamers)

if len(sys.argv) <= 1:
  DREAMERS=load_dreamers()
elif sys.argv[1] == "all":
  DREAMERS=load_dreamers()
else:
  DREAMERS=dict(map(lambda dreamer: (dreamer, "no-desc"), sys.argv[1].split(",")))

if DREAMERS is not None:
    for dreamer, desc in DREAMERS.items():
        print("collecting dreams for dreamer %s" % dreamer)
        dreams = collect_dreams(dreamer, desc)
        if dreams is not None:
            with codecs.open('dreams/' + dreamer + '.json', 'w', encoding='utf-8') as out_file:
                json.dump(dreams, out_file, sort_keys=False, indent=4, ensure_ascii=False)
