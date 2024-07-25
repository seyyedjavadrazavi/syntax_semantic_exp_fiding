import pandas as pd
import copy
from csv import writer
import itertools

#'same' = 1
#'children' = 2
#'siblings' = 3
# 'parent' = 4

idis = []
posts = pd.read_xml(r'../../data/bioinformatics/Posts.xml')
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']

questions = posts.loc[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]
answers = posts.loc[(posts['PostTypeId'] == 2) & (~posts['OwnerUserId'].isnull())]
del posts

idis = questions['Id'].values.tolist()

tag_obs_len1 = pd.read_csv(r'../../data/bioinformatics/bioinformatics_tags_observation_len1.csv')
tag_obs_len2 = pd.read_csv(r'../../data/bioinformatics/bioinformatics_tags_observation_len2.csv')
tag_obs_len3 = pd.read_csv(r'../../data/bioinformatics/bioinformatics_tags_observation_len3.csv')
tag_obs_len4 = pd.read_csv(r'../../data/bioinformatics/bioinformatics_tags_observation_len4.csv')
tag_obs_len5 = pd.read_csv(r'../../data/bioinformatics/bioinformatics_tags_observation_len5.csv')

# seman_tags = pd.read_csv(r'../../data/ai/w2v_CBOW.csv')
# tg_names = seman_tags.columns.values.tolist()

####################### Start

def remove_duplicates(input_tags):
    seen = {}
    result = []
    for sublist in input_tags:
        key = (sublist[0], sublist[1])
        if key not in seen:
            seen[key] = True
            result.append(copy.deepcopy(sublist))

    return result

def findsubsets(bag, n):
        if n == 1:
            h = 1
        else:
        
            set_bag = set(bag)
            sub = itertools.combinations(set_bag, n)
            sub = [list(x) for x in sub]
    
            [x.sort() for x in sub]
    
            cnt = 0
            for i in sub:
                if n == 1:
                    qu_bag = tag_obs_len1.loc[tag_obs_len1['tag1'] == i, 'ques_id']
                elif n == 2:
                    qu_bag = tag_obs_len2[(tag_obs_len2['tag1'] == i[0]) & (tag_obs_len2['tag2'] == i[1])]
                elif n == 3:
                    qu_bag = tag_obs_len3[(tag_obs_len3['tag1'] == i[0]) & (tag_obs_len3['tag2'] == i[1]) & (tag_obs_len3['tag3'] == i[2])]
                elif n == 4:
                    qu_bag = tag_obs_len4[(tag_obs_len4['tag1'] == i[0]) & (tag_obs_len4['tag2'] == i[1]) & (tag_obs_len4['tag3'] == i[2]) & (tag_obs_len4['tag4'] == i[3])]
                elif n == 5:
                    qu_bag = tag_obs_len5[(tag_obs_len5['tag1'] == i[0]) & (tag_obs_len5['tag2'] == i[1]) & (tag_obs_len5['tag3'] == i[2]) & (tag_obs_len5['tag4'] == i[3]) & (tag_obs_len5['tag5'] == i[4])]
                # elif n == 6:
                #     qu_bag = tag_obs_len6[(tag_obs_len6['tag1'] == i[0]) & (tag_obs_len6['tag2'] == i[1]) & (tag_obs_len6['tag3'] == i[2])   & (tag_obs_len6['tag4'] == i[3]) & (tag_obs_len6['tag5'] == i[4]) & (tag_obs_len6['tag6'] == i[5])]
    
    
                if len(qu_bag) > 0:
                    cnt += 1
                    h = 1 + findsubsets(bag, n-1)
                    break
                
            if cnt == 0:
                h = 1 + findsubsets(bag, n-1)
    
        return h
    
