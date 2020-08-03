from flask import Flask, url_for, request, redirect
from flask import render_template
import json
import pandas as pd
from .chatbot import Chatbot
from chatbot_app import app
import os


# construct our bot instance
faq_path = os.path.join(os.getcwd(), 'chatbot_app/data/faq.csv')
bot = Chatbot(faq_path, stem = True)
bot.extend_stop_words(['plus', 'tres', 'etc'])
bot.create_corpus()

# get the corpus as a DataFrame
history = []
df = pd.read_csv(faq_path, encoding="utf-8")

questions_topics_path = os.path.join(os.getcwd(), 'chatbot_app/data/questions_by_topics.json')
# get questions grouped by topics for the topics buttons
with open(questions_topics_path, 'r') as outfile:
    questions_by_topics = json.load(outfile)

@app.route("/")
def index(title=None):
    title = "Chatbot"
    bot.question = bot.responses["bjr"]
    return render_template('index.html', title=title, 
                                        bot=bot, 
                                        history=history, 
                                        topics=questions_by_topics, 
                                        data=df.questions.values, 
                                        responses=df.responses.values)

@app.route('/question', methods=['POST'])
def question():
    bot.get_answer(request.form['question'])
    history.append([request.form['question'], bot.answer])
    return redirect(url_for('index'))