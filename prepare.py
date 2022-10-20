import pandas as pd
import numpy as np
import re
from requests import get
from bs4 import BeautifulSoup as soupify
import unicodedata
import nltk
from nltk.corpus import stopwords

def basic_clean(string):
    '''This function takes in a dataframe column and lowercases everything, normalizes unicode characters, and replaces
        anything that is not a letter, number, whits space, or single quote. It returns the cleaned column as a Series.'''
    # create an empty list to hold the cleaned strings
    cleaned = []
    # lowercase all characters
    string = string.str.lower()
    # loop through each string in the column
    for item in string:
        # encode and decode the string into ascii
        item = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore').decode('utf-8')
        # remove anything that is not a letter, number, slash, or space
        item = re.sub(r'[^0-9a-z/\'\s]', '', item)
        # add the cleaned string to the list
        cleaned.append(item)
    # return the list of strings
    return cleaned

def get_blog_urls(base_url, header={'User-Agent': 'Codeup Data Science'}):
    '''This function takes in a url and returns list of Codeup blog urls.'''
    # initiate BeautifulSoup
    soup = soupify(get(url, headers=header).content)
    # return the soupified links
    return [link['href'] for link in soup.select('a.more-link')]

def get_blog_content(base_url):
    '''This function takes in the base url for Codeup blog posts and returns the blog contents as a list of strings.'''
    # acquire the urls for each blog using the get_blog_urls function
    blog_links = get_blog_urls(base_url)
    # create an empty list for the blog contents
    all_blogs = []
    # loop through each blog and soupify the text
    for blog in blog_links:
        blog_soup = soupify(get(blog,headers=header).content)
    # location of the text in the html code
        blog_content = {'title': blog_soup.select_one('h1.entry-title').text,'content': blog_soup.select_one(
            'div.entry-content').text.strip()}
    # add the text to the list
        all_blogs.append(blog_content)
    # return the text from all the blogs
    return all_blogs

def tokenize(string):
    '''This function takes in a dataframe column and tokenizes each string in the column. It returns the tokenized
        strings as a list.'''
    # make an empty list for the tokenized strings
    token = []
    # initiate the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # loop through the column and tokenize each string
    for item in string:
        item = tokenizer.tokenize(item, return_str=True)
        token.append(item)
    # return the list of tokenized strings
    return token

def stem(string):
    '''This function takes in a dataframe column and stems each string. It returns the stemmed strings as
        a list.'''
    # initiate the stemmer
    ps = nltk.porter.PorterStemmer()
    # create a new list for stemmed strings
    stemmed = []
    # loop through each item in the column and return a stemmed version
    for item in string:
        stems = [ps.stem(word) for word in item.split()]
        article_stemmed = ' '.join(stems)
    # add stemmed strings to the list
        stemmed.append(article_stemmed)
    # return list of stemmed strings
    return stemmed

def lemmatize(string):
    '''This function takes in a dataframe column and lemmatizes each string. It returns the lemmatized strings
        as a list.'''
    # initiate the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    # empty list for lemmatized strings
    lemlem = []
    # loop through each item in each column and lemmatize
    for item in string:
        lems = [wnl.lemmatize(word) for word in item.split()]
        article_lemmatized = ' '.join(lems)
        lemlem.append(article_lemmatized)
    # return a list of lemmatized strings
    return lemlem

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    '''This function takes in a dataframe column and optional parameters and returns each observation in the column
        with the stopwords removed.'''
    stop_list = stopwords.words('english')
    stopped = []
    for item in string:
        for word in extra_words:
            if item not in stop_list:
                stop_list.append(word)
        for word in exclude_words:    
            if item in stop_list:
                stop_list.remove(word) 
        words = item.split()
        words_stopped = [word for word in words if word not in stop_list]
        article_stopped = ' '.join(words_stopped)
        stopped.append(article_stopped)
    return stopped

def get_cats(base_url):
    '''This function takes in the url from the inshorts.com base page and acquires a list of categories using 
        BeautifulSoup. It returns the list of categories in all lowercase letters.'''
    soup = soupify(get(base_url).content)
    return [cat.text.lower() for cat in soup.find_all('li')[1:]]

def get_all_shorts(base_url):
    '''This function takes in a url and gets the list of categories using the get_cats function. It acquires the
        text for all articles in each category using BeautifulSoup and returns a dictionary of the title, category, 
        and text body for all articles.'''
    cats = get_cats(base_url)
    all_articles = []
    for cat in cats:
        cat_url = base_url + '/' + cat
        cat_soup = soupify(get(cat_url).content)
        cat_titles = [
            title.text for title in cat_soup.find_all('span', itemprop='headline')
        ]
        cat_bodies = [
            body.text for body in cat_soup.find_all('div', itemprop='articleBody')]
        cat_articles = [{'title': title,
        'category': cat,
        'body': body} for title, body in zip(
        cat_titles, cat_bodies)]
        all_articles.extend(cat_articles)
    return all_articles

