import pytest
from chatbot_app.src.faq import scraper
import pandas as pd
import os

FILE_REL_PATH = os.path.relpath(__file__)
CURRENT_DIR = os.path.dirname(FILE_REL_PATH)  # get directory path of file

def test_scraper():
    faq_file = os.path.join(CURRENT_DIR, 'data/faq.csv')
    result_scrap = scraper(faq_file)
    assert isinstance(result_scrap, pd.core.frame.DataFrame), f"An error occured {result_scrap}"