import pandas as pd
import copy
import csv
from csv import writer
import itertools

question_tag = []

posts = pd.read_csv(r'../../data/bioinformatics/bioinformatics_Posts.csv')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']

p_tgs = posts[['Id','Tags']]

per_tgs = []
cnt = 1

for tg in p_tgs.iterrows():
    if (str(tg[1]['Tags']) != 'nan'):
        qu_tag = tg[1]['Tags']
        qu_tag = qu_tag.split('|')
        qu_tag.remove('')
        qu_tag.remove('')
        qu_tag.sort()
        qu_tag.insert(0, tg[1]['Id'])
        question_tag.append(copy.deepcopy(qu_tag))
        

l2 = [itm for itm in question_tag if len(itm) == 2]
l3 = [itm for itm in question_tag if len(itm) == 3]
l4 = [itm for itm in question_tag if len(itm) == 4]
l5 = [itm for itm in question_tag if len(itm) == 5]
l6 = [itm for itm in question_tag if len(itm) == 6]
l7 = [itm for itm in question_tag if len(itm) == 7]
l8 = [itm for itm in question_tag if len(itm) == 8]

df_tgs_len1 = pd.DataFrame(l2, columns=['ques_id', 'tag1'])
df_tgs_len1.to_csv('../../data/bioinformatics/bioinformatics_tags_observation_len1.csv')

df_tgs_len2 = pd.DataFrame(l3, columns=['ques_id', 'tag1', 'tag2'])
df_tgs_len2.to_csv('../../data/bioinformatics/bioinformatics_tags_observation_len2.csv')

df_tgs_len3 = pd.DataFrame(l4, columns=['ques_id', 'tag1', 'tag2', 'tag3'])
df_tgs_len3.to_csv('../../data/bioinformatics/bioinformatics_tags_observation_len3.csv')

df_tgs_len4 = pd.DataFrame(l5, columns=['ques_id', 'tag1', 'tag2', 'tag3', 'tag4'])
df_tgs_len4.to_csv('../../data/bioinformatics/bioinformatics_tags_observation_len4.csv')

df_tgs_len5 = pd.DataFrame(l6, columns=['ques_id', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5'])
df_tgs_len5.to_csv('../../data/bioinformatics/bioinformatics_tags_observation_len5.csv')

# df_tgs_len6 = pd.DataFrame(l7, columns=['ques_id', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6'])
# df_tgs_len6.to_csv('tags_observation_len6.csv')
