import pandas as pd
from csv import writer 

test_data = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_test_data.csv")
posts = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_Posts.csv")
abandoned_tasks_rate = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_candidate_result.csv")
deviation_from_community = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_usr_choise_result.csv")
req_profile = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_requester_expertise.csv")
task_difficaulity_subs = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_task_difficaulty_subs.csv")
task_difficaulity_ordr = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_task_difficaulty_ordering.csv")
worker_info = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_worker_expertise.csv")

slcted_questions = [['Id', 'AcceptedAnswerId', 'OwnerUserId', 'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount']]

test_data = test_data.loc[~test_data['AcceptedAnswerId'].isnull()]

ll = 0
for ques in test_data.iterrows():
    comb_list = list()
    ques = ques[1]
    print(ques['Id'])

    tsk_diffclty_subs = task_difficaulity_subs.loc[task_difficaulity_subs['id'] == ques['Id'], 'rep_avg'].values[0]
    tsk_diffclty_odrd = task_difficaulity_ordr.loc[task_difficaulity_ordr['id'] == ques['Id'], 'rep_avg'].values[0]

    ############### requester profile ##########################
    OwnerId = posts.loc[posts['Id'] == ques['Id'], 'OwnerUserId'].values[0]
    if str(OwnerId) == 'nan':
        continue
    fair_aban = abandoned_tasks_rate.loc[abandoned_tasks_rate['UserId'] == OwnerId, 'percentage'].values[0]
    fair_comm = deviation_from_community.loc[deviation_from_community['UserId'] == OwnerId, 'changed_prcnt'].values[0]
    req_rep = req_profile.loc[req_profile['user_id'] == OwnerId, 'reputation'].values
    if len(req_rep) > 0:
        req_rep = req_rep[0]
    else:
        continue

    re_exprtis = req_profile.loc[req_profile['user_id'] == OwnerId, 'expertise'].values[0]
    
    ############### worker profile ##########################
    # print(ques['Id'])
    item = posts.loc[posts['ParentId'] == ques['Id']]
    wrkr_rep = pd.merge(item, worker_info, left_on = 'OwnerUserId', right_on = 'user_id', how = 'inner')
    wrkr_rep = wrkr_rep[['user_id', 'Id', 'reputation']]
    wrkr_rep.rename(columns = {'reputation':'wrkr_rep'}, inplace = True)

    wrkr_exprtis = pd.merge(item, worker_info, left_on = 'OwnerUserId', right_on = 'user_id', how = 'inner')

    ############### set label ################################
    wrkr_rep['label'] = 0
    wrkr_rep.loc[wrkr_rep['Id'] == ques['AcceptedAnswerId'], 'label'] = 1

    wrkr_rep_exprtis = wrkr_rep[['user_id', 'wrkr_rep', 'label']]
    wrkr_rep_exprtis = wrkr_rep_exprtis.loc[wrkr_rep_exprtis['user_id'].isin(wrkr_exprtis['user_id'].values.tolist())]
    wrkr_rep_exprtis['wrkr_exprtis'] = wrkr_exprtis['expertise'].values

    ############## combine two dataframes #####################
    combine = wrkr_rep_exprtis
    combine['fair_aban'] = fair_aban
    combine['fair_comm'] = fair_comm
    combine['req_rep'] = req_rep
    combine['req_exprtis'] = re_exprtis
    combine['ques_id'] = ques['Id']
    # combine['sim_qu_id'] = sm_qu
    combine['tsk_difficlty_subs'] = tsk_diffclty_subs
    combine['tsk_difficlty_ordring'] = tsk_diffclty_odrd
    combine['difclt_rep_diff_subs'] = req_rep - tsk_diffclty_subs
    combine['difclt_rep_diff_ordring'] = req_rep - tsk_diffclty_odrd

    combine = combine[['ques_id', 'user_id', 'fair_aban', 'fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty_subs', 'tsk_difficlty_ordring', 'difclt_rep_diff_subs', 'difclt_rep_diff_ordring', 'wrkr_rep', 'wrkr_exprtis', 'label']]

    # print(len(combine))
    if len(combine) > 0:
        comb_list.extend(combine.values.tolist())
        
    if len(comb_list) > 0:
        with open('../../../data/bioinformatics/bioinformatics_test_data_combination.csv', 'a', newline='') as f_object:
            writer_object = writer(f_object)
            if ll == 0:
                writer_object.writerow(['ques_id', 'wrkr_id', 'req_fair_aban', 'req_fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty_subscrp', 'tsk_difficlty_ordering', 'difclt_rep_diff_subscrp', 'difclt_rep_diff_ordring', 'wrkr_rep', 'wrkr_exprtis', 'label'])
                ll = 1
    
            [writer_object.writerow(x) for x in comb_list]
            f_object.close()













############################# phase 1




