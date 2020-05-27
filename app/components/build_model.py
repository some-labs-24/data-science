from build_post_list import build_post_list
from tweet_cleaning import emoji_free_text, url_free_text

# Required Libraries

#Base and Cleaning 
import json
import requests
import pandas as pd
import numpy as np
import emoji
import re
import string
from collections import Counter

#Natural Language Processing (NLP)
import spacy
from spacy.tokenizer import Tokenizer
from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.coherencemodel import CoherenceModel
from gensim.parsing.preprocessing import STOPWORDS as SW
from wordcloud import STOPWORDS
stopwords = set(STOPWORDS)

### ask lawrence if he agrees to have the cleaned data set stored at elephantsql


def build_model(twitter_handle, num_followers_to_scan):
    #Creating the dataframe from tweets pulled from Twitter API
    data = build_post_list(twitter_handle, num_followers_to_scan=num_followers_to_scan)

    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.rename(columns={0:'tweets'})
    df['tweets'] = df['tweets'].apply(emoji_free_text)
    df['tweets'] = df['tweets'].apply(url_free_text)

    # Tokenizing the tweets
    nlp = spacy.load('en_core_web_sm')

    tokenizer = Tokenizer(nlp.vocab)
    custom_stopwords = ['hi']
    # Customize stop words by adding to the default list
    STOP_WORDS = nlp.Defaults.stop_words.union(custom_stopwords)
    # ALL_STOP_WORDS = spacy + gensim + wordcloud
    ALL_STOP_WORDS = STOP_WORDS.union(SW).union(stopwords)

    tokens = []
    for doc in tokenizer.pipe(df['tweets'], batch_size=500):
        doc_tokens = []  
        for token in doc:
            if token.text.lower() not in STOP_WORDS:
                doc_tokens.append(token.text.lower())
        tokens.append(doc_tokens)
    # Makes tokens column
    df['tokens'] = tokens
    # Make tokens a string again

    # Refrence 4 : https://stackoverflow.com/questions/45306988/column-of-lists-convert-list-to-string-as-a-new-column
    df['tokens_back_to_text'] = [' '.join(map(str, l)) for l in df['tokens']]

    # Lemmitization
    def get_lemmas(text):

        '''Used to lemmatize the processed tweets'''
        lemmas = []
    
        doc = nlp(text)
    
        # Something goes here :P
        for token in doc: 

            if ((token.is_stop == False) and (token.is_punct == False)) and (token.pos_ != 'PRON'):
                lemmas.append(token.lemma_)
    
        return lemmas

    df['lemmas'] = df['tokens_back_to_text'].apply(get_lemmas)

    # Make lemmas a string again
    df['lemmas_back_to_text'] = [' '.join(map(str, l)) for l in df['lemmas']]

    # Tokenizing lemmas and cleaning tokens
    def tokenize(text):
        """
        Parses a string into a list of semantic units (words)
        Args:
            text (str): The string that the function will tokenize.
        Returns:
            list: tokens parsed out
        """
        # Removing url's
        pattern = r"http\S+"
        
        tokens = re.sub(pattern, "", text) # https://www.youtube.com/watch?v=O2onA4r5UaY
        tokens = re.sub('[^a-zA-Z 0-9]', '', text)
        tokens = re.sub('[%s]' % re.escape(string.punctuation), '', text) # Remove punctuation
        tokens = re.sub('\w*\d\w*', '', text) # Remove words containing numbers
        tokens = re.sub('@*!*\$*', '', text) # Remove @ ! $
        tokens = tokens.strip(',') # TESTING THIS LINE
        tokens = tokens.strip('?') # TESTING THIS LINE
        tokens = tokens.strip('!') # TESTING THIS LINE
        tokens = tokens.strip("'") # TESTING THIS LINE
        tokens = tokens.strip(".") # TESTING THIS LINE

        tokens = tokens.lower().split() # Make text lowercase and split it
        
        return tokens

    # Apply tokenizer
    df['lemma_tokens'] = df['lemmas_back_to_text'].apply(tokenize)

    # Create a id2word dictionary
    id2word = Dictionary(df['lemma_tokens'])
    # Filtering Extremes
    id2word.filter_extremes(no_below=2, no_above=.99)
    # Creating a corpus object 
    corpus = [id2word.doc2bow(d) for d in df['lemma_tokens']]
    # Instantiating a LDA model 
    model = LdaMulticore(corpus=corpus, num_topics=5, id2word=id2word, workers=12, passes=5)
    # Filtering for words 
    words = [re.findall(r'"([^"]*)"',t[1]) for t in model.print_topics()]
    # Create Topics
    topics = [' '.join(t[0:10]) for t in words]
    
    topics_list = []

    for id, t in enumerate(topics): 
        topics_list.append(t)

    dictOfWords = { i : topics_list[i] for i in range(0, len(topics_list) ) }
    
    print(dictOfWords)


if __name__ == "__main__":
    build_model('DutchBros', 5)