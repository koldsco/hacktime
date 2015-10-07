#! /usr/bin/env python

import requests
from stop_words import StopWords
import json
import sys,os

ES_CONFIG = {
    'index': 'apm',
    'type': 'test-03',
    'path': 'https://search-escloud-ir7f3gyru66ibel5pnp3bdjzoi.us-west-2.es.amazonaws.com/'
}

def save_to_ES(s3, text, category):
    filter_stop_words = StopWords('stop_words.json')
    body = {
        "file": s3,
        "transcript": text,
        "text": filter_stop_words.exclude_stopwords(text),
        "category": category
    }
    url = '{path}{index}/{type}/{s3}'.format(s3=s3, **ES_CONFIG)
    r = requests.put(url, json=body)
    if 200 <= r.status_code < 300:
        return True
    else:
        print url
        print r.reason
        print r.status_code
        return False

def read_json(file_name):
    tempfile = "/tmp/%s"%file_name
    os.system("aws s3 cp s3://teamname-files/%s %s"%(file_name,tempfile))
    with open(tempfile) as f:
        j = json.load(f)

    return j

if __name__ == "__main__":
    def main():
        json_name = sys.argv[1]
        json_obj = read_json(json_name)
        text, s3file, category, fulllink = json_obj["text"], json_obj["s3file"], json_obj["entities"],json_obj["fulladdr"]

        print save_to_ES(s3file, text, category)

    # MAIN
    main()
