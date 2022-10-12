import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
import re

def get_content(urls):
    '''This function takes in a list of urls for the Codeup blog web pages and returns a dataframe of the title of the blog
        and the content.'''
    articles = [{}]
    for url in urls:
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.text.strip()
        p1 = soup.find_all('p')[1].text.strip()
        p2 = soup.find_all('p')[2].text.strip()
        p3 = soup.find_all('p')[3].text.strip()
        p4 = soup.find_all('p')[4].text.strip()
        content = p1 + p2 + p3 + p4
        articles.append({'title':title, 'content':content})
    return articles

def get_news_articles(url):
    '''This function takes in a url from an inshorts.com category and returns a list of articles, separated by title,
        author, date, and content.'''
    articles = []
    soup = BeautifulSoup(get(url).content, 'html.parser')
    article_list = soup.select('div.container')[0].text.split('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    del article_list[0]
    for article in article_list:
        article = article.replace('\n', '').replace('      ', '')
        article_re = r'(?P<title>.*)short by\s(?P<Author>\w+\s\w+)\s/\s(?P<date>.*2022)\,Wednesday(?P<content>.*)short'
        articles.append(re.findall(article_re, article))
        articles = [i for i in articles if i]
        #title, author, date, content = article_mashed
        #articles.append({'title':title, 'author':author, 'date':date, 'content':content})
    return articles

def news_dict(articles):
    '''This function takes in a list of articles from the get_news_articles function and returns a dictionary for each
        article.'''
    art_dict = [{}]
    columns = ['title','author','date','content']
    for article in articles:
    #dict(zip(columns, article[0]))
        art_dict.append(dict(zip(columns, article[0])))
    return art_dict

def news_df(news, category):
    '''This function takes in the dictionary from the news_dict function and the category to which the articles belong
    (string) and returns a dataframe of each article. A column is added for the article's category.'''
    news = pd.DataFrame(news).drop(0)
    news['category'] = category
    return news