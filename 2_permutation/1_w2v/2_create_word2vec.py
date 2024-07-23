##references https://radimrehurek.com/gensim/models/word2vec.html
# https://towardsdatascience.com/a-beginners-guide-to-word-embedding-with-gensim-word2vec-model-5970fa56cc92
##https://www.geeksforgeeks.org/python-word-embedding-using-word2vec/

import warnings
import gensim
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import copy
import csv
from csv import writer

warnings.filterwarnings(action = 'ignore')

tags = pd.read_csv(r'../../data/bioinformatics/bioinformatics_Tags.csv')
tags_name = tags['TagName'].values.tolist()

data = []
with open('../../data/bioinformatics/bioinformatics_permutation_tags.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        row = row[0].split(',')
        data.append(copy.deepcopy(row[1:]))

# Create CBOW model
model1 = Word2Vec(data, min_count = 1, vector_size = 200, window = 5, workers=10)
model1.save("../../data/bioinformatics/word2vec_CBOW_with_n.model")

# Create Skip Gram model
model2 = Word2Vec(data, min_count = 1, vector_size = 200, window = 5, workers=10, sg = 1)
model2.save("../../data/bioinformatics/word2vec_Skip_Gram_with_n.model")

cnt = 1
for tg in tags_name:
    # tg = tg.lower()
    bag_of_word = []
    n_gram = []

    for row in tags_name:
        try:
            ngram = float(model2.wv.similarity(tg, row))
            n_gram.append(copy.deepcopy(ngram))
            bg = float(model1.wv.similarity(tg, row))
            bag_of_word.append(copy.deepcopy(bg))
        except Exception as inst:
            bag_of_word.append(copy.deepcopy(-1))
            n_gram.append(copy.deepcopy(-1))

    with open('../../data/bioinformatics/w2v_CBOW.csv', 'a', newline='') as f_object:  
        if cnt == 1:
            cl_name = tags_name
            
            writer_object = writer(f_object)
            writer_object.writerow(cl_name)
            writer_object.writerow(bag_of_word)
            f_object.close()
        else:
            writer_object = writer(f_object)
            writer_object.writerow(bag_of_word)
            f_object.close()            

    with open('../../data/bioinformatics/w2v_NGram.csv', 'a', newline='') as f_object:  
        if cnt == 1:
            cl_name = tags_name
            
            writer_object = writer(f_object)
            writer_object.writerow(cl_name)
            writer_object.writerow(n_gram)
            f_object.close()
            cnt += 1
        else:
            writer_object = writer(f_object)
            writer_object.writerow(n_gram)
            f_object.close()            
