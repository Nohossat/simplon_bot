from flask import Flask, url_for, request, redirect
from flask import render_template
from .src.chatbot import Chatbot
import json
import pandas as pd

app = Flask(__name__, static_url_path='', 
            static_folder='src/static',
            template_folder='src/templates')

from .src import main
