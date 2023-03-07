import urllib.request as request
from bs4 import BeautifulSoup as bs
import json

endpoint = "https://leagueoflegends.fandom.com/wiki/{}/LoL/Audio"
champs = "processed/champs.jsonl"

def process_champs_jsonl():
    champ_records = []
    with open(champs, "r") as champs_jsonl:
        for jsonl_entry in champs_jsonl:
            champ_records.append(json.loads(jsonl_entry))

    return champ_records

def scrape_champ_html(champ_name):
    return request.urlopen(endpoint.format(champ_name)).read().decode("utf-8")

def parse_champ_quotes(html):
    soup = bs(html, "html.parser")
    quotes = soup.findAll("i", data=True)
    print(quotes)

parse_champ_quotes(scrape_champ_html(process_champs_jsonl()[0]["name"]))
