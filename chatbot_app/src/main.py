from flask import Flask, url_for, request, redirect
from flask import render_template
import json
import pandas as pd
from .chatbot import Chatbot
from chatbot_app import app
import os
import re

# construct our bot instance
faq_path = os.path.join(os.getcwd(), 'chatbot_app/data/faq.csv')
bot = Chatbot(faq_path, stem = True)
bot.extend_stop_words(['plus', 'tres', 'etc'])
bot.create_corpus()

# get the corpus as a DataFrame
df = pd.read_csv(faq_path, encoding="utf-8")

questions_topics_path = os.path.join(os.getcwd(), 'chatbot_app/data/questions_by_topics.json')

# get questions grouped by topics for the topics buttons
with open(questions_topics_path, 'r') as outfile:
    questions_by_topics = json.load(outfile)

@app.route("/")
def index(title="Chatbot - Simplon"):
    if bot.answer is None :
        bot.question = bot.responses["bjr"]

    # get responses as preview and full response - useful when we only want to show partial responses
    pattern = re.compile(r".+?\.\W")
    responses = []

    for resp in df.responses.values :
        result = pattern.match(resp)
        preview = result.group()
        responses.append((preview, resp))

    return render_template('index.html', title=title, 
                                        bot=bot, 
                                        history=bot.history, 
                                        topics=questions_by_topics, 
                                        data=df.questions.values, 
                                        responses=responses)


@app.route('/question', methods=['POST'])
def question():
    # try to get from use input if he wants to leave or if he is satisfied with the bot response
    question_lower = request.form['question'].lower()
    pattern_oui = re.compile(r"(oui)|(satisfait)")
    pattern_bye = re.compile(r"(bye)|(ciao)|(au revoir)|(salut)")
    pattern_non = re.compile(r"(non)|(pas\s*\w*satisfaite?)")
    result_oui = pattern_oui.search(question_lower)
    result_bye = pattern_bye.search(question_lower)
    result_non = pattern_non.search(question_lower)

    # history with no answer if the user satisfied and wants to leave the service
    if result_oui or result_bye or result_non:
        bot.history.append({
            "question_bot" : bot.question,
            "question" : request.form['question'], 
            "preview" : None, 
            "answer" : None})

    if result_oui and not result_bye and not result_non: # the bot answered the user question
        bot.enableForm = True
        bot.question = bot.responses["response_pos"]
        return redirect(url_for('index'))

    if result_non and not result_bye: # the user isn't satisfied with answer
        bot.enableForm = True
        bot.question = bot.responses["response_neg"]
        return redirect(url_for('index'))

    if result_bye: # the user wants to leave the app
        bot.enableForm = False
        bot.question = bot.responses["bye"]
        bot.active = False
        return redirect(url_for('index'))

    # get preview answer and full answer
    bot.get_answer(request.form['question'])
    pattern_preview = re.compile(r".+?\.\W")
    result = pattern_preview.search(bot.answer)
    preview = result.group(0)
    bot.history.append({
            "question_bot" : bot.question,
            "question" : request.form['question'], 
            "preview" : preview, 
            "answer" : bot.answer})
    bot.enableForm = True
    bot.question = bot.responses["suite_question"]
    return redirect(url_for('index'))