import pandas as pd
import itertools
from csv import writer

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
      
        tmp_tgs = list(itertools.permutations(qu_tag))

        crnt_per_tgs = [list(per) for per in tmp_tgs if per not in per_tgs]
        [x.insert(0, tg[1]['Id']) for x in crnt_per_tgs]

        with open('../../data/bioinformatics/bioinformatics_permutation_tags.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            for i in crnt_per_tgs:
                writer_object.writerow(i)

            f_object.close()
