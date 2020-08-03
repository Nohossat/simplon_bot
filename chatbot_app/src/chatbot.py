from selenium import webdriver
import pandas as pd
import numpy as np
from stop_words import get_stop_words
import string
import unidecode
import re
import gensim
from gensim import corpora
from gensim import models
import gensim.downloader as api
from gensim.summarization import summarize, keywords
from nltk.stem.snowball import FrenchStemmer
from pprint import pprint
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class Chatbot():
    def __init__(self, filename = None, stem = False, closest_answers_flag = False):
        self.filename = filename

        try :
            self.data = pd.read_csv(self.filename, encoding="utf-8")
        except Exception as e:
            self.data = e

        self.corpus = None
        self.question = None
        self.answer = None
        self.stop_words = get_stop_words('french').copy()
        self.stem = stem
        self.closest_answers_flag = closest_answers_flag
        self.responses = {
            "bjr" : "Bonjour", 
            "question": "As-tu une question ?", 
            "bye" : "Au revoir"
        }
    
    @staticmethod
    def tokenize(document):
        """
        transform the corpus into a list of list of tokens
        """
        punct = string.punctuation + "…" + "`" + "’" # remove punctuation
        transformer = str.maketrans(punct, ' '*len(punct))
        document = document.translate(transformer)

        pattern = re.compile(r"\n") # remove linebreak
        document = pattern.sub(" ", document)

        document = unidecode.unidecode(document) # remove accents
        
        document = document.split(' ') # split sentence into tokens
        new_document = []
        
        for word in document:
            if word :
                new_document.append(word)
            
        return new_document

    def extend_stop_words(self, words):
        self.stop_words.extend(words)

    def clean_comment(self, document):
        """
        remove stop words, numbers and small words form the corpus
        """
        return [word.lower() for word in document if len(word) > 2 and not word.isnumeric() and word not in self.stop_words]

    def nettoyage(self, document):
        """
        function to clean the dataset + stemming
        """
        document = self.clean_comment(self.tokenize(document))
        
        if self.stem:
            stem = FrenchStemmer()
            document = [stem.stem(word) for word in document]
        return document

    def get_answer(self, question):
        """
        vectorize user input than output closest answer
        """
        # we clean the user input & add it to our corpus (last index)
        user_corpus = self.nettoyage(question)
        self.corpus.append(' '.join(user_corpus))
        
        # transform our corpus into a BOW matrix
        vectorizer = TfidfVectorizer()
        user_corpus_vect = vectorizer.fit_transform(self.corpus)
        
        # prefer array to get the similarity
        user_corpus_array = user_corpus_vect.toarray()
        
        # cosine similiarity between the user input and all the topics
        corpus_vect = user_corpus_array[:-1]
        user_input_vect = user_corpus_array[-1].reshape(1, -1)
        cosine_simil_scores = np.array(cosine_similarity(corpus_vect, user_input_vect))
        
        if self.closest_answers_flag:
            index_answer = np.argsort(np.hstack(cosine_simil_scores))[::-1][:3]
            self.answer = self.data.iloc[index_answer, 1] # related questions
            return

        index_answer = np.argmax(cosine_simil_scores)
        self.answer = self.data.iloc[index_answer, 1]

    def create_corpus(self):
        corpus_df = self.data.full_text.apply(self.nettoyage)
        self.corpus = [" ".join(text_list) for text_list in corpus_df]


if __name__ == "__main__":
    # init chatbot
    
    bot = Chatbot('../data/faq.csv', stem = True)
    bot.extend_stop_words(['plus', 'tres', 'etc'])
    bot.create_corpus()

    while True:
        bot.question = input("BOT : Salut, as-tu une question à me poser ? (Taper q pour quitter)")
        print(f"USER : {bot.question}")
        if bot.question == 'q':
            break
        
        bot.get_answer()
        print("=========")
        print(bot.answer)