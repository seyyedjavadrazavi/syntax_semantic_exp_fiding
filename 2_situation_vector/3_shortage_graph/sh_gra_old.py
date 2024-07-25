import pandas as pd
import copy
import csv
from csv import writer
import itertools
import math
import timeit

posts = pd.read_xml(r'../../data/history/Posts.xml')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']

questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]
idis = questions['Id'].values.tolist()

del posts
del questions

seman_tags = pd.read_csv(r'../../data/history/w2v_CBOW.csv')
tg_names = seman_tags.columns.values.tolist()

tag_obs_len1 = pd.read_csv(r'../../data/history/history_tags_observation_len1.csv')    
tag_obs_len2 = pd.read_csv(r'../../data/history/history_tags_observation_len2.csv')
tag_obs_len3 = pd.read_csv(r'../../data/history/history_tags_observation_len3.csv')
tag_obs_len4 = pd.read_csv(r'../../data/history/history_tags_observation_len4.csv')
tag_obs_len5 = pd.read_csv(r'../../data/history/history_tags_observation_len5.csv')
    
ll = 0

# ind = idis.index(42)
# idis = idis[ind:]
for qu in idis:
    # start_1 = timeit.default_timer()
    print(qu)
    
    sim_qu = []
    sem_sim_tgs = []
    crnt_tgs = []

    tags_size = 0
    crnt_tgs_l1 = tag_obs_len1.loc[tag_obs_len1['ques_id'] == qu]
    crnt_tgs_l2 = tag_obs_len2.loc[tag_obs_len2['ques_id'] == qu]
    crnt_tgs_l3 = tag_obs_len3.loc[tag_obs_len3['ques_id'] == qu]
    crnt_tgs_l4 = tag_obs_len4.loc[tag_obs_len4['ques_id'] == qu]
    crnt_tgs_l5 = tag_obs_len5.loc[tag_obs_len5['ques_id'] == qu]

    if len(crnt_tgs_l1) != 0:
        org_tgs = crnt_tgs_l1.iloc[:, 2:].values[0].tolist()
        # qu_bag_1 = tag_obs_len1.iloc[:, 1].values.tolist()
        tags_size = 1            
    elif len(crnt_tgs_l2) != 0:
        org_tgs = crnt_tgs_l2.iloc[:, 2:].values[0].tolist()
        tags_size = 2
    elif len(crnt_tgs_l3) != 0:
        org_tgs = crnt_tgs_l3.iloc[:, 2:].values[0].tolist()
        tags_size = 3
    elif len(crnt_tgs_l4) != 0:
        org_tgs = crnt_tgs_l4.iloc[:, 2:].values[0].tolist()
        tags_size = 4
    elif len(crnt_tgs_l5) != 0:
        org_tgs = crnt_tgs_l5.iloc[:, 2:].values[0].tolist()
        tags_size = 5
    
    org_tgs = [str(x) for x in org_tgs]

    org_tgs.sort()

    crnt_tgs.extend(org_tgs) 
    if crnt_tgs[0] != 'null' and crnt_tgs[0] != 'nan':
        tg  = crnt_tgs[0]
        del crnt_tgs[0]
    else:
        tg  = crnt_tgs[1]
        del crnt_tgs[0:2]

    col = seman_tags[tg].values.tolist()
    col.sort(reverse=True)
    col = col[:5]
    indeces = [col.index(i) for i in col]
    names = [tg_names[i] for i in indeces]

    df_qu_bag_1 = tag_obs_len1[tag_obs_len1['tag1'].isin(names)]
    df_qu_bag_2 = tag_obs_len2[(tag_obs_len2['tag1'].isin(names)) | ((tag_obs_len2['tag2'].isin(names)))]
    df_qu_bag_3 = tag_obs_len3[(tag_obs_len3['tag1'].isin(names)) | (tag_obs_len3['tag2'].isin(names)) | (tag_obs_len3['tag3'].isin(names))]
    df_qu_bag_4 = tag_obs_len4[(tag_obs_len4['tag1'].isin(names)) | (tag_obs_len4['tag2'].isin(names)) | (tag_obs_len4['tag3'].isin(names)) | (tag_obs_len4['tag4'].isin(names))]
    df_qu_bag_5 = tag_obs_len5[(tag_obs_len5['tag1'].isin(names)) | (tag_obs_len5['tag2'].isin(names)) | (tag_obs_len5['tag3'].isin(names)) | (tag_obs_len5['tag4'].isin(names)) | (tag_obs_len5['tag5'].isin(names))]


    if len(df_qu_bag_1) > 0:
        df_qu_bag_1.loc[df_qu_bag_1['tag1'].isin(org_tgs), 'score'] = 1
        tmp_ques_1 = df_qu_bag_1
    if len(df_qu_bag_2) > 0:
        df_qu_bag_2.loc[(tag_obs_len2['tag1'].isin(org_tgs)) | ((tag_obs_len2['tag2'].isin(org_tgs))), 'score'] = 1
        tmp_ques_2 = df_qu_bag_2
    if len(df_qu_bag_3) > 0:
        df_qu_bag_3.loc[(tag_obs_len3['tag1'].isin(org_tgs)) | (tag_obs_len3['tag2'].isin(org_tgs)) | (tag_obs_len3['tag3'].isin(org_tgs)), 'score'] = 1
        tmp_ques_3 = df_qu_bag_3
    if len(df_qu_bag_4) > 0:
        df_qu_bag_4.loc[(tag_obs_len4['tag1'].isin(org_tgs)) | (tag_obs_len4['tag2'].isin(org_tgs)) | (tag_obs_len4['tag3'].isin(org_tgs)) | (tag_obs_len4['tag4'].isin(org_tgs)), 'score'] = 1
        tmp_ques_4 = df_qu_bag_4
    if len(df_qu_bag_5) > 0:
        df_qu_bag_5.loc[(tag_obs_len5['tag1'].isin(org_tgs)) | (tag_obs_len5['tag2'].isin(org_tgs)) | (tag_obs_len5['tag3'].isin(org_tgs)) | (tag_obs_len5['tag4'].isin(org_tgs)) | (tag_obs_len5['tag5'].isin(org_tgs)), 'score'] = 1
        tmp_ques_5 = df_qu_bag_5

    cnt = 0
    for i in names:
        scr = col[cnt]
        cnt += 1
        # scr = col.loc[col['sim_tag'] == i, 'similarity'].values[0]
        if len(df_qu_bag_1) > 0:
            df_qu_bag_1.loc[df_qu_bag_1['tag1'] == i, 'score'] = scr
            tmp_ques_1 = df_qu_bag_1
        if len(df_qu_bag_2) > 0:
            df_qu_bag_2.loc[(df_qu_bag_2['tag1'] == i) | (df_qu_bag_2['tag2'] == i), 'score'] = scr
            tmp_ques_2 = df_qu_bag_2
        if len(df_qu_bag_3) > 0:
            df_qu_bag_3.loc[(df_qu_bag_3['tag1'] == i) | (df_qu_bag_3['tag2'] == i), 'score'] = scr
            tmp_ques_3 = df_qu_bag_3
        if len(df_qu_bag_4) > 0:
            df_qu_bag_4.loc[(df_qu_bag_4['tag1'] == i) | (df_qu_bag_4['tag2'] == i), 'score'] = scr
            tmp_ques_4 = df_qu_bag_4
        if len(df_qu_bag_5) > 0:
            df_qu_bag_5.loc[(df_qu_bag_5['tag1'] == i) | (df_qu_bag_5['tag1'] == i), 'score'] = scr
            tmp_ques_5 = df_qu_bag_5
    
    cnt = 0
    sim_qu = []
    for tg in crnt_tgs:
        if tg == 'null' or tg == 'nan':
            continue

        col = seman_tags[tg].values.tolist()
        col.sort(reverse=True)
        col = col[:5]
        indeces = [col.index(i) for i in col]
        names = [tg_names[i] for i in indeces]
        # names.append(copy.deepcopy(tg))

        if len(df_qu_bag_1) > 0:
            tmp_ques_1 = tmp_ques_1[tmp_ques_1['tag1'].isin(names)]
    
        if len(df_qu_bag_2) > 0:
            tmp_ques_2 = tmp_ques_2[(tmp_ques_2['tag1'].isin(names)) | ((tmp_ques_2['tag2'].isin(names)))]

        if len(df_qu_bag_3) > 0:
            tmp_ques_3 = tmp_ques_3[(tmp_ques_3['tag1'].isin(names)) | (tmp_ques_3['tag2'].isin(names)) | (tmp_ques_3['tag3'].isin(names))]

        if len(df_qu_bag_4) > 0:
            tmp_ques_4 = tmp_ques_4[(tmp_ques_4['tag1'].isin(names)) | (tmp_ques_4['tag2'].isin(names)) | (tmp_ques_4['tag3'].isin(names)) | (tmp_ques_4['tag4'].isin(names))]

        if len(df_qu_bag_5) > 0:
            tmp_ques_5 = tmp_ques_5[(tmp_ques_5['tag1'].isin(names)) | (tmp_ques_5['tag2'].isin(names)) | (tmp_ques_5['tag3'].isin(names)) | (tmp_ques_5['tag4'].isin(names)) | (tmp_ques_5['tag5'].isin(names))]

        tmp_ques = []
        for i in names:
            if i in org_tgs:
                if len(df_qu_bag_1) > 0:
                    if len(tmp_ques_1) > 0:
                        tmp_ques_1['score'] = math.pow(tmp_ques_1['score'].values[0] * 1, 0.5)
                        tmp_ques.extend(tmp_ques_1.values.tolist())
                if len(df_qu_bag_2) > 0:
                    if len(tmp_ques_2) > 0:
                        tmp_ques_2['score'] = math.pow(tmp_ques_2['score'].values[0] * 1, 0.5)
                        tmp_ques.extend(tmp_ques_2.values.tolist())
                if len(df_qu_bag_3) > 0:
                    if len(tmp_ques_3) > 0:
                        tmp_ques_3['score'] = math.pow(tmp_ques_3['score'].values[0] * 1, 0.5)
                        tmp_ques.extend(tmp_ques_3.values.tolist())
                if len(df_qu_bag_4) > 0:
                    if len(tmp_ques_4) > 0:
                        tmp_ques_4['score'] = math.pow(tmp_ques_4['score'].values[0] * 1, 0.5)
                        tmp_ques.extend(tmp_ques_4.values.tolist())
                if len(df_qu_bag_5) > 0:
                    if len(tmp_ques_5) > 0:
                        tmp_ques_5['score'] = math.pow(tmp_ques_5['score'].values[0] * 1, 0.5)
                        tmp_ques.extend(tmp_ques_5.values.tolist())

            else:
                scr = col[cnt]
                # scr = col.loc[col['sim_tag'] == i, 'similarity'].values[0]
                if len(df_qu_bag_1) > 0:
                    if len(tmp_ques_1) > 0:
                        tmp_ques_1['score'] = math.pow(tmp_ques_1['score'].values[0] * scr, 0.5)
                        tmp_ques.extend(tmp_ques_1.values.tolist())
                if len(df_qu_bag_2) > 0:
                    if len(tmp_ques_2) > 0:
                        tmp_ques_2['score'] = math.pow(tmp_ques_2['score'].values[0] * scr, 0.5)
                        tmp_ques.extend(tmp_ques_2.values.tolist())
                if len(df_qu_bag_3) > 0:
                    if len(tmp_ques_3) > 0:
                        tmp_ques_3['score'] = math.pow(tmp_ques_3['score'].values[0] * scr, 0.5)
                        tmp_ques.extend(tmp_ques_3.values.tolist())
                if len(df_qu_bag_4) > 0:
                    if len(tmp_ques_4) > 0:
                        tmp_ques_4['score'] = math.pow(tmp_ques_4['score'].values[0] * scr, 0.5)
                        tmp_ques.extend(tmp_ques_4.values.tolist())
                if len(df_qu_bag_5) > 0:
                    if len(tmp_ques_5) > 0:
                        tmp_ques_5['score'] = math.pow(tmp_ques_5['score'].values[0] * scr, 0.5)
                        tmp_ques.extend(tmp_ques_5.values.tolist())

        tmp_ques.sort()
        tmp_ques = list(tmp_ques for tmp_ques,_ in itertools.groupby(tmp_ques))

        crnt_ans = 20
        if len(tmp_ques) > crnt_ans:
            sim_qu = tmp_ques
        else:
            break
            
    if len(sim_qu) == 0:
        if len(crnt_tgs) == 0:
            if (len(org_tgs) == 1) & (len(tmp_ques_1) > 0):
                sorted_data = tmp_ques_1.values.tolist()
                sorted_data.sort(key=lambda x:x[2], reverse=True)
                sim_qu.extend(sorted_data[:20])
            
            if (len(org_tgs) <= 2) & (len(tmp_ques_2) > 0) & (len(sim_qu) < 20):
                sorted_data = tmp_ques_2.values.tolist()
                sorted_data.sort(key=lambda x:x[3], reverse=True)
                sim_qu.extend(sorted_data[:20])
            
            if (len(org_tgs) <= 3) & (len(tmp_ques_3) > 0) & (len(sim_qu) < 20):
                sorted_data = tmp_ques_3.values.tolist()
                sorted_data.sort(key=lambda x:x[4], reverse=True)
                sim_qu.extend(sorted_data[:20])

            if (len(org_tgs) <= 4) & (len(tmp_ques_4) > 0) & (len(sim_qu) < 20):
                sorted_data = tmp_ques_4.values.tolist()
                sorted_data.sort(key=lambda x:x[5], reverse=True)
                sim_qu.extend(sorted_data[:20])

            if (len(org_tgs) <= 5) & (len(tmp_ques_5) > 0) & (len(sim_qu) < 20):
                sorted_data = tmp_ques_5.values.tolist()
                sorted_data.sort(key=lambda x:x[6], reverse=True)
                sim_qu.extend(sorted_data[:20])

        else:
            sim_qu = tmp_ques
    else:
        sim_qu.sort(reverse=True, key = lambda x : x[-1])
        sim_qu = sim_qu[:20]

    # stop_1 = timeit.default_timer()
    # print('Time_1: ', stop_1 - start_1)  

    if len(sim_qu) > 0:
        subscription = []
        if ll == 0:
            with open('../../data/history/history_sem_sim_questions_pahse1.csv', 'a', newline='') as f_object:  
                writer_object = writer(f_object)
                writer_object.writerow(['original', 'similar', 'similarity'])
                f_object.close()
                ll = 1

        with open('../../data/history/history_sem_sim_questions_pahse1_full.csv', 'a', newline='') as f_object:  
            for i in sim_qu:
                i.insert(0, qu)
                writer_object = writer(f_object)
                writer_object.writerow(i)
            f_object.close()

        with open('../../data/history/history_sem_sim_questions_pahse1.csv', 'a', newline='') as f_object:  
            for i in sim_qu:
                # i.insert(0, qu)
                writer_object = writer(f_object)
                writer_object.writerow([i[0], i[1], i[-1]])
            f_object.close()
