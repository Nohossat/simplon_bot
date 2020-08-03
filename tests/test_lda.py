import pytest
from chatbot_app.src.lda import *
import os
import types
import spacy

FILE_ABSOLUTE_PATH = os.path.abspath(__file__)  # get absolute filepath
CURRENT_DIR = os.path.dirname(FILE_ABSOLUTE_PATH)  # get directory path of file
PARENT_DIR = os.path.dirname(CURRENT_DIR)

def test_corpus_gen():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    df = pd.read_csv(faq_file, encoding="utf-8")
    corp_gen = corpus_gen(df.full_text.values.tolist())
    assert isinstance(corp_gen, types.GeneratorType), "it should be a generator"

def test_clean_doc():
    # get dataset
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    df = pd.read_csv(faq_file, encoding="utf-8")
    corpus = corpus_gen(df.full_text.values.tolist())

    # convert to spacy doc objects
    nlp = spacy.load("fr_core_news_sm")

    # tokenize
    docs = nlp.pipe(corpus)
    tokens = clean_doc(next(docs))
    
    real_tokens = ['Simplon.co', 'premier', 'seul', 'formation', 'genre', 'bien', 'qu’', 'distingue', 'format', 'intensif', 'vraiment', 'gratuit', 'voir', 'gratuité', 'tourné', 'vers', 'public', 'éloigné', 'emploi', 'sous-représenté', 'numérique', 'implanter', 'territoire', 'fragiliser', 'nature', 'développement', 'croissance', 'internationalisation', 'Simplon', 'premier', 'formation', 'type', 'seul', 'plusieurs', 'formation', 'exister', 'déjà', 'France', 'apparition', 'Simplon.co', '2013', 'web@cadémie', '3WAcadémie', 'Cefim', 'bien', 'territoire', 'créer', 'près', 'temps', 'presque', 'Simplon.co', 'Wagon', 'école', 'Webforce3', 'enfin', 'troisième', 'catégorie', 'celui', 'formation', 'créer', 'contact', 'Simplon', 'copycat', 'fork', 'franchiser', 'autonomiser', 'Wild', 'Code', 'School', 'auparavant', 'Simplon', 'Village', 'perche', 'Pop', 'School', 'Access', 'Code', 'School', 'Pôle', 'enfin', 'dernier', 'catégorie', 'formation', 'monter', 'sillage', 'dispositif', 'Grande', 'école', 'numérique', 'intéresser', 'certains', 'innover', 'réellement', 'gratuit', 'Simplon', 'ensembl', 'former', 'véritable', 'filière', 'riche', 'complémentaire', 'fournir', 'solution', 'différent', 'parfois', 'articuler', 'fonction', 'durée', 'entre', 'mois', 'métier', 'viser', 'développeur', 'data', 'analyst', 'technicien', 'etc.', 'technologie', 'PHP', 'ruby', 'Java', 'pédagogie', 'descendant', 'actif', 'formateur', 'physique', 'présentiell', 'distancielle', 'viser', 'public', 'concentrer', 'grand', 'agglomération', 'viser', 'territoire', 'fragile', 'oui', 'Simplon.co', 'unique', 'genre', 'véritablement', 'ouvrir', 'distinction', 'âge', 'niveau', 'scolaire', 'origine', 'territorial', 'réellement', 'intégralement', 'gratuite', 'également', 'seul', 'intégrer', 'origine', 'préoccupation', 'central', 'concerner', 'représentation', 'effectif', 'féminin', 'métier', 'féminiser', 'mode', 'également', 'assez', 'rare', 'qu’', 'dispute', 'Simplon', 'place', 'territoire', 'complexe', 'lien', 'géographie', 'prioritaire', 'ruralité', 'Outre-mer', 'international', 'certains', 'pilier', 'pédagogique', 'learning', 'teaching', 'également', 'caractéristique', 'original']
    assert tokens == real_tokens, "the tokens aren't correct"

def test_get_bigrams():
    # get dataset
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    df = pd.read_csv(faq_file, encoding="utf-8")
    corpus = corpus_gen(df.full_text.values.tolist())

    # convert to spacy doc objects
    nlp = spacy.load("fr_core_news_sm")

    # tokenize
    docs = nlp.pipe(corpus)
    bigrams = get_bigrams(docs)
    
    assert len(next(bigrams)) == 186, "the bigrams list length isn't correct"

def test_get_bow_matrix():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    bow_matrix = get_bow_matrix(faq_file)

    assert len(bow_matrix) == 26, "the bow matrix shape isn't correct"

def test_get_questions_by_topic():
    output_topics_file = os.path.join(CURRENT_DIR, 'data/questions_by_topics.json')
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    model_file = os.path.join(PARENT_DIR, 'chatbot_app/models/lda_model')
    get_questions_by_topic(faq_file, model_file, output_topics_file)

    assert os.path.exists(output_topics_file), "the output with the topics hasn't been created or doesn't exist"