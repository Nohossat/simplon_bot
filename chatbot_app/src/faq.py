from selenium import webdriver
import pandas as pd

def scraper(filename):
    try :
        browser = webdriver.Chrome()
        browser.get("https://simplon.co/anti-faq")
        data = {
            "questions" : [],
            "responses" : []
        }
        for topic in browser.find_elements_by_css_selector('.card.faq-box'):
            data['questions'].append(topic.find_element_by_css_selector('h5 .btn').text)
            data['responses'].append(topic.find_element_by_css_selector("[data-parent='#accordion'] p").get_attribute('innerHTML'))
            
        browser.quit()

        df_faq = pd.DataFrame(data)

        df_faq.loc[:, 'full_text'] = df_faq['questions'] + ' ' + df_faq['responses']
        df_faq.to_csv(filename, index=False)
        return df_faq.head()
    except Exception as e:
        return e

if __name__ == "__main__":
    result_scrap = scraper("../data/faq.csv")
    print(result_scrap)