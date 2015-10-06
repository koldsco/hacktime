#! /usr/bin/env python

import json
import re

class StopWords:
    """ StopWords: Parse text and exclude "common meaningless words"
        
        Usage: sw = StopWords(<json file with common stop words>)

        parsed_text = sw.exclude_stopwords(text)

        <stop word json>: {"stopWords": ["word1", "word2", ...]}
    """

    def __init__(self, stop_json):
        stop = self._read_json(stop_json)
        self.stop_words = [_.upper() for _ in stop["stopWords"]]

        self.word_regex = re.compile('\w+')

    def _read_json(self, file_name):
        with open(file_name) as f:
            j = json.load(f)

        return j

    def is_stopword(self, word):
        """ True if word is a "stop word", False otherwise
        """
        return word.upper() in self.stop_words

    def exclude_stopwords(self, text):
        """ Parse incoming text and exclude stopwords
        """

        def split_words(text):
            """ Split text into words """
            return self.word_regex.findall(text)

        out = []

        for word in split_words(text):
            if not self.is_stopword(word):
                out.append(word)

        return out