def sibilngs(bag, n):
    if n == 0:
        return []
    sib = []

    if n == 1:
        qu_bag = tag_obs_len1[(tag_obs_len1['tag1'].isin(bag))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
    if n == 2:
        qu_bag = tag_obs_len2[(tag_obs_len2['tag1'].isin(bag)) | ((tag_obs_len2['tag2'].isin(bag)))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [sib.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]
    if n == 3:
        qu_bag = tag_obs_len3[((tag_obs_len3['tag1'].isin(bag)) & (tag_obs_len3['tag2'].isin(bag))) | ((tag_obs_len3['tag1'].isin(bag)) & (tag_obs_len3['tag3'].isin(bag))) | (tag_obs_len3['tag2'].isin(bag)) & (tag_obs_len3['tag3'].isin(bag))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [sib.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]
    if n == 4:
        qu_bag = tag_obs_len4[((tag_obs_len4['tag1'].isin(bag)) & (tag_obs_len4['tag2'].isin(bag)) & (tag_obs_len4['tag3'].isin(bag))) | ((tag_obs_len4['tag1'].isin(bag)) & (tag_obs_len4['tag2'].isin(bag)) & (tag_obs_len4['tag4'].isin(bag))) |
        ((tag_obs_len4['tag1'].isin(bag)) & (tag_obs_len4['tag3'].isin(bag)) & (tag_obs_len4['tag4'].isin(bag))) | ((tag_obs_len4['tag2'].isin(bag)) & (tag_obs_len4['tag3'].isin(bag)) & (tag_obs_len4['tag4'].isin(bag)))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [sib.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]
    if n == 5:
        qu_bag = tag_obs_len5[((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag))) |
        ((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag))) | 
        ((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag))) |
        ((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag))) |
        ((tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag)))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [sib.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]

    return sib
    
def children(bag):
    n = len(bag)
    kids = []

    if n == 1:
        qu_bag = tag_obs_len2[(tag_obs_len2['tag1'].isin(bag)) | ((tag_obs_len2['tag2'].isin(bag)))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [kids.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]
    if n == 2:
        qu_bag = tag_obs_len3[((tag_obs_len3['tag1'].isin(bag)) & (tag_obs_len3['tag2'].isin(bag))) | ((tag_obs_len3['tag1'].isin(bag)) & (tag_obs_len3['tag3'].isin(bag))) | (tag_obs_len3['tag2'].isin(bag)) & (tag_obs_len3['tag3'].isin(bag))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [kids.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]
    if n == 3:
        qu_bag = tag_obs_len4[((tag_obs_len4['tag1'].isin(bag)) & (tag_obs_len4['tag2'].isin(bag)) & (tag_obs_len4['tag3'].isin(bag))) | ((tag_obs_len4['tag1'].isin(bag)) & (tag_obs_len4['tag2'].isin(bag)) & (tag_obs_len4['tag4'].isin(bag))) |
        ((tag_obs_len4['tag1'].isin(bag)) & (tag_obs_len4['tag3'].isin(bag)) & (tag_obs_len4['tag4'].isin(bag))) | ((tag_obs_len4['tag2'].isin(bag)) & (tag_obs_len4['tag3'].isin(bag)) & (tag_obs_len4['tag4'].isin(bag)))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [kids.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]
    if n == 4:
        qu_bag = tag_obs_len5[((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag))) |
        ((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag))) | 
        ((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag))) |
        ((tag_obs_len5['tag1'].isin(bag)) & (tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag))) |
        ((tag_obs_len5['tag2'].isin(bag)) & (tag_obs_len5['tag3'].isin(bag)) & (tag_obs_len5['tag4'].isin(bag)) & (tag_obs_len5['tag5'].isin(bag)))]
        qu_bag = qu_bag.iloc[:, 1:2].values.tolist()
        [kids.append(copy.deepcopy(x[0])) for x in qu_bag if len(qu_bag) > 0]

    return kids
     
