import pandas as pd
import copy
from sklearn.model_selection import train_test_split

posts = pd.read_csv(r"../../data/bioinformatics/bioinformatics_Posts.csv")
posts['CreationDate'] = pd.to_datetime(posts['CreationDate'])
posts = posts.loc[posts['CreationDate'] < '2019-06-01T00:00:00.000000000']
questions = posts[(posts['PostTypeId'] == 1) & (~posts['AcceptedAnswerId'].isnull())]
slcted_questions = questions[['Id', 'AcceptedAnswerId', 'OwnerUserId', 'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount']]
labels = (len(slcted_questions) * [1])

x_train, x_Combine, y_train, y_Combine = train_test_split(slcted_questions, labels, train_size = 0.8, random_state = 42) 
  
x_val, x_test, y_val, y_test = train_test_split(x_Combine, y_Combine, test_size = 0.5, random_state = 42) 

x_test['label'] = y_test
x_train.to_csv('../../data/bioinformatics/bioinformatics_train_data.csv', index=False)
x_val.to_csv('../../data/bioinformatics/bioinformatics_validate_data.csv', index=False)
x_test.to_csv('../../data/bioinformatics/bioinformatics_test_data.csv', index=False)
