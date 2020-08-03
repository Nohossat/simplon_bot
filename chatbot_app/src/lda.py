import pandas as pd
from stop_words import get_stop_words
import string
import json

# models
import gensim
from gensim import corpora
from gensim import models
from nltk.util import ngrams
import spacy


def corpus_gen(data):
        for row in data:
            yield row

def clean_doc(doc):
    stop_words = get_stop_words('french').copy() 
    stop_words.extend(['plus', 'tres', 'etc'])
    list_tokens = []
    for token in doc:
        if token.pos_ not in ["PUNCT"] and len(token.lemma_) > 2 and token.lemma_ not in stop_words:
            list_tokens.append(token.lemma_)
    return list_tokens

def get_bigrams(docs):
    for doc in docs:
        bigrams = ngrams(clean_doc(doc), 2)
        bigrams_list = [' '.join(bigram) for bigram in bigrams]
        yield bigrams_list

def get_bow_matrix():
    df = pd.read_csv("../data/faq.csv", encoding="utf-8")

    # generate bigrams
    corpus = corpus_gen(df.full_text.values.tolist())
    nlp = spacy.load("fr_core_news_sm")
    docs = nlp.pipe(corpus)
    bigram_gen = get_bigrams(docs)

    # generate word _ id dict
    id2word = corpora.Dictionary(bigram_gen)

    # generate bow matrix
    corpus = corpus_gen(df.full_text.values.tolist())
    docs = nlp.pipe(corpus)
    bigrams = get_bigrams(docs)
    matrix_bow = [id2word.doc2bow(bigram) for bigram in bigrams]
    return matrix_bow

def get_questions_by_topic():
    matrix_bow = get_bow_matrix()
    lda_model = models.ldamodel.LdaModel.load("../models/lda_model")
    topics = ["économie sociale et solidaire", "projets Simplon", "école numérique", "reconversion professionnelle"] # induced by the model
    questions_by_topics = {}

    for i, bow in enumerate(matrix_bow):
        topic_idx, proba = lda_model.get_document_topics(bow)[0]
        
        if topics[topic_idx] not in questions_by_topics.keys():
            questions_by_topics[topics[topic_idx]] = {}
            questions_by_topics[topics[topic_idx]]['keywords'] = [word for word, prop in lda_model.show_topic(topic_idx)]
            questions_by_topics[topics[topic_idx]]['questions'] = []
        questions_by_topics[topics[topic_idx]]['questions'].append(i)
        
    # save to json for future use   
    with open("../data/questions_by_topics.json", 'w') as outfile:
        json.dump(questions_by_topics, outfile)

if __name__ == "__main__":
    get_questions_by_topic()