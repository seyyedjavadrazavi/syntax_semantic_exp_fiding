import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import cal_metric
import copy
from b_s import bert_Score
import math

posts = pd.read_csv(r"../data/bioinformatics/bioinformatics_Posts.csv")
avg_scrs = pd.read_csv(r"../data/bioinformatics/bioinformatics_res_F1_10_layers.csv")
avg_scrs.columns = ['qu_id', 'sim_ques_id', 'similarity']
avg_scrs = avg_scrs.drop_duplicates(subset=['qu_id', 'sim_ques_id'])
train_data = pd.read_csv(r"../data/bioinformatics/bioinformatics_train_data_combination.csv")
validate_data = pd.read_csv(r"../data/bioinformatics/bioinformatics_validate_data_combination.csv")
test_data = pd.read_csv(r"../data/bioinformatics/bioinformatics_test_data_combination.csv")

X_train = train_data[['req_fair_aban', 'req_fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty_subscrp', 'difclt_rep_diff_subscrp', 'wrkr_rep', 'wrkr_exprtis']]
y_train = train_data[["label"]]

X_val = validate_data[['req_fair_aban', 'req_fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty_subscrp', 'difclt_rep_diff_subscrp', 'wrkr_rep', 'wrkr_exprtis']]
y_val = validate_data[["label"]]

X_test = test_data[['req_fair_aban', 'req_fair_comm', 'req_rep', 'req_exprtis', 'tsk_difficlty_subscrp', 'difclt_rep_diff_subscrp', 'wrkr_rep', 'wrkr_exprtis']]
y_test = test_data[["label"]]

# Initialize the MLP classifier
mlp = MLPClassifier(hidden_layer_sizes=(50,), max_iter=500, random_state=42)

# Training process
train_accuracies = []
val_accuracies = []

# Custom training loop to capture accuracy over epochs
n_epochs = 50
for epoch in range(n_epochs):
    mlp.partial_fit(X_train, y_train, classes=np.unique([0, 1]))
    train_pred = mlp.predict(X_train)
    val_pred = mlp.predict(X_val)
    train_acc = accuracy_score(y_train, train_pred)
    val_acc = accuracy_score(y_val, val_pred)
    train_accuracies.append(train_acc)
    val_accuracies.append(val_acc)
    print(f'Epoch {epoch+1}/{n_epochs}, Training Accuracy: {train_acc}, Validation Accuracy: {val_acc}')

# Evaluate the model on the test set
test_pred = mlp.predict(X_test)
test_accuracy = accuracy_score(y_test, test_pred)
print(f'Test Accuracy: {test_accuracy}')

y_test = y_test.values.tolist()
y_test = [x[0] for x in y_test]
test_pred = list(test_pred)

df_mlp1 = test_data[['ques_id', 'wrkr_id']]
df_mlp1['org_label'] = y_test
df_mlp1['pred_label'] = test_pred

idis = df_mlp1.ques_id.unique()

y_test = []
test_pred = []
b_s = []
df_mlp1['org_label'].astype(int)
# idis = idis[:10]
grtr_one = 0
for id in idis:
    crnt_ques = df_mlp1.loc[df_mlp1['ques_id'] == id]
    print(len(crnt_ques))
    if len(crnt_ques):
        grtr_one += 1
    crnt_ques = crnt_ques.loc[crnt_ques['pred_label'] == 1]

    if len(crnt_ques) == 0:
        df_mlp1.loc[(df_mlp1['ques_id'] == id), 'bert_score'] = 0
        continue

    for wrkr in crnt_ques.iterrows():

        res = bert_Score(wrkr[1]['wrkr_id'], wrkr[1]['ques_id'], id)
        df_mlp1.loc[(df_mlp1['ques_id'] == id) & (df_mlp1['wrkr_id'] == wrkr[1]['wrkr_id']), 'bert_score'] = res

        # with open('../data/bioinformatics/bioinformatics_ML_res_subs.csv', 'a', newline='') as f_object:
        #     writer_object = writer(f_object)    
        #     writer_object.writerow([id, wrkr[1]['wrkr_id'], res])
        #     f_object.close()

mrr = []
p_at_1 = []
dcgk = []
for id in idis:
    qu_acan_id = posts.loc[posts['Id'] == id, 'AcceptedAnswerId'].values[0]
    acan_ownr_id = posts.loc[posts['Id'] == qu_acan_id, 'OwnerUserId'].values[0]

    crnt_ques = df_mlp1.loc[df_mlp1['ques_id'] == id]
    crnt_ques.sort_values('bert_score', ascending = False)
    y_test.append(copy.deepcopy(crnt_ques['org_label'].values.tolist()))
    test_pred.append(copy.deepcopy(crnt_ques['bert_score'].values.tolist()))

    qu_tst_pred = crnt_ques['wrkr_id'].values.tolist()
    if acan_ownr_id in qu_tst_pred:
        ind = qu_tst_pred.index(acan_ownr_id)
    else:
        continue
    mrr.append(copy.deepcopy(1/(ind+1)))

    if qu_tst_pred[0] == acan_ownr_id:
        p_at_1.append(copy.deepcopy(1))

    dcgk.append(copy.deepcopy(1/math.log2((ind+1)+1)))

M_MRR = sum(mrr) / len(idis)
M_p_at_k = sum(p_at_1) / len(idis)
N_DCG = sum(dcgk) / len(idis)
print('MRR is ', M_MRR)
print('M_p_at_k is ', M_p_at_k)
print('N_DCG is ', N_DCG)

# df_mlp1.to_csv(r"../data/bioinformatics/bioinformatics_ordered_res_rmv_orgnal_ques.csv", index = False, header=True)

print('MLP first -> mean_mrr issssssssssss :', cal_metric(y_test, test_pred, ['mean_mrr']))
print('MLP first -> NDCG issssssssssss :', cal_metric(y_test, test_pred, ['ndcg@10']))
print('MLP first -> P@1 issssssssssss :', cal_metric(y_test, test_pred, ['P@1']))

# Plotting the training and validation accuracy over epochs
fig, ax = plt.subplots()
ax.set_xlim(0, n_epochs)
ax.set_ylim(0, 1)
ax.set_xlabel('Epoch')
ax.set_ylabel('Accuracy')
line1, = ax.plot([], [], label='Training Accuracy', color='blue')
line2, = ax.plot([], [], label='Validation Accuracy', color='orange')
ax.legend()

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

def update(epoch):
    line1.set_data(range(epoch+1), train_accuracies[:epoch+1])
    line2.set_data(range(epoch+1), val_accuracies[:epoch+1])
    return line1, line2

ani = animation.FuncAnimation(fig, update, frames=n_epochs, init_func=init, blit=True)
plt.show()

a = 111