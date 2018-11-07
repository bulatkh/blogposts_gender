import os
import re
import numpy as np
from mrjob.job import MRJob
from operator import itemgetter
from mrjob.step import MRStep

word_search_re = re.compile(r"[\w]+")


class NaiveBayesTrainer(MRJob):

    def steps(self):
        """
        first step: map gender with each words and then count probability of word in post
        second step: combine frequencies for each gender
        """
        return [
            MRStep(mapper=self.extract_words_mapping,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.compare_words_reducer)
        ]

    def extract_words_mapping(self, key, value):
        """
        :returns generator gender-word tuples and probability of 1 word
        """
        # split text by whitespaces
        tokens = value.split()
        # get the gender
        gender = eval(tokens[0])
        blog_post = eval(" ".join(tokens[1:]))
        all_words = word_search_re.findall(blog_post)
        all_words = [word.lower() for word in all_words]
        for word in all_words:
            yield (gender, word, len(all_words)), 1

    def reducer_count_words(self, key, flag):
        """
        :returns generator of word and gender-probability tuple
        """
        frequency = sum(flag)
        gender, word, num_words = key
        yield word, (gender, float(frequency / num_words))

    def compare_words_reducer(self, word, values):
        """
        :returns for each word its dictionary containing gender as a key and prob as a value
        """
        per_gender = {}
        for value in values:
            gender, probability = value
            per_gender[gender] = probability
        yield word, per_gender


if __name__ == '__main__':
    NaiveBayesTrainer.run()