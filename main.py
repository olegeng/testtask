# Imports
import requests, gspread, re, os
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from bs4 import BeautifulSoup
load_dotenv()

class UserDataScraper():
    '''
    Class for ETL process
    '''

    def __init__(self):
        self.root = os.getenv('SCRAPPING_URL')
        self.page = requests.get(self.root)
        self.soup = BeautifulSoup(self.page.text, 'lxml')
        self.spreadsheet_url = os.getenv('SPREADSHEET_URL')
        self.scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        self.my_creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('CRED_PATH'), self.scope)
        self.gc = gspread.authorize(self.my_creds)

#Define lists for making a dataframe in the future.
    def extract(self):
        #Method for extracting data
        #Define all lists required for a create a data structure in the future
        names, roles, img_links, linkedin, twt, undefined_soc, site = [], [], [], [], [], [], []
        #next: scraping
        people_boxes = self.soup.find_all('div', class_ = 'speakers-list_item-wrapper')
        for person in people_boxes:
            names.append(person.find('h3', 'speakers-list_item-heading').get_text())
            roles.append(person.find('div', 'margin-bottom margin-small').find_all('div')[1].get_text())
            img_links.append(f"{self.root}{person.find('img')['src'][3:]}")
            socnetworks_links = person.find_all('a', class_=re.compile(r'speakers-list_social-link'))
            linkedin.append(socnetworks_links[0].get('href'))
            twt.append(socnetworks_links[1].get('href'))
            undefined_soc.append(socnetworks_links[2].get('href'))
            site.append(socnetworks_links[3].get('href'))


        return {
            'name': names,
            'role': roles,
            'img_link': img_links,
            'linkedin': linkedin,
            'twitter': twt,
            'NameLess_SN': undefined_soc,
            'Site': site
        }

    def transform(self, source=None):
        #Method for transforming data to required state
        if not source:
            source = self.extract()
        df = pd.DataFrame(source)
        replace_dict = {'index.html#': pd.NA, 'another_value': pd.NA, 'yet_another_value': pd.NA}
        df.replace(replace_dict, inplace=True)
        return df

    def load(self, dataframe=None):
        #Method for loading our data into spreadsheet and transforming into csv/json
        if not dataframe:
            dataframe = self.transform()
        dataframe.to_csv('contributors.csv')
        dataframe.to_json('contributors.json')
        spreadsheet = self.gc.open_by_url(self.spreadsheet_url)
        sheet = spreadsheet.sheet1
        set_with_dataframe(sheet, dataframe)


test = UserDataScraper()
test.load()