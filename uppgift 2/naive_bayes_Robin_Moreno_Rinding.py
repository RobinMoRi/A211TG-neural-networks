#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 21:08:37 2020

@author: Robin Moreno Rinding
"""
import pandas as pd

golf_df = pd.read_csv('golf_data.csv')
print(golf_df)

# group labels (taken from Python Machine Learning by Example)
def get_label_index(labels):
    from collections import defaultdict
    label_index = defaultdict(list)
    for index, label in enumerate(labels):
        label_index[label].append(index)
    return label_index
label_index = get_label_index(golf_df["game"])

#%% Compute prior probability
def get_prior(label_index):
    prior = {label: len(index) for label, index in label_index.items()}
    total_count = sum(prior.values())
    for label in prior:
        prior[label] /= float(total_count)
    return prior
prior = get_prior(label_index)
print('Prior: ', prior)

#%% Compute likelihood
import numpy as np
def get_likelihood(term_matrix, label_index, smoothing=0):
    likelihood = {}
    for label, index in label_index.items():
        print(label, index)
        likelihood[label] = term_matrix[index, :].sum(axis=0) + smoothing
        likelihood[label] = np.asarray(likelihood[label])[0]
        total_count = likelihood[label].sum()
        likelihood[label] = likelihood[label] / float(total_count)
    return likelihood

smoothing = 1
likelihood = get_likelihood(golf_df.values, label_index, smoothing)
len(likelihood[0])