#https://neulearn.github.io/2020-08-16-bert/
#https://github.com/lanwuwei/BERTOverflow
#https://github.com/jeniyat/StackOverflowNER

from transformers import AutoTokenizer
import pandas as pd
import copy
import re
from bs4 import BeautifulSoup
from bert_score import score
import torch
print(torch.cuda.is_available())
import os

posts = pd.read_xml(r'../data/bioinformatics/Posts.xml')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']
questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]
idis = questions['Id'].values.tolist()

del questions

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

os.environ['CURL_CA_BUNDLE'] = ''
def bert_Score(wrkr_id, orgnal_ques, orgnal_id):
    answrs_prnt_id = posts.loc[(posts['OwnerUserId'] == wrkr_id) & (posts['PostTypeId'] == 2) & (~posts['ParentId'].isnull()), 'ParentId'].values.tolist()
    if (orgnal_id in answrs_prnt_id) and (len(answrs_prnt_id) > 1):
        answrs_prnt_id.remove(orgnal_id)
    answrs_prnt = posts.loc[(posts['Id'].isin(answrs_prnt_id)), 'Body'].values.tolist()

    text_sim_ques = []
    for ind in range(len(answrs_prnt)):
        res = cleaner(answrs_prnt[ind])
        if len(res) > 0:
            text_sim_ques.append(copy.deepcopy(res))
    

    crnt_txt = posts.loc[posts['Id'] == orgnal_ques, 'Body'].values[0]
    crnt_txt = cleaner(crnt_txt)

    ################################# Bert Score
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
            [trnctd.append(copy.deepcopy(x[:300])) for x in text_sim_ques]
            trnctd = trnctd[:20]
            ques_txt = crnt_txt[:300]
            ques_txt = [ques_txt] * len(trnctd)
            P, R, F1 = score(trnctd, ques_txt, lang="en", model_type = "lanwuwei/BERTOverflow_stackoverflow_github", num_layers = 10, device="cuda:0", nthreads=6, rescale_with_baseline=True, verbose=True)

    data = []
    data = P.data
    sim_p = data.tolist()    

    data = R.data
    sim_R = data.tolist()
    
    data = F1.data
    sim_F1 = data.tolist()
    
    return sum(sim_p)/len(sim_p)#, sum(sim_R)/len(sim_R), sum(sim_F1)/len(sim_F1)