import numpy as np
import pandas as pd
import copy

posts = pd.read_csv(r"../../../../data/bioinformatics/bioinformatics_Posts.csv")
data = pd.read_csv(r"../../../../data/bioinformatics/bioinformatics_avg_of_acan_score.csv")

questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]

candidate_list = list()
for usr in data.iterrows():
    print(usr[1]['UserId'])
    # print(type(usr[1]['UserId']))
    # print(questions.dtypes)
    qu = questions[questions['OwnerUserId'] == usr[1]['UserId']]
    ques_ids = qu['Id'].values.tolist()

    if len(qu) == 0:
        continue

    can_cnt = 0
    for i in qu.iterrows():
        ansrs = posts.loc[posts['ParentId'] == i[1]['Id']]
        for ans in ansrs.iterrows():
            if usr[1]['avg_scores'] < ans[1]['Score']:
                can_cnt += 1
                break ## be ezaee har soal 1 martabe mishomarim.

    candidate_list.append(copy.deepcopy([usr[1]['UserId'] , len(qu), can_cnt, can_cnt/len(qu)]))

df_cols = ['UserId', 'qu_cnt', 'candidate_cnt', 'percentage']
result = pd.DataFrame(candidate_list, columns=df_cols) 
result.to_csv(r"../../../../data/bioinformatics/bioinformatics_candidate_result.csv", index = False, header=True)
