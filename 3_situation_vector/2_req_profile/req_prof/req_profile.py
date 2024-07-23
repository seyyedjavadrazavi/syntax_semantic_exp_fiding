import pandas as pd
from csv import writer

posts = pd.read_xml(r'../../../data/bioinformatics/Posts.xml')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']

questions = posts.loc[posts['PostTypeId'] == 1]
answers = posts.loc[(posts['PostTypeId'] == 2) & (~posts['OwnerUserId'].isnull())]
del posts

users = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_Users.csv")
users = users[['Id', 'Reputation']]
unique_usrs = users['Id'].unique()

seman_tags = pd.read_csv(r'../../../data/bioinformatics/w2v_CBOW.csv')
tg_names = seman_tags.columns.values.tolist()

tags = pd.read_csv('../../../data/bioinformatics/bioinformatics_permutation_tags.csv', sep="\t", header=None)
tags = tags[0].str.split(',', expand=True)
tags.columns = ['qu_id', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5']
tags = tags.drop_duplicates(subset=['qu_id'])

############################## Start
ll = 0
for usr in unique_usrs:
    reputation = users.loc[users['Id'] == usr, 'Reputation'].values[0]
    res = 0
    print('User Id isssssssssss: ', usr)
    ques_ids = questions.loc[questions['OwnerUserId'] == usr, 'Id'].values.tolist()
    if len(ques_ids) == 0:
        continue
    
    # ques_ids = ques_ids['Id
    ques_ids = [str(int(x)) for x in ques_ids]
    sim_tgs = tags.loc[tags['qu_id'].isin(ques_ids), ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']].values.tolist()
    rltd_tgs = []
    [rltd_tgs.extend(x) for x in sim_tgs]
    sim_tgs = []
    for tg in rltd_tgs:
        if tg in tg_names:
            try:
                col = seman_tags[tg].values.tolist()
            except:
                continue
        else:
            continue
        sstgs = []
        sstgs.extend(col)
        sstgs.sort(reverse=True)
        sstgs = sstgs[:5]
        indeces = [col.index(i) for i in sstgs]
        names = []
        names = [tg_names[i] for i in indeces]
        sim_tgs.extend(names)
    
    cnd_ques = tags.loc[(tags['tag1'].isin(sim_tgs)) & (tags['tag2'].isin(sim_tgs)) & (tags['tag3'].isin(sim_tgs)) & (tags['tag4'].isin(sim_tgs)) & (tags['tag5'].isin(sim_tgs)), 'qu_id'].values.tolist()
    
    cnd_ques_ids = [int(x) for x in cnd_ques]
    sim_ques_ids = questions.loc[(questions['Id'].isin(cnd_ques_ids)) & (questions['OwnerUserId'] == usr), 'Id'].values.tolist()
    # sim_ques_ids = sim_ques['Id'].values.tolist()

    ques_ids = [int(x) for x in ques_ids]
    if len(sim_ques_ids) > 0:
        ques_ids.extend(sim_ques_ids)
    ques_ids = list(set(ques_ids))

    acan_ids = questions.loc[(questions['Id'].isin(ques_ids)) & (~questions['AcceptedAnswerId'].isnull())].values.tolist()

    res = len(acan_ids)/len(ques_ids) 

    with open('../../../data/bioinformatics/bioinformatics_requester_expertise.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        if ll == 0:
            writer_object.writerow(['user_id', 'expertise', 'reputation'])
            ll = 1

        writer_object.writerow([usr, res, reputation])
        f_object.close()
