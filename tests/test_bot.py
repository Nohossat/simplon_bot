import pytest
import os

from chatbot_app.src.chatbot import Chatbot

FILE_ABSOLUTE_PATH = os.path.abspath(__file__)  # get absolute filepath
CURRENT_DIR = os.path.dirname(FILE_ABSOLUTE_PATH)  # get directory path of file
PARENT_DIR = os.path.dirname(CURRENT_DIR)


def test_read_faq_file():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    assert faq_file == "/Users/nohossat/Documents/simplon-vms/chatbot_flask/chatbot_app/src/static/data/faq.csv", "error while reading faq file"

def test_bot_init():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    bot = Chatbot(faq_file, stem = True)
    assert isinstance(bot, Chatbot), "The bot hasn't been well initialized"

def test_tokenize():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    bot = Chatbot(faq_file, stem = True)
    tokens = ["Bonjour", "il", "fait", "chaud"]
    assert bot.tokenize("Bonjour, il fait chaud") == tokens, "the tokenization didn't worked"

def test_extend_stop_words():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    bot = Chatbot(faq_file, stem = True)
    new_stop_words = ['plus', 'tres', 'etc']
    bot.extend_stop_words(new_stop_words)
    last_stop_words = bot.stop_words[len(bot.stop_words) - 3 :len(bot.stop_words)]
    assert last_stop_words == new_stop_words, "the new stop words weren't added"

def test_nettoyage():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    bot = Chatbot(faq_file, stem = True)
    document = "Bonjour, il fait chaud"
    cleaned_tokens = ["bonjour", "chaud"]
    assert bot.nettoyage("Bonjour, il fait chaud") == cleaned_tokens, "the document hasn't been cleaned correctly"

def test_create_corpus():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    bot = Chatbot(faq_file, stem = True)
    bot.create_corpus()
    assert len(bot.corpus) == 26, "the length of the corpus isn't correct"

def test_get_answer():
    faq_file = os.path.join(PARENT_DIR, 'chatbot_app/src/static/data/faq.csv')
    bot = Chatbot(faq_file, stem = True)
    bot.create_corpus()
    question = "Où se situe Simplon ?"
    bot.get_answer(question)
    answer = "On aurait envie de vous dire oui parce que le projet est effectivement né de multiples discussions qui ont eu lieu dans un appartement de la rue du Simplon dans le 18ème arrondissement de Paris, parce que le projet a même porté le nom de code “Silicon Simplon” en forme de pied de nez à l’omniprésence du 2ème arrondissement et de son “Silicon Sentier” sur la scène digitale francilienne, mais non… le siège social de Simplon, son centre de formation des formateurs des Fabriques Simplon sur les territoires et un de ses lieux d’activités principales est à Montreuil au métro Croix de Chavaux, en Seine-Saint-Denis ;-) On pourrait également vous dire que Simplon ça vient d’un col dans les Alpes où existe un monastère, que Napoléon y aurait gagné la bataille d’Italie, que depuis longtemps l’Orient Express y passe et que c’est pour cela qu’on l’appelle le Simplon Orient Express… Mais depuis novembre 2017 Simplon est désormais officiellement présent, grâce à la Ville de Paris, dans le 18ème arrondissement à la Halle Pajole. Et chose qui n'est&nbsp;due qu'au hasard, le président cofondateur de Simplon vit rue du Simplon ;-)"
    assert bot.answer == answer, "the answer isn't correct"
