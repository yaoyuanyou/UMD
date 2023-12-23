#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:29:17 2023

@author: tonyyao
"""

#Import Libraries

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re
import string
from gensim.parsing.preprocessing import remove_stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
!pip install contractions
import contractions
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from bs4 import BeautifulSoup

#Import Dataset

df = pd.read_csv("/Users/tonyyao/Python/amazon_reviews_multilingual_US_v1_00.tsv", sep = '\t', on_bad_lines='skip')

#Show some basic aspect of the dataset

print(df.head())
print("---------------")
print(df.shape)
print("---------------")
print(df.info())

#Select useful columns

data = df[['product_title', 'product_category', 'star_rating', 'helpful_votes', 'total_votes',
           'review_headline', 'review_body', 'review_date']]

#Check empty rows

print(data.isnull().sum())

#Remove empty rows

data = data.dropna()

#Check numbers of reviews on different categories

cat = data.groupby('product_category')['product_category'].count()

print(cat)

plt.bar(cat.index, cat)
plt.show()

#Focus on category of Mobile_Apps

Mobile_Apps_Data = data[data['product_category'] == 'Mobile_Apps']

print(Mobile_Apps_Data.head())

#Descriptive Analysis of star rating and review dates

rating = Mobile_Apps_Data.groupby('star_rating')['star_rating'].count()

plt.bar(rating.index, rating)
plt.show()

year = [x[:4] for x in Mobile_Apps_Data['review_date']]
Mobile_Apps_Data['review_year'] = year
year_count = Counter(year)

plt.bar(year_count.keys(),year_count.values())
plt.show()
    
#Define function to explore review length

def len_of_review(rev):
    if type(rev) != float:
        leng = len(rev)
    else:
        leng = 0
    return leng

#99% of the reviews are within 1000 letters, not a big deal:)

plt.hist(Mobile_Apps_Data['review_body'].apply(len_of_review), range=[0, 30000], facecolor='gray', align='mid')

#Define function to clean text, standardize text formats.

def clean_text(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    text = remove_stopwords(text)
    return text

# Applying text cleaning lowercasing and removing punctuation to Book Titles.

Mobile_Apps_Data['product_title'] = Mobile_Apps_Data['product_title'].apply(clean_text)

print(Mobile_Apps_Data.head())

#Pop unrelated columns

Mobile_Apps_Data = Mobile_Apps_Data[['product_title', 'star_rating', 'review_headline', 'review_body', 'review_year']]

#Focus on polorized ratings in 2015

Mobile_Apps_Data_2015 = Mobile_Apps_Data[Mobile_Apps_Data['review_year'] == '2015']
Mobile_Apps_Data_5Star = Mobile_Apps_Data_2015[Mobile_Apps_Data_2015['star_rating'] == 5]
Mobile_Apps_Data_1Star = Mobile_Apps_Data_2015[Mobile_Apps_Data_2015['star_rating'] == 1]

#Most popular mobile games in people's reviews

print(Counter(Mobile_Apps_Data_2015['product_title']).most_common(20))
print("---------------")
print(Counter(Mobile_Apps_Data_5Star['product_title']).most_common(20))
print("---------------")
print(Counter(Mobile_Apps_Data_1Star['product_title']).most_common(20))

#Check why people have some bad comments on Facebook and Facebook Messenger LOL!

classes = []

for row in Mobile_Apps_Data_1Star['product_title']:
    if 'facebook' in row:
        classes.append("facebook")
    elif 'amazon underground' in row:
        classes.append("amazon underground")
    else:
        classes.append("other")

classes_5 = []

for row in Mobile_Apps_Data_5Star['product_title']:
    if 'amazon underground' in row:
        classes_5.append("amazon underground")
    else:
        classes_5.append("other")
        
Mobile_Apps_Data_1Star['classification'] = classes

Mobile_Apps_Data_5Star['classification'] = classes_5


Mobile_Apps_Data_Facebook = Mobile_Apps_Data_1Star[Mobile_Apps_Data_1Star['classification'] == 'facebook']

Mobile_Apps_Data_A1 = Mobile_Apps_Data_1Star[Mobile_Apps_Data_1Star['classification'] == 'amazon underground']

Mobile_Apps_Data_A5 = Mobile_Apps_Data_5Star[Mobile_Apps_Data_5Star['classification'] == 'amazon underground']

#Create Word Cloud
Facebook_Reviews = Mobile_Apps_Data_Facebook.groupby('star_rating')['review_body'].apply(','.join).reset_index()

#Create Contractions

stop=set(stopwords.words('english'))
snow = nltk.stem.SnowballStemmer('english')

def clean_text(text):
    '''Make text lowercase, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r"n\'t","not",text)
    text = re.sub(r"\'re","are",text)
    text = re.sub(r"\'s","is",text)
    text = re.sub(r"\'d","would",text)
    text = re.sub(r"\'ll","will",text)    
    text = re.sub(r"\'t","not",sentence)
    text = re.sub(r"\'ve","have",sentence)
    text = re.sub(r"\'m","am",sentence)
    text = remove_stopwords(text)
    text = contractions.fix(text)
    return text

preprocessed_reviews=[]


for sentence in Facebook_Reviews['review_body']:
    sentence=re.sub(r"http\S+"," ",sentence)
    sentence=BeautifulSoup(sentence,'lxml').get_text()
    cleanr=re.compile('<.*?>')
    sentence=re.sub(cleanr,' ',sentence)
    sentence=clean_text(sentence)
    sentence=re.sub("\S\*\d\S*"," ",sentence)
    sentence=re.sub("[^A-Za-z]+"," ",sentence)
    sentence=re.sub(r'[?|!|\'|"|#]',r' ',sentence)
    sentence=re.sub(r'[.|,|)|(|\|/]',r' ',sentence)
    sentence = sentence.lower()
    preprocessed_reviews.append(sentence.strip())
    
# Start with one review:

stopwords = set(STOPWORDS)
stopwords.update(["racism", "one", "understand", "year", "work", "study", "american", "book", "read", "information"])

# Generate a word cloud image
wordcloud = WordCloud(max_font_size=50, max_words=500,stopwords=stopwords, background_color="white",width=800, height=400).generate(preprocessed_reviews[0])

# Display the generated image:
# the matplotlib way:
plt.figure( figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Facebook')
plt.show()

