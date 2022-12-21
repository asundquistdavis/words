from time import time
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from itertools import groupby
from re import sub
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import Session, declarative_base
executable_path = {'executable_path': ChromeDriverManager().install()}
Base = declarative_base()
engine = create_engine('sqlite:///words.sqlite')

ENTRY_URL = 'https://en.wikipedia.org/wiki/Special:Search?search=&go=Go'

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer(), primary_key=True)
    word = Column(String())
    total_count = Column(Integer())
    document_count = Column(Integer())
    letter_count = Column(Integer())
    vowel_count = Column(Integer())

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    paragraphs_count = Column(Integer())
    unique_word_count = Column(Integer())
    total_word_count = Column(Integer())
    latitude = Column(Float())
    longitude = Column(Float())
    url = Column(String())
    scrape_time = Column(Float())
    scrape_count = Column(Integer())

    def print_out(self):
        print(f'ID: {self.id},\nName: {self.name},\nParagraphs Count: {self.paragraphs_count},\nUnique Word Count: {self.unique_word_count},\nTotal Word Count: {self.total_word_count},\n{"Latidute: "+str(self.latitude)+", Longitude: "+str(self.longitude)+","}\nScrape Time: {self.scrape_time},\nScrape Count: {self.scrape_count}\n----------------------------------------------------------------')

Base.metadata.create_all(engine)

def count_vowels(word):
    vowels = 'aeiou'
    count = 0
    for letter in word:
        if letter in vowels:
            count += 1
    return count

def clean_and_split(text):
    text = text.lower()
    text = sub(r'[^\s]*[a-zA-Z]+[^a-zA-Z\s][a-zA-Z][^\s]*', '', text)
    text = sub(r'[^a-zA-Z\s]+', '', text)
    words = text.split()
    return sorted(words)

def get_word_or_none(session:Session, word:str)->Word:
    try:
        return session.query(Word).filter_by(word=word).first()
    except Exception as error:
        print(error)
        return None

def add_word(session:Session, word:str, term_count)->Word:
    letter_count = len(word)
    vowel_count = count_vowels(word)
    word = Word(word=word, total_count=term_count, document_count=1, letter_count=letter_count, vowel_count=vowel_count)
    session.add(word)
    session.commit()
    return word

def update_word(session:Session, target_word:Word, term_count:int)->Word:
    target_word.total_count = term_count + target_word.total_count
    target_word.document_count = target_word.document_count + 1
    session.commit()
    return target_word

def add_or_update_word(word:str, term_count:int):
    with Session(engine) as session:
        target_word = get_word_or_none(session, word)
        if target_word == None:
            return add_word(session, word, term_count)
        else:
            return update_word(session, target_word, term_count)

class Document_Summary():
    def __init__(self, name:str, paragraphs:list, latitude:float, longitude:float, url:str, start_time:float) -> None:
        self.name:str = name
        self.paragraphs:list[str] = paragraphs
        self.latitude = latitude
        self.longitude = longitude
        self.url = url
        self.start_time:float = start_time
        self.text:str = ''.join(self.paragraphs)
        self.end_time:float = time()
        self.get_word_lengths()

    def get_word_lengths(self):
        self.all_words = clean_and_split(self.text)
        self.total_word_count = len(self.all_words)
        self.words = []
        for word, group in groupby(self.all_words):
            self.words.append((word, len(list(group))))
        self.unique_word_count = len(list(self.words))

    def load_document(self):
        self.end_time = time()
        add_or_update_doc(self)

    def load_words(self):
        for (word, term_count) in self.words:
            add_or_update_word(word, term_count)

def get_doc_or_none(session:Session, document_summary:Document_Summary)->Document:
    try:
        return session.query(Document).filter_by(name=document_summary.name).first()
    except Exception as error:
        print(error)
        return None

def add_doc(session:Session, document_summary:Document_Summary, scrape_time:float):
    document = Document(name=document_summary.name, paragraphs_count=len(document_summary.paragraphs), unique_word_count=document_summary.unique_word_count, total_word_count=document_summary.total_word_count, latitude=document_summary.latitude, longitude=document_summary.longitude, url=document_summary.url, scrape_time=scrape_time, scrape_count=1)
    session.add(document)
    session.commit()

def update_doc(session:Session, target_document:Document, scrape_time:float):
    target_document.scrape_count += 1
    target_document.scrape_time = scrape_time
    session.commit()

def add_or_update_doc(document_summary:Document_Summary):
    with Session(engine) as session:
        target_document = get_doc_or_none(session, document_summary)
        if target_document == None:
            add_doc(session, document_summary, document_summary.end_time-document_summary.start_time)
        else:
            update_doc(session, target_document, document_summary.end_time-document_summary.start_time)

def get_random_page_html():
    with Browser('chrome', **executable_path, headless=False) as browser:
        browser.visit(ENTRY_URL)
        browser.links.find_by_partial_text('Random article').click()
        html = browser.html
        url = browser.url
    return html, url

def scrape_page_html(html:str, url:str, start_time:float):
    soup = BeautifulSoup(html, 'html5lib')
    name = soup.find('title').text.replace(' - Wikipedia', '')
    paragraphs = [p.text for p in soup.find('div', attrs={'id': 'bodyContent'}).find_all('p')]
    try:
        latitude = float(soup.find('span', attrs={'class': 'geo-dec'}).text.split()[0].strip('°NS'))
        longitude = float(soup.find('span', attrs={'class': 'geo-dec'}).text.split()[1].strip('°EW'))
    except:
        latitude = None
        longitude = None
    return Document_Summary(name, paragraphs, latitude, longitude, url, start_time)

def create_random_document():
    start_time = time()
    html, url = get_random_page_html()
    document_summary = scrape_page_html(html, url, start_time)
    document_summary.load_words()
    document_summary.load_document()

if __name__ == '__main__':
    create_random_document()
    with Session(engine) as s:
        s.query(Document).all()[-1].print_out()
        print(f'50th word\'s total count: {s.query(Word).all()[50].total_count}')
        print([(word.word, word.total_count) for word in s.query(Word).order_by(Word.total_count).all()])