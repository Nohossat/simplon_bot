# A Simplon chatbot

[![travis_build_status](https://travis-ci.com/Nohossat/simplon_bot.svg?branch=master)](https://travis-ci.com/github/Nohossat/simplon_bot)

We use the Simplon Anti-FAQ to build this chatbot. 

Cosine similarity and LDA techniques were used to get the most relevant results.

## Installation

```
git clone https://github.com/Nohossat/simplon_bot.git
cd simplon_bot
python -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=chatbot_app
export FLASK_ENV=development
flask run // this will launch the application in http://127.0.0.1:5000/

```