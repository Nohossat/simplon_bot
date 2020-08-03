from flask import Flask, url_for, request, redirect
from flask import render_template
from chatbot_app.src.chatbot import Chatbot
import json
import pandas as pd

app = Flask(__name__, 
            static_url_path='', 
            static_folder='src/static',
            template_folder='src/templates')

import chatbot_app.src.views
