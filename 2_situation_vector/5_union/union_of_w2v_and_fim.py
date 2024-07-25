import pandas as pd
from csv import writer

posts = pd.read_csv('../../data/bioinformatics/bioinformatics_Posts.csv')

posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']
questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull()), 'Id'].values.tolist()
del posts

b_s = pd.read_csv('../../data/bioinformatics/bioinformatics_res_F1_10_layers.csv')
b_s.columns = ['qu_id', 'sim_ques_id', 'similarity']

w2v = pd.read_csv('../../data/bioinformatics/bioinformatics_sem_sim_questions.csv')
w2v.columns = ['qu_id', 'sim_ques_id', 'similarity']

fim = pd.read_csv('../../data/bioinformatics/bioinformatics_sim_questions_tree.csv')
fim.columns = ['qu_id', 'sim_ques_id', 'similarity', 'relation']

ll = 0
for qu_id in questions:
    print('The id isssssssssssssssss: ',qu_id)
    cnd = []
    
    qu_fim = fim.loc[fim['qu_id'] == qu_id]
    qu_fim = qu_fim.drop_duplicates(subset=['qu_id', 'sim_ques_id'])

    qu_w2v = w2v.loc[w2v['qu_id'] == qu_id]
    qu_w2v = qu_w2v.drop_duplicates(subset=['qu_id', 'sim_ques_id'])
    qu_w2v.fillna(-111, inplace=True)
    
    b_s_itms = b_s.loc[b_s['qu_id'] == qu_id]
    b_s_itms = b_s_itms.drop_duplicates(subset=['qu_id', 'sim_ques_id'])

##################### Subscription
    commn_itms = list(set(qu_fim.sim_ques_id) & set(qu_w2v.sim_ques_id) & set(b_s_itms.sim_ques_id))

    if len(commn_itms) != 0:
    
        cmmn_freq_itms = qu_fim.loc[qu_fim['sim_ques_id'].isin(commn_itms)] 
        cmmn_w2v_itms = qu_w2v.loc[qu_w2v['sim_ques_id'].isin(commn_itms)] 
        cmmn_b_s_itms = b_s_itms.loc[b_s_itms['sim_ques_id'].isin(commn_itms)] 
        
        res_sum = (cmmn_freq_itms['similarity'].values[0] + cmmn_w2v_itms['similarity'].values[0] + cmmn_b_s_itms['similarity'].values[0]) / 3
        cmn_df = cmmn_w2v_itms[['qu_id', 'sim_ques_id']]
        cmn_df['similarity'] = res_sum

        nt_cmmn_freq_itms = qu_fim.loc[~qu_fim['sim_ques_id'].isin(commn_itms)] 
        nt_cmmn_w2v_itms = qu_w2v.loc[~qu_w2v['sim_ques_id'].isin(commn_itms)] 
        nt_cmmn_b_s_itms = b_s_itms.loc[~b_s_itms['sim_ques_id'].isin(commn_itms)]

        nt_cmmn_itms = pd.concat([nt_cmmn_freq_itms, nt_cmmn_w2v_itms, nt_cmmn_b_s_itms], ignore_index=True)

        nt_cmmn_itms['similarity'] = nt_cmmn_itms['similarity'] / 3
        nt_cmmn_itms.sort_values(by=['similarity'])
        nt_cmmn_itms = nt_cmmn_itms.iloc[:(30 - len(cmn_df))]

        if len(nt_cmmn_itms) > 0:
            itms = pd.concat([cmn_df, nt_cmmn_itms], ignore_index=True)
        
        cnd = itms.iloc[:30]
        cnd = cnd[['qu_id', 'sim_ques_id', 'similarity']]

    else:
        itms = pd.concat([qu_fim, qu_w2v, b_s_itms], ignore_index=True)
        itms['similarity'] = itms['similarity'] / 3
        itms.sort_values(by=['similarity'])
        cnd = itms.iloc[:30]
        cnd = cnd[['qu_id', 'sim_ques_id', 'similarity']]

    cnd = cnd.values.tolist()
    with open('../../data/bioinformatics/bioinformatics_avg_scores_subscription.csv', 'a', newline='') as f_object:              
        writer_object = writer(f_object)

        if ll == 0:
            writer_object.writerow(['qu_id', 'sim_ques_id', 'score'])
            ll = 1

        [writer_object.writerow(x) for x in cnd]
        
        f_object.close()

##################### Ordering

    itms = pd.concat([qu_fim, qu_w2v, b_s_itms], ignore_index=True)
    itms['similarity'] = itms['similarity'] / 3
    itms = itms.sort_values(by=['similarity'], ascending = False)
    cnd = itms.iloc[:30]
    cnd = cnd[['qu_id', 'sim_ques_id', 'similarity']]

    cnd = cnd.values.tolist()

    with open('../../data/bioinformatics/bioinformatics_avg_scores_by_order.csv', 'a', newline='') as f_object:              
        writer_object = writer(f_object)

        if ll == 0:
            writer_object.writerow(['qu_id', 'sim_ques_id', 'score'])
            ll = 1

        [writer_object.writerow(x) for x in cnd]
        
        f_object.close()