def parent(bag, n):
    set_bag = set(bag)
    if n - 1 <= 0:
        sub = list(itertools.combinations(set_bag, 1))
    else:
        sub = list(itertools.combinations(set_bag, n))
    itm = []
    for x in sub:
        cc = 0
        for y in x:
            if len(x) == 1:
                itm.append(copy.deepcopy((y)))
                cc = 1
        if cc == 0:
            itm.append(copy.deepcopy((list(x))))
            
    if type(itm[0]) == type(itm):
        size = len(itm[0])
    elif type(itm[0]) == type('string'): 
        size = 1

    sib = []
    qu_bag = []
    if n < -10:
        for tg_set in itm:
            if size == 1:
                qu_bag1 = tag_obs_len1.loc[tag_obs_len1['tag1'] == tg_set].values.tolist()
                qu_bag1 = [x[1] for x in qu_bag1]
                qu_bag.extend(list(set(qu_bag1)))
                tg_set = [tg_set]
            if (len(qu_bag) < 10) & (size < 2):
                qu_bag2 = tag_obs_len2[(tag_obs_len2['tag1'].isin(tg_set)) | (tag_obs_len2['tag2'].isin(tg_set))].values.tolist()
                qu_bag2 = [x[1] for x in qu_bag2]
                qu_bag.extend(list(set(qu_bag2)))
            if (len(qu_bag) < 10) & (size < 3):
                qu_bag3 = tag_obs_len3[(tag_obs_len3['tag1'].isin(tg_set)) | (tag_obs_len3['tag2'].isin(tg_set)) | (tag_obs_len3['tag3'].isin(tg_set))].values.tolist()
                qu_bag3 = [x[1] for x in qu_bag3]
                qu_bag.extend(list(set(qu_bag3)))
            if (len(qu_bag) < 10) & (size < 4):
                qu_bag4 = tag_obs_len4[(tag_obs_len4['tag1'].isin(tg_set)) | (tag_obs_len4['tag2'].isin(tg_set)) | (tag_obs_len4['tag3'].isin(tg_set)) | (tag_obs_len4['tag4'].isin(tg_set))].values.tolist()
                qu_bag4 = [x[1] for x in qu_bag4]
                qu_bag.extend(list(set(qu_bag4)))
            if (len(qu_bag) < 10) & (size < 5):
                qu_bag5 = tag_obs_len5[(tag_obs_len5['tag1'].isin(tg_set)) | (tag_obs_len5['tag2'].isin(tg_set)) | (tag_obs_len5['tag3'].isin(tg_set)) | (tag_obs_len5['tag4'].isin(tg_set)) | (tag_obs_len5['tag5'].isin(tg_set))].values.tolist()
                qu_bag5 = [x[1] for x in qu_bag5]
                qu_bag.extend(list(set(qu_bag5)))
                
            sib.extend(qu_bag)
        
    else:
        for tg_set in itm:
            if size == 1:
                qu_bag = []
                tmp_1 = tag_obs_len1.loc[tag_obs_len1['tag1'] == tg_set]
                tg_set = [tg_set]
                tmp_2 = tag_obs_len2[(tag_obs_len2['tag1'].isin(tg_set)) | (tag_obs_len2['tag2'].isin(tg_set))]
                tmp_3 = tag_obs_len3[(tag_obs_len3['tag1'].isin(tg_set)) | (tag_obs_len3['tag2'].isin(tg_set)) & (tag_obs_len3['tag3'].isin(tg_set))]
                tmp_4 = tag_obs_len4[(tag_obs_len4['tag1'].isin(tg_set)) | (tag_obs_len4['tag2'].isin(tg_set)) & (tag_obs_len4['tag3'].isin(tg_set)) & (tag_obs_len4['tag4'].isin(tg_set))]
                tmp_5 = tag_obs_len5[(tag_obs_len5['tag1'].isin(tg_set)) | (tag_obs_len5['tag2'].isin(tg_set)) & (tag_obs_len5['tag3'].isin(tg_set)) & (tag_obs_len5['tag4'].isin(tg_set)) & (tag_obs_len5['tag5'].isin(tg_set))]
                if len(tmp_1) > 0:
                    qu_bag.extend(tmp_1['ques_id'].values.tolist())
                if len(tmp_2) > 0:
                    qu_bag.extend(tmp_2['ques_id'].values.tolist())
                if len(tmp_3) > 0:
                    qu_bag.extend(tmp_3['ques_id'].values.tolist())
                if len(tmp_4) > 0:
                    qu_bag.extend(tmp_4['ques_id'].values.tolist())
                if len(tmp_5) > 0:
                    qu_bag.extend(tmp_5['ques_id'].values.tolist())

            if size == 2:
                qu_bag = tag_obs_len2[(tag_obs_len2['tag1'].isin(tg_set)) & (tag_obs_len2['tag2'].isin(tg_set))]
            if size == 3:
                qu_bag = tag_obs_len3[(tag_obs_len3['tag1'].isin(tg_set)) & (tag_obs_len3['tag2'].isin(tg_set)) & (tag_obs_len3['tag3'].isin(tg_set))]
            if size == 4:
                qu_bag = tag_obs_len4[(tag_obs_len4['tag1'].isin(tg_set)) & (tag_obs_len4['tag2'].isin(tg_set)) & (tag_obs_len4['tag3'].isin(tg_set)) & (tag_obs_len4['tag4'].isin(tg_set))]
            if size == 5:
                qu_bag = tag_obs_len5[(tag_obs_len5['tag1'].isin(tg_set)) & (tag_obs_len5['tag2'].isin(tg_set)) & (tag_obs_len5['tag3'].isin(tg_set)) & (tag_obs_len5['tag4'].isin(tg_set)) & (tag_obs_len5['tag5'].isin(tg_set))]
            # elif size == 6:
            #     qu_bag = tag_obs_len6[(tag_obs_len6['tag1'] == tg_set) & (tag_obs_len6['tag2'] == tg_set) & (tag_obs_len6['tag3'] == tg_set)   & (tag_obs_len6['tag4'] == tg_set) & (tag_obs_len6['tag5'] == tg_set) & (tag_obs_len6['tag6'] == tg_set)]
            
            if size != 1:
                qu_bag = qu_bag.iloc[:, 1:2].values.tolist()

                if len(qu_bag) > 0:
                    if len(qu_bag) > 1:
                        try:
                            [sib.extend(x[0]) for x in qu_bag]
                        except:
                            [sib.extend(x) for x in qu_bag]
                    # else:
                    #     try:
                    #         sib.append(copy.deepcopy(qu_bag[0][0]))
                    #     except:
                    #         sib.append(copy.deepcopy(qu_bag[0]))
            else:
                if len(qu_bag) > 0:
                    sib.extend(qu_bag)

    return sib

