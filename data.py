from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

engine = create_engine('sqlite:///words.sqlite')

Base = automap_base()

Base.prepare(autoload_with=engine)

Word = Base.classes.word

Document = Base.classes.document

def get_data():
    data = {}
    with Session(engine) as session:
        data['words'] = [{'word': word.word, 'total_count': word.total_count} for word in session.query(Word).all()]
        data['total_words_count'] = sum(word.total_count for word in session.query(Word).all())
        data['total_letter_count'] = sum(word.letter_count*word.total_count for word in session.query(Word).all())
        data['total_vowel_count'] = sum(word.vowel_count*word.total_count for word in session.query(Word).all())
        data['unique_words_count'] = len([word for word in session.query(Word).all()])
        data['documents'] = [{'name': document.name, 'paragraphs_count': document.paragraphs_count, 'unique_word_count': document.unique_word_count, 'total_word_count': document.total_word_count, 'latitude': document.latitude, 'longitude': document.longitude, 'scrape_time': document.scrape_time, 'scrape_count': document.scrape_count} for document in session.query(Document).all()]
        data['documents_with_location'] = [{'name': document.name, 'paragraphs_count': document.paragraphs_count, 'unique_word_count': document.unique_word_count, 'total_word_count': document.total_word_count, 'latitude': document.latitude, 'longitude': document.longitude, 'scrape_time': document.scrape_time, 'scrape_count': document.scrape_count} for document in session.query(Document).filter(Document.latitude != None).all()]
        data['documents_count'] = len([document for document in session.query(Document).all()])
        data['total_scrape_time'] = sum(document.scrape_time for document in session.query(Document).all())
    return data