import pandas as pd
import itertools
from csv import writer

# Load and preprocess the data
posts = pd.read_csv(r'../../data/bioinformatics/bioinformatics_Posts.csv')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']

post_tags = posts[['Id','Tags']]

per_tgs = []
for tg in post_tags.iterrows():
    if pd.notna(tg):
        tag_list = tg.split('|')
        tag_list = [tag for tag in tag_list if tag]
      
        tag_permutations = list(itertools.permutations(tag_list))

        crnt_per_tgs = [per_tgs.extend(list(per)) for per in tag_permutations if per not in per_tgs]
        # Add post ID to each permutation
        [x.insert(0, tg[1]['Id']) for x in crnt_per_tgs]

        # Write permutations to CSV
        with open('../../data/bioinformatics/bioinformatics_permutation_tags.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            [writer_object.writerow(i) for i in crnt_per_tgs]
            
print('Done')
