import pandas as pd
import copy

posts = pd.read_csv(r"../../../../data/bioinformatics/bioinformatics_Posts.csv")

questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]

questions = questions.dropna(subset=['OwnerUserId'])

unique_usrs = questions.OwnerUserId.unique().tolist()

score_list = list()
for usr in unique_usrs:
    qu = questions.loc[questions['OwnerUserId'] == usr]
    if qu.empty == True:
        continue
    
    answers = posts[posts['Id'].isin(qu['AcceptedAnswerId'].values.tolist())]
    # res = pd.merge(qu, posts, how='inner', left_on='AcceptedAnswerId', right_on='Id')
    usr_scrs = list()
    usr_scrs = answers['Score'].values.tolist()
    # for i in res.iterrows():
    #     scr = i[1]['Score']
    #     usr_scrs.append(copy.deepcopy(scr))

    if len(usr_scrs) == 0:
        score_list.append(copy.deepcopy([usr, 0]))
    else:
        score_list.append(copy.deepcopy([usr, sum(usr_scrs)/len(usr_scrs)]))

df_cols = ['UserId', 'avg_scores']
result = pd.DataFrame(score_list, columns=df_cols) 
result.to_csv(r"../../../../data/bioinformatics/bioinformatics_avg_of_acan_score.csv", index = False, header=True)