# start = idis.index(81)
# end = idis.index(7161263)
# idis = idis[start:]
    
for qu in idis:
    print(qu)
    crnt_tgs = []
    tree_tags = []
    sim_qu = []
    tags_size = 0
    crnt_tgs_l1 = tag_obs_len1.loc[tag_obs_len1['ques_id'] == qu]
    crnt_tgs_l2 = tag_obs_len2.loc[tag_obs_len2['ques_id'] == qu]
    crnt_tgs_l3 = tag_obs_len3.loc[tag_obs_len3['ques_id'] == qu]
    crnt_tgs_l4 = tag_obs_len4.loc[tag_obs_len4['ques_id'] == qu]
    crnt_tgs_l5 = tag_obs_len5.loc[tag_obs_len5['ques_id'] == qu]

    if len(crnt_tgs_l1) != 0:
        crnt_tgs = crnt_tgs_l1.iloc[:, 2:].values[0].tolist()
        qu_bag = tag_obs_len1.iloc[:, 1].values.tolist()       
        tags_size = 1            
    elif len(crnt_tgs_l2) != 0:
        crnt_tgs = crnt_tgs_l2.iloc[:, 2:].values[0].tolist()
        qu_bag = tag_obs_len2[(tag_obs_len2['tag1'].isin(crnt_tgs)) & (tag_obs_len2['tag2'].isin(crnt_tgs))]
        tags_size = 2
    elif len(crnt_tgs_l3) != 0:
        crnt_tgs = crnt_tgs_l3.iloc[:, 2:].values[0].tolist()
        qu_bag = tag_obs_len3[(tag_obs_len3['tag1'].isin(crnt_tgs)) & (tag_obs_len3['tag2'].isin(crnt_tgs)) & (tag_obs_len3['tag3'].isin(crnt_tgs))]
        tags_size = 3
    elif len(crnt_tgs_l4) != 0:
        crnt_tgs = crnt_tgs_l4.iloc[:, 2:].values[0].tolist()
        qu_bag = tag_obs_len4[(tag_obs_len4['tag1'].isin(crnt_tgs)) & (tag_obs_len4['tag2'].isin(crnt_tgs)) & (tag_obs_len4['tag3'].isin(crnt_tgs)) & (tag_obs_len4['tag4'].isin(crnt_tgs))]
        tags_size = 4
    elif len(crnt_tgs_l5) != 0:
        crnt_tgs = crnt_tgs_l5.iloc[:, 2:].values[0].tolist()
        qu_bag = tag_obs_len5[(tag_obs_len5['tag1'].isin(crnt_tgs)) & (tag_obs_len5['tag2'].isin(crnt_tgs)) & (tag_obs_len5['tag3'].isin(crnt_tgs)) & (tag_obs_len5['tag4'].isin(crnt_tgs)) & (tag_obs_len5['tag5'].isin(crnt_tgs))]
        tags_size = 5
    
    if tags_size == 0:
        continue
    
    crnt_tgs = [str(x) for x in crnt_tgs]

    if tags_size == 1:
        [tree_tags.append(copy.deepcopy([qu, x, 1, 1])) for x in qu_bag]
    else:
        h = findsubsets(crnt_tgs, len(crnt_tgs))

    crnt_ans = 30
    tree_tags = remove_duplicates(tree_tags)
    if len(tree_tags) >= crnt_ans:
        a = 1
    else:
        h_parent = 0
        if qu == 26:
            qweqwe = -1
        while len(tree_tags) < crnt_ans:
            #################################################### Children
            childs = children(crnt_tgs)
            [tree_tags.append(copy.deepcopy([qu, x, 1, 2])) for x in childs]

            tree_tags = remove_duplicates(tree_tags)
            if len(tree_tags) >= crnt_ans:
                break

            #################################################### Sibilngs
            sib = sibilngs(crnt_tgs, len(crnt_tgs) - h_parent)
            if h - h_parent <= 0:
                [tree_tags.append(copy.deepcopy([qu, x, -1, 2])) for x in sib]
            else:
                [tree_tags.append(copy.deepcopy([qu, x, (1-(1/(h - h_parent))), 2])) for x in sib]
                
            tree_tags = remove_duplicates(tree_tags)    
            if len(tree_tags) >= crnt_ans:
                break

            #################################################### Parent
            h_parent += 1
            if h_parent > 30:
                tree_tags = remove_duplicates(tree_tags)
                break
            sim_parent = parent(crnt_tgs, len(crnt_tgs) - h_parent)
            try:
                [tree_tags.append(copy.deepcopy([qu, x, (1-(1/(h - h_parent))), 4])) for x in sim_parent]
            except:
                [tree_tags.append(copy.deepcopy([qu, x, 0, 4])) for x in sim_parent]
            
            tree_tags = remove_duplicates(tree_tags)

    # stop_1 = timeit.default_timer()
    # print('Time_1: ', stop_1 - start_1)  

    tree_tags.sort(key=lambda x: x[2], reverse=True)
    res = tree_tags[:50]    

    res = [x for x in res if x[1] != qu]

    with open('../../data/bioinformatics/bioinformatics_sim_questions_tree.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        for i in res:
            if i[0] != i[1]:
                writer_object.writerow(i)
        f_object.close()


