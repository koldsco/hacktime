import requests
from stop_words import StopWords

ES_CONFIG = {
    'index': 'apm',
    'type': 'test-03',
    'path': 'https://search-escloud-ir7f3gyru66ibel5pnp3bdjzoi.us-west-2.es.amazonaws.com/'
}

def save_to_ES(s3, text):
    filter_stop_words = StopWords('stop_words.json')
    body = {
        "file": s3,
        "transcript": text,
        "text": filter_stop_words.exclude_stopwords(text)
    }
    url = '{path}{index}/{type}/{s3}'.format(s3=s3, **ES_CONFIG)
    r = requests.put(url, json=body)
    if r.status_code == 200:
        return True
    else:
        return False
