import urllib.request as request
from bs4 import BeautifulSoup as bs
import json
import time

endpoint = "https://leagueoflegends.fandom.com/wiki/{}/LoL/Audio"
champs = "processed/champs.jsonl"
champ_quotes_file = open("processed/champ_quotes.jsonl", "w")
error_log = open("raw/parse_errors.txt", "w")


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
    quotes = soup.findAll("i")
    return filter(lambda quote: "\"" in quote, map(lambda soup_quote: soup_quote.text, quotes))

def write_champ_quotes(champ_id, champ_name):
    champ_name = champ_name if len(champ_name.split(" ")) == 1 else "_".join(champ_name.split(" "))
    parsed_quotes = parse_champ_quotes(scrape_champ_html(champ_name))
    for qid, quote in enumerate(parsed_quotes):
        champ_quotes_file.write(json.dumps({"id": qid, "champ_id": champ_id, "quote": quote.lstrip("\"").rstrip("\"").rstrip("\n")}) + "\n")

def write_all_champ_quotes():
    champ_records = process_champs_jsonl()
    for champ in champ_records:
        print("Writing champion quote data for: {}".format(champ["name"]))
        start = time.time()
        try:
            write_champ_quotes(champ["id"], champ["name"])
            print("\tCOMPLETED - {}s".format(time.time() - start))
            time.sleep(2)
        except Exception as e:
            print("Could not get quotes for: " + champ["name"])
            print("Logged to raw/parse_errors.txt")
            error_log.write("Could not parse quotes for: " + champ["name"] + "\n")
    champ_quotes_file.close()
    error_log.close()
        

write_all_champ_quotes()