# test_data = test_data.dropna(subset = ['qu_id', 'sim_qu_id'])
# ques_idis = test_data.drop_duplicates(subset=['qu_id'])
# # print(len(ques_idis))

# ll = 0
# for ques in ques_idis.iterrows():
#     comb_list = list()
#     ques = ques[1]
#     print(ques['qu_id'])

#     tsk_diffclty = task_difficaulity.loc[task_difficaulity['id'] == ques['qu_id'], 'rep_avg'].values[0]

#     ############### requester profile ##########################
#     OwnerId = posts.loc[posts['Id'] == ques['qu_id'], 'OwnerUserId'].values[0]
#     if str(OwnerId) == 'nan':
#         continue
#     fair_aban = abandoned_tasks_rate.loc[abandoned_tasks_rate['UserId'] == OwnerId, 'percentage'].values[0]
#     fair_comm = deviation_from_community.loc[deviation_from_community['UserId'] == OwnerId, 'changed_prcnt'].values[0]
#     req_rep = req_profile.loc[req_profile['user_id'] == OwnerId, 'reputation'].values[0]
#     re_exprtis = req_profile.loc[req_profile['user_id'] == OwnerId, 'expertise'].values[0]
    
#     ############### worker profile ##########################
#     # print(ques['qu_id'])
#     sim_ques = test_data.loc[test_data['qu_id'] == int(ques['qu_id']), 'sim_qu_id'].values.tolist()
#     sim_ques = posts.loc[posts['Id'].isin(sim_ques) & (~posts['AcceptedAnswerId'].isnull()), 'Id'].values.tolist()
#     for sm_qu in sim_ques:
#         acan_id = posts.loc[(posts['Id'] == int(sm_qu)) & (~posts['AcceptedAnswerId'].isnull()), 'AcceptedAnswerId']
#         if len(acan_id) == 0:
#             continue
#         else:
#             acan_id = acan_id.values[0]

#         item = posts.loc[posts['Id'] == acan_id]
#         wrkr_rep = pd.merge(item, worker_info, left_on = 'OwnerUserId', right_on = 'user_id', how = 'inner')
#         wrkr_rep = wrkr_rep[['user_id', 'Id', 'reputation']]
#         wrkr_rep.rename(columns = {'reputation':'wrkr_rep'}, inplace = True)

#         wrkr_exprtis = pd.merge(item, worker_info, left_on = 'OwnerUserId', right_on = 'user_id', how = 'inner')

#         ############### set label ################################
#         wrkr_rep['label'] = 1
#         # wrkr_rep.loc[wrkr_rep['Id'] == ques['AcceptedAnswerId'], 'label'] = 1

#         wrkr_rep_exprtis = wrkr_rep[['user_id', 'wrkr_rep', 'label']]
#         wrkr_rep_exprtis = wrkr_rep_exprtis.loc[wrkr_rep_exprtis['user_id'].isin(wrkr_exprtis['user_id'].values.tolist())]
#         wrkr_rep_exprtis['wrkr_exprtis'] = wrkr_exprtis['expertise'].values

#         ############## combine two dataframes #####################
#         combine = wrkr_rep_exprtis
#         combine['fair_aban'] = fair_aban
#         combine['fair_comm'] = fair_comm
#         combine['req_rep'] = req_rep
#         combine['req_exprtis'] = re_exprtis
#         combine['ques_id'] = ques['qu_id']
#         combine['sim_qu_id'] = sm_qu
#         combine['tsk_difficlty'] = tsk_diffclty
#         combine['difclt_rep_diff'] = combine['req_rep'] - combine['tsk_difficlty']

#         combine = combine[['ques_id', 'user_id', 'sim_qu_id', 'fair_aban', 'fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty', 'difclt_rep_diff', 'wrkr_rep', 'wrkr_exprtis', 'label']]

#         # print(len(combine))
#         if len(combine) > 0:
#             comb_list.extend(combine.values.tolist())
        
#     if len(comb_list) > 0:
#         with open('../../../data/ai/ai_test_data_combination.csv', 'a', newline='') as f_object:
#             writer_object = writer(f_object)
#             if ll == 0:
#                 writer_object.writerow(['ques_id', 'wrkr_id', 'sim_qu_id', 'req_fair_aban', 'req_fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty', 'difclt_rep_diff', 'wrkr_rep', 'wrkr_exprtis', 'label'])
#                 ll = 1

#             [writer_object.writerow(x) for x in comb_list]
#             f_object.close()

# res = pd.DataFrame(ai, aiolumns=['ques_id', 'wrkr_id', 'req_fair_aban', 'req_fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty', 'difclt_rep_diff', 'wrkr_rep', 'wrkr_exprtis', 'label'])
# res.to_csv('../../../data/ai/ai_test_data_combination.csv', index=False)
