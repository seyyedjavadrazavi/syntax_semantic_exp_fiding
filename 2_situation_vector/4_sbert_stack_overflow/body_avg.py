import pandas as pd
import copy
from csv import writer
import re
from bs4 import BeautifulSoup

posts = pd.read_csv(r"../../data/english/english_Posts.csv")
# sub_ques = pd.read_csv(r"../../data/english/english_union_qu_ids.csv")
# sub_uniq_ques = sub_ques['qu_id'].values.tolist()
# sub_uniq_ques.extend(sub_ques['sim_ques'].values.tolist())

# sub_uniq_ques = list(set(sub_uniq_ques))

posts = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]

mean = posts['Body'].apply(len).mean()

print('The average nymber of words in the english questions\' body is', mean)


'The average nymber of words in the ai questions\' body is 915.4834834834835'
'The average nymber of words in the bioinformatics questions\' body is 1428.4168912848158'
'The average nymber of words in the biology questions\' body is 662.8708845696152'
'The average nymber of words in the english questions\' body is 611.6817633724015'
'The average nymber of words in the history questions\' body is 867.7828875045805'