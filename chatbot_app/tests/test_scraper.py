import pytest
from chatbot_flask.src.faq import scraper
import pandas as pd

def test_scraper():
    result_scrap = scraper("data/faq.csv")
    assert isinstance(result_scrap, pd.core.frame.DataFrame), f"An error occured {result_scrap}"