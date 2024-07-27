## Syntax and Semantic Expert Recommendation

This repository contains the code for our paper on expert recommendation systems based on syntax and semantic analysis. To utilize this code for your dataset, please follow the instructions outlined below.

### Progress

The code is organized sequentially, with folders numbered from 1 to 4. Each folder represents a step in the process, starting with data preparation and ending with a multi-layer perceptron (MLP) model. If file order matters within a folder, it follows a similar numerical pattern. Detailed instructions for each section are provided below.

### 0. Download Dataset

We utilized the Stack Exchange dataset, which can be downloaded from [archive.org](https://archive.org/details/stackexchange). Extract each dataset to the corresponding folder in the `./data` directory. For example, the biology dataset should be extracted to `./data/biology`.
In this repository, we changed the 'task' term to 'question' because we used the Stack Exchange dataset, where questions are referred to as tasks. So, in some cases, based on the need we used 'question' and 'task' instead of each other. 
### 1. Preparation

To convert XML files to CSV, execute all Python scripts in the `1_preparation` folder. This includes the `Comments`, `Posts`, `Tags`, `User`, and `Worker` directories. Paths are relative, and all files will be stored in the `data` directory. Modify the directory names in the Python scripts for different datasets as needed.

### 2. Situation Vector

This folder is dedicated to computing syntax and semantic similarities between texts.

##### 2.1 Word2Vec

In the `W2V` folder, we first compute permutations of tags to create all possible sequences of question tags (`1_separate_tags`). Then, we train and create word2vec vectors (`2_create_word2vec`). The W2V model is used for computing semantic similarity.

##### 2.2 Syntax Similarity

In the `2_tree` folder, we sort question tags based on their number and compute syntax similarity using a tree structure. Tags are considered children, siblings, or parents based on their relationships to the input question, as detailed in our paper.

##### 2.3. Semantic Similarity

###### 2.3.1 Graph

First, we select one tag from the input question and compute the five most similar tags using the W2V model. Questions with at least one of these tags are selected. This process is recursively repeated for all tags of the new question until all tags are considered or the number of candidate questions is sufficiently reduced. The Apriori algorithm is employed to select new candidates at each step.

###### 2.3.2 SBERT -> 4_bert_score folder

In the `4_bert_score` folder, we use the BERT Score to calculate the similarity between question bodies. Due to the time-consuming nature of this process, we generate a shortlist of candidates by averaging the `tree` and `graph` candidates. The BERT Score is then calculated for candidates with higher scores.

##### 2.5. Union

We compute the average similarity scores of all candidates from the previous three phases (tree, graph, and BERT). This is done using two methods: intersections and ordering. In the first method, we find the intersection of the three candidate lists and select questions recommended by all similarity methods first, and then, other questions are selected based on their scores. In the second method, all questions are ordered and selected based on their similarity scores.

##### 2.6. Task Difficulty

Here, we compute the difficulty of tasks based on the reputation of users who have completed similar tasks. 


### 3. Profiles
In this directory, we split the dataset into training, testing, and validation sets. We also create profiles for both requesters and workers, as well as situation vectors, which are used as inputs for training, testing, and validating the model.

##### 3.1. Split Data
In the `1_split_data` folder, the Python code divides the dataset to test, train, and validate data 80%, 10%, and 10%, respectively. 

##### 3.2. Req Profile
In the folder `2_req_profile` there are two subfolders, by which the requesters' profiles including fairness, expertise, and reputation are generated.

In the `fairness/abandoned_tasks_rate` directory, we first calculate the average number of upvotes for accepted answers to a requester's questions. Then, we determine the number of questions that have answers with more upvotes than the average but were not chosen as the accepted answer. This could be a possible indication of unfair behavior.

In the `fairness/deviation_from_community` directory, we define the answers that were marked as accepted but had lower upvotes compared to other answers in a question. 

In the `exp_rep` directory, the reputation and expertise of requesters are computed. Expertise means how many accomplished tasks in a specific domain each requester has. 

##### 3.3. Worker Profile
In this directory, the workers' profiles including expertise in domain and reputation are generated.

##### 3.4. Create Situation Vector
Here, the input data of the ML model for training, validating, and testing purposes are generated. Each row includes the worker, requester, and task information.

### 4. MLP

Continue....
