import pandas as pd
import copy

validate_data = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_validate_data.csv")
posts = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_Posts.csv")
abandoned_tasks_rate = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_candidate_result.csv")
deviation_from_community = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_usr_choise_result.csv")
req_profile = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_requester_expertise.csv")
task_difficaulity_subs = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_task_difficaulty_subs.csv")
task_difficaulity_ordr = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_task_difficaulty_ordering.csv")
worker_info = pd.read_csv(r"../../../data/bioinformatics/bioinformatics_worker_expertise.csv")

slcted_questions = [['Id', 'AcceptedAnswerId', 'OwnerUserId', 'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount']]

validate_data = validate_data.dropna(subset = ['OwnerUserId'])

comb_list = list()
for ques in validate_data.iterrows():
    ques = ques[1]
    print(ques['Id'])
    
    tsk_diffclty_subs = task_difficaulity_subs.loc[task_difficaulity_subs['id'] == ques['Id'], 'rep_avg']
    if len(tsk_diffclty_subs) > 0:
        tsk_diffclty_subs = tsk_diffclty_subs.values[0]
    else:
        tsk_diffclty_subs = -1

    tsk_diffclty_odrd = task_difficaulity_ordr.loc[task_difficaulity_ordr['id'] == ques['Id'], 'rep_avg']
    if len(tsk_diffclty_odrd) > 0:
        tsk_diffclty_odrd = tsk_diffclty_odrd.values[0]
    else:
        tsk_diffclty_odrd = -1

    ############### requester profile ##########################
    fair_aban = abandoned_tasks_rate.loc[abandoned_tasks_rate['UserId'] == ques['OwnerUserId'], 'percentage'].values[0]
    fair_comm = deviation_from_community.loc[deviation_from_community['UserId'] == ques['OwnerUserId'], 'changed_prcnt'].values[0]
    req_rep = req_profile.loc[req_profile['user_id'] == ques['OwnerUserId'], 'reputation'].values[0]
    re_exprtis = req_profile.loc[req_profile['user_id'] == ques['OwnerUserId'], 'expertise'].values[0]
    
    ############### worker profile ##########################
    # print(ques['Id'])
    item = posts.loc[posts['ParentId'] == ques['Id']]
    answr_tt = worker_info.loc[worker_info['user_id'].isin(item['OwnerUserId'].values.tolist()), ['user_id', 'reputation']]
    answr_tt['Id'] = item['Id']
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
    combine['tsk_difficlty_subs'] = tsk_diffclty_subs
    combine['tsk_difficlty_ordring'] = tsk_diffclty_odrd
    combine['difclt_rep_diff_subs'] = req_rep - tsk_diffclty_subs
    combine['difclt_rep_diff_ordring'] = req_rep - tsk_diffclty_odrd

    combine = combine[['ques_id', 'user_id', 'fair_aban', 'fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty_subs', 'tsk_difficlty_ordring', 'difclt_rep_diff_subs', 'difclt_rep_diff_ordring', 'wrkr_rep', 'wrkr_exprtis', 'label']]

    comb_list.extend(combine.values.tolist())

res = pd.DataFrame(comb_list, columns=['ques_id', 'wrkr_id', 'req_fair_aban', 'req_fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty_subscrp', 'tsk_difficlty_ordering', 'difclt_rep_diff_subscrp', 'difclt_rep_diff_ordring', 'wrkr_rep', 'wrkr_exprtis', 'label'])
res.to_csv('../../../data/bioinformatics/bioinformatics_validate_data_combination.csv', index=False)