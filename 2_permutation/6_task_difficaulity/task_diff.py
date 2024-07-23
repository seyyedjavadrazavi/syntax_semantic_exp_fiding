import pandas as pd
import datetime

posts = pd.read_xml(r'../../data/bioinformatics/Posts.xml')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < datetime.datetime.strptime('2019-06-01T00:00:00.000000', '%Y-%m-%dT%H:%M:%S.%f')]
questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]
idis = questions['Id'].values.tolist()
del questions

users = pd.read_csv(r'../../data/bioinformatics/bioinformatics_Users.csv')
sim_questions_subs = pd.read_csv(r'../../data/bioinformatics/bioinformatics_avg_scores_subscription.csv')
sim_questions_ordring = pd.read_csv(r'../../data/bioinformatics/bioinformatics_avg_scores_by_order.csv')
sim_questions_ordring.columns = ['qu_id', 'sim_ques_id', 'score']

subs_task_dfclty = []
ordr_task_dfclty = []
for id in idis:
############################ Subscriptoin
    sim_cnd = sim_questions_subs.loc[sim_questions_subs['qu_id'] == id, 'sim_ques_id'].values.tolist()
    sim_cnd = [int(x) for x in sim_cnd]
    sim_cnd = list(set(sim_cnd))
    acans = posts.loc[(posts['Id'].isin(sim_cnd)) & (~posts['AcceptedAnswerId'].isnull()), 'AcceptedAnswerId'].values.tolist()
    wrkrs = posts.loc[posts['Id'].isin(acans), 'OwnerUserId'].values.tolist()
    rep_usrs = users.loc[users['Id'].isin(wrkrs), 'Reputation'].values.tolist()

    if len(rep_usrs) == 0:
        continue

    rep_avrg = sum(rep_usrs) / len(rep_usrs)
    subs_task_dfclty.append([id, rep_avrg])

############################## Ordering 
    sim_cnd = sim_questions_ordring.loc[sim_questions_ordring['qu_id'] == id, 'sim_ques_id'].values.tolist()
    sim_cnd = [int(x) for x in sim_cnd]
    sim_cnd = list(set(sim_cnd))
    acans = posts.loc[(posts['Id'].isin(sim_cnd)) & (~posts['AcceptedAnswerId'].isnull()), 'AcceptedAnswerId'].values.tolist()
    wrkrs = posts.loc[posts['Id'].isin(acans), 'OwnerUserId'].values.tolist()
    rep_usrs = users.loc[users['Id'].isin(wrkrs), 'Reputation'].values.tolist()
    
    if len(rep_usrs) == 0:
        continue
    
    rep_avrg = sum(rep_usrs) / len(rep_usrs)
    ordr_task_dfclty.append([id, rep_avrg])

df_tsk_difclty = pd.DataFrame(subs_task_dfclty, columns=['id', 'rep_avg'])
df_tsk_difclty.to_csv('../../data/bioinformatics/bioinformatics_task_difficaulty_subs.csv', index = False)

df_tsk_difclty = pd.DataFrame(ordr_task_dfclty, columns=['id', 'rep_avg'])
df_tsk_difclty.to_csv('../../data/bioinformatics/bioinformatics_task_difficaulty_ordering.csv', index = False)

