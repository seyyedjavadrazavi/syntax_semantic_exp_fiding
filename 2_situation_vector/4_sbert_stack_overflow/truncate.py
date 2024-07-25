#https://neulearn.github.io/2020-08-16-bert/
#https://github.com/lanwuwei/BERTOverflow
#https://github.com/jeniyat/StackOverflowNER

from transformers import AutoTokenizer
import pandas as pd
import copy
from csv import writer
import re
from bs4 import BeautifulSoup
# import timeit
import csv
from bert_score import score
import torch
print(torch.cuda.is_available())
import os

posts = pd.read_xml(r'../../data/bioinformatics/Posts.xml')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']
questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]
idis = questions['Id'].values.tolist()

del questions

seman_tags = pd.read_csv(r'../../data/bioinformatics/w2v_CBOW.csv')
tg_names = seman_tags.columns.values.tolist()

tree = pd.read_csv(r'../../data/bioinformatics/bioinformatics_sim_questions_tree.csv')
tree.columns = ['qu_id', 'sim_ques_id', 'similarity', 'type_of_ques']

graph = pd.read_csv(r'../../data/bioinformatics/bioinformatics_sem_sim_questions.csv')
graph.columns = ['qu_id', 'sim_ques_id', 'similarity']

tokenizer = AutoTokenizer.from_pretrained('lanwuwei/BERTOverflow_stackoverflow_github', model_max_length=512)

def cleaner(input_text):
    if 'code' in input_text:
        input_text = input_text.replace('<code>', 'IN LINE CODE:').replace('</code>', '.').replace('&lt;', '').replace('&gt;', '')

    clean_txt = ''
    soup = BeautifulSoup(input_text, 'html.parser')
    clean_txt += soup.text

    clean = re.compile('<.*?>')

    input_text = re.sub(clean, ',', clean_txt)
    input_text = input_text.replace('\n', ' ').replace("""\"""", '').replace(',,', '').replace('///', '').replace('//', '')
    
    if input_text[0] == ',':
        input_text = input_text[1:]
    
    input_text = input_text.lstrip()
    input_text = input_text.rstrip()


    tok_txt = tokenizer(input_text, truncation=True)
    
    tok_txt = tok_txt.encodings[0].tokens[1:]
    if tok_txt[len(tok_txt)-1] == '[SEP]':
        tok_txt = tok_txt[:len(tok_txt)-1]
    output_txt = tokenizer.convert_tokens_to_string(tok_txt)

    return output_txt

start = idis.index(4205)
# end = idis.index(7161263)
idis = idis[start:]
ll = 1
os.environ['CURL_CA_BUNDLE'] = ''
for qu in idis:
    print('question id isssssssss: ', qu)

    qu_tree = tree.loc[tree['qu_id'] == qu]
    qu_tree = qu_tree.drop_duplicates(subset=['qu_id', 'sim_ques_id'])
    qu_graph = graph.loc[graph['qu_id'] == qu]
    qu_graph = qu_graph.drop_duplicates(subset=['qu_id', 'sim_ques_id'])
    
    commn_itms = list(set(qu_tree.sim_ques_id) & set(qu_graph.sim_ques_id))

    if len(commn_itms) != 0:
    
        cmmn_freq_itms = qu_tree.loc[qu_tree['sim_ques_id'].isin(commn_itms)] 
        cmmn_graph_itms = qu_graph.loc[qu_graph['sim_ques_id'].isin(commn_itms)] 
        
        res_sum = (cmmn_freq_itms['similarity'].values + cmmn_graph_itms['similarity'].values) / 2 # + cmmn_b_s_itms['similarity'].values[0]) / 3
        cmn_df = cmmn_graph_itms[['qu_id', 'sim_ques_id']]
        cmn_df['similarity'] = res_sum

        nt_cmmn_freq_itms = qu_tree.loc[~qu_tree['sim_ques_id'].isin(commn_itms)] 
        nt_cmmn_graph_itms = qu_graph.loc[~qu_graph['sim_ques_id'].isin(commn_itms)] 

        nt_cmmn_itms = pd.concat([nt_cmmn_freq_itms, nt_cmmn_graph_itms], ignore_index=True)

        nt_cmmn_itms['similarity'] = nt_cmmn_itms['similarity'] / 2

        itms = pd.concat([cmn_df, nt_cmmn_itms], ignore_index=True)
        itms.sort_values(by=['similarity'])
        cnd = itms[:30]
        cnd = cnd[['qu_id', 'sim_ques_id', 'similarity']]

    else:
        itms = pd.concat([qu_tree, qu_graph], ignore_index=True)
        itms['similarity'] = itms['similarity'] / 2
        itms.sort_values(by=['similarity'])
        cnd = itms[:30]
        cnd = cnd[['qu_id', 'sim_ques_id', 'similarity']]

    with open('../../data/bioinformatics/bioinformatics_union_tree_graph.csv', 'a', newline='') as f_object:              
        writer_object = writer(f_object)

        if ll == 0:
            writer_object.writerow(['qu_id', 'sim_ques_id', 'similarity'])
            ll = 1

        [writer_object.writerow(x) for x in cnd.values.tolist()]

        f_object.close()

    text_sim_ques = []
    id_sim_ques = []
    cnd_idis = cnd['sim_ques_id'].values.tolist()
    uncleaned_text_sim = posts.loc[posts['Id'].isin(cnd_idis), 'Body'].values.tolist()
    
    for ind in range(len(uncleaned_text_sim)):
        res = cleaner(uncleaned_text_sim[ind])
        if len(res) > 0:
            text_sim_ques.append(copy.deepcopy(res))
            id_sim_ques.append(copy.deepcopy(cnd_idis[ind]))
    

    crnt_txt = posts.loc[posts['Id'] == qu, 'Body'].values[0]
    crnt_txt = cleaner(crnt_txt)

