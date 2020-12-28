#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 16:36:55 2020

@author: mac
"""
#%% Imports
import glob
import os
from nltk.corpus import names
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

#%% Read email-files (emails array) and set label (labels array)
# Sample of mail
def print_sample_mail(path):
    with open(path, 'r') as infile:
        sample = infile.read()
    print(sample)
    
print('--------------------Legit mail--------------------')
print_sample_mail('enron1/ham/0007.1999-12-14.farmer.ham.txt') #legit mail

print('\n--------------------Spam mail--------------------')
print_sample_mail('enron1/spam/0058.2003-12-21.GP.spam.txt') #spam mail
 
emails, labels = [], []

for filename in glob.glob(os.path.join('enron1/spam/', '*.txt')):
    with open (filename, 'r', encoding="ISO-8859-1") as infile:
        emails.append(infile.read())
        labels.append(1)
        
for filename in glob.glob(os.path.join('enron1/ham/', '*.txt')):
    with open (filename, 'r', encoding="ISO-8859-1") as infile:
        emails.append(infile.read())
        labels.append(0)
        
#%% Pre-processing data   
# Pre-process and clean the raw text data:
#   Number and punctuation removal
#   Human name removal 
#   Stop-word removal: remove the, is, at etc...
#   Lemmetization: grouping together the inflected forms of a word so they can be analysed as a single item

def is_letter_only(word):
    return word.isalpha()

all_names = set(names.words())
lemmatizer = WordNetLemmatizer()

# Text-cleansing function:
def clean_text(docs):
    docs_cleaned = []
    for doc in docs:
        doc = doc.lower()
        doc_cleaned = ' '.join(lemmatizer.lemmatize(word) for word in doc.split() if is_letter_only(word) and word not in all_names)
        docs_cleaned.append(doc_cleaned)
    return docs_cleaned
emails_cleaned = clean_text(emails)

#%% Removal of stop words
#removal of stop words that can cause problems, term feature extraction
# max_feature: max number of features limit to 1000, excluding too common (50%) and too rare (2 min_df)
cv = CountVectorizer(stop_words="english", max_features=1000, max_df=0.5, min_df=2)
docs_cv = cv.fit_transform(emails_cleaned)

terms = cv.get_feature_names()

#%% Naive Bayes model from scratch
#%% Group data by label
def get_label_index(labels):
    """
    Group data by label and record the index of samples
    """
    from collections import defaultdict
    label_index = defaultdict(list)
    for index, label in enumerate(labels):
        label_index[label].append(index)
    return label_index

label_index = get_label_index(labels)
#output label_index {0: [3000, ...... 6670, 6671], 1: [0, ...., 2998, 2999]}
# training sample indices are grouped by class

#%% Compute prior 
# (The class prior is an estimate of the probability that 
# randomly sampling an instance from a population will yield 
# the given class (regardless of any attributes of the instance).)
# googla bild för att se alla delar i bayes sats (vad de kallas...)
def get_prior(label_index):
    """
    Compute prior based on training samples
    @param label_index: grouped sample indices by class
    @return: dictionary, with class label as key, corresponding prior as the value
    """
    prior = {label: len(index) for label, index in label_index.items()}
    total_count = sum(prior.values())
    for label in prior:
        prior[label] /= float(total_count)
    return prior
prior = get_prior(label_index)
print('Prior: ', prior)

#%% Compute likelihood
# Samma sak här... se bild för vart likelihooden i bayes sats är...
import numpy as np
def get_likelihood(term_matrix, label_index, smoothing=0):
    """
    Compute likelihood based on training samples
    @param term_matrix: sparse matrix of the term frequency features
    @param label_index: grouped sample indices by class
    @param smoothing: integer, additive Laplace smoothing parameter
    @return: dictionary, with class as key, corresponding conditional probability P(feature|clas) vector as value
    """
    likelihood = {}
    for label, index in label_index.items():
        likelihood[label] = term_matrix[index, :].sum(axis=0) + smoothing
        print('1:',likelihood)
        likelihood[label] = np.asarray(likelihood[label])[0]
        print('2:',likelihood)
        total_count = likelihood[label].sum()
        likelihood[label] = likelihood[label] / float(total_count)
    return likelihood

smoothing = 1
likelihood = get_likelihood(docs_cv, label_index, smoothing)
len(likelihood[0])

#likelihood[0] is P(feature | legit) vector of length 1000
#likelihood[1] is P(feature | spam) vector of length 1000

#%% Compute posterior
# Trick for handleing small value P(feature | class) is done here
def get_posterior(term_matrix, prior, likelihood):
    """
    Compute posterior of testing samples, based on prior and likelihood
    @param term_matrix: sparse matrix of the term frequency features
    @param prior: dictionary, with class label as key, corresponding prior as the value
    @param likelihood: dictionary, with class label as key, corresponding conditional prob vector as value
    @return: dictionary, with class label as key, corr posterior as value
    """
    num_docs = term_matrix.shape[0]
    posteriors = []
    for i in range(num_docs):
        # posterior is proportional to prior * likelihood
        # = exp(log(prior * likelihood))
        # = exp(log(prior) + log(likelihood))
        posterior = {key: np.log(prior_label) for key, prior_label in prior.items()}
        for label, likelihood_label in likelihood.items():
            term_document_vector = term_matrix.getrow(i)
            counts = term_document_vector.data
            indices = term_document_vector.indices
            for count, index in zip(counts, indices):
                posterior[label] += np.log(likelihood_label[index]) * count
        # exp(-1000):exp(-999) will cause zero division error,
        # however it equates to exp(0):exp(1)
        min_log_posterior = min(posterior.values())
        for label in posterior:
            try:
                posterior[label] = np.exp(posterior[label] - min_log_posterior)
            except:
                posterior[label] = float('inf')
        # normalize so that all sums up to 1
        sum_posterior = sum(posterior.values())
        for label in posterior:
            if posterior[label] == float('inf'):
                posterior[label] = 1.0
            else:
                posterior[label] /= sum_posterior
        posteriors.append(posterior.copy())
    return posteriors

emails_test = ['''Subject: flat screens hello , 
               please call or contact regarding the other flat screens
                 requested .
                 trisha tlapek - eb 3132 b
                 michael sergeev - eb 3132 a
                 also the sun blocker that was taken away from eb 3131 a .
                 trisha should two monitors also michael .
                 thanks
                 kevin moore''',
                 '''Subject: let ' s stop the mlm insanity !
                 still believe you can earn $ 100 , 000 fast in mlm ? get real !
                 get emm , a brand new system that replaces mlm with something that
            works !
                 start earning 1 , 000 ' s now ! up to $ 10 , 000 per week doing
            simple
                 online tasks .
                 free info - breakfree @ luxmail . com - type " send emm info " in
            the
            subject box .
                 this message is sent in compliance of the proposed bill section 301
            . per
                 section 301 , paragraph ( a ) ( 2 ) ( c ) of s . 1618 . further
            transmission
                 to you by the sender of this e - mail may be stopped at no cost to
            you by
                 sending a reply to : " email address " with the word remove in the
            subject
                 line .''',]
            
# Pre-processing
emails_cleaned_test = clean_text(emails_test)
term_docs_test = cv.transform(emails_cleaned_test)
posterior = get_posterior(term_docs_test, prior, likelihood)  
print(posterior)           
## Will give 99% for ham for first email, and 99% for spam for second email
            
            





        
        
        
        