################################# Bert Score
    p_score = []
    r_score = []
    f_score = []

    try:
        ques_txt = [crnt_txt] * len(text_sim_ques)
        P, R, F1 = score(text_sim_ques, ques_txt, lang="en", model_type = "lanwuwei/BERTOverflow_stackoverflow_github", num_layers = 10, device="cuda:0", nthreads=6, rescale_with_baseline=True, verbose=True)
    except:
        trnctd = []
        [trnctd.append(copy.deepcopy(x[:411])) for x in text_sim_ques]
        ques_txt = crnt_txt[:411]
        ques_txt = [crnt_txt] * len(trnctd)
        try:
            P, R, F1 = score(trnctd, ques_txt, lang="en", model_type = "lanwuwei/BERTOverflow_stackoverflow_github", num_layers = 10, device="cuda:0", nthreads=6, rescale_with_baseline=True, verbose=True)
        except:
            trnctd = []
            [trnctd.append(copy.deepcopy(x[:200])) for x in text_sim_ques]
            trnctd = trnctd[:20]
            ques_txt = crnt_txt[:250]
            ques_txt = [ques_txt] * len(trnctd)
            P, R, F1 = score(trnctd, ques_txt, lang="en", model_type = "lanwuwei/BERTOverflow_stackoverflow_github", num_layers = 10, device="cuda:0", nthreads=6, rescale_with_baseline=True, verbose=True)

    data = []   
    
    data = P.data
    sim_p = data.tolist()    
    p_score.extend(sim_p)

    data = R.data
    sim_R = data.tolist()
    r_score.extend(sim_R)
    
    data = F1.data
    sim_F1 = data.tolist()
    f_score.extend(sim_F1)

    with open('../../data/bioinformatics/bioinformatics_res_p_10_layers.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        for i in range(len(p_score)):
            writer_object.writerow([qu, id_sim_ques[i], p_score[i]])
        f_object.close()
    
    with open('../../data/bioinformatics/bioinformatics_res_R_10_layers.csv', 'a', newline='') as f_object:  
        writer_object = writer(f_object)
        for i in range(len(r_score)):
            writer_object.writerow([qu, id_sim_ques[i], r_score[i]])
        f_object.close()

    with open('../../data/bioinformatics/bioinformatics_res_F1_10_layers.csv', 'a', newline='') as f_object:  
        writer_object = writer(f_object)
        for i in range(len(f_score)):
            writer_object.writerow([qu, id_sim_ques[i], f_score[i]])
        f_object.close()






    # b_s_scr = []
    # for i in range(len(p_score)):
    #     b_s_scr.append(copy.deepcopy([qu, id_sim_ques[i], p_score[i]]))
    # b_s_itms = pd.DataFrame(b_s_scr, columns=['qu_id', 'sim_ques_id', 'similarity'])

    # commn_itms = list(set(cnd.sim_ques_id) & set(b_s_itms.sim_ques_id))

    # if len(commn_itms) != 0:
    #     cnd_itms = cnd.loc[cnd['sim_ques_id'].isin(commn_itms)] 
    #     cmmn_b_s_itms = b_s_itms.loc[b_s_itms['sim_ques_id'].isin(commn_itms)] 
        
    #     res_sum = (cnd_itms['similarity'].values + cmmn_b_s_itms['similarity'].values) / 2
    #     cmn_df = cmmn_b_s_itms[['qu_id', 'sim_ques_id']]
    #     cmn_df['similarity'] = res_sum

    #     nt_cmmn_freq_itms = cnd.loc[~cnd['sim_ques_id'].isin(commn_itms)] 
    #     cmmn_nt_b_s_itms = b_s_itms.loc[~b_s_itms['sim_ques_id'].isin(commn_itms)] 

    #     nt_cmmn_itms = pd.concat([nt_cmmn_freq_itms, cmmn_nt_b_s_itms], ignore_index=True)

    #     nt_cmmn_itms['similarity'] = nt_cmmn_itms['similarity'] / 2

    #     itms = pd.concat([cmn_df, nt_cmmn_itms], ignore_index=True)
    #     itms.sort_values(by=['similarity'])
    #     cnd = itms.iloc[:30]
    #     cnd = cnd[['qu_id', 'sim_ques_id', 'similarity']]

    # else:
    #     itms = pd.concat([cnd, b_s_itms], ignore_index=True)
    #     itms['similarity'] = itms['similarity'] / 2
    #     itms.sort_values(by=['similarity'])
    #     cnd = itms.iloc[:30]
    #     cnd = cnd[['qu_id', 'sim_ques_id', 'similarity']]