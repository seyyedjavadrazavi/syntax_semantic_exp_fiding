### Syntax and Semantic Expert Recommendation

This repository contains the code for our paper on expert recommendation systems based on syntax and semantic analysis. To utilize this code for your dataset, please follow the instructions outlined below.

#### Progress

The code is organized sequentially, with folders numbered from 1 to 4. Each folder represents a step in the process, starting with data preparation and ending with a multi-layer perceptron (MLP) model. If file order matters within a folder, it follows a similar numerical pattern. Detailed instructions for each section are provided below.

#### 0. Download Dataset

We utilized the Stack Exchange dataset, which can be downloaded from [archive.org](https://archive.org/details/stackexchange). Extract each dataset to the corresponding folder in the `./data` directory. For example, the biology dataset should be extracted to `./data/biology`.

#### 1. Preparation

To convert XML files to CSV, execute all Python scripts in the `1_preparation` folder. This includes the `Comments`, `Posts`, `Tags`, `User`, and `Worker` directories. Paths are relative, and all files will be stored in the `data` directory. Modify the directory names in the Python scripts for different datasets as needed.

#### 2. Situation Vector

This folder is dedicated to computing syntax and semantic similarities between texts.

##### 2.1 Word2Vec

In the `W2V` folder, we first compute permutations of tags to create all possible sequences of question tags (`1_separate_tags`). Then, we train and create word2vec vectors (`2_create_word2vec`). The W2V model is used for computing semantic similarity.

##### 2.2 Syntax Similarity

In the `2_tree` folder, we sort question tags based on their number and compute syntax similarity using a tree structure. Tags are considered children, siblings, or parents based on their relationships to the input question, as detailed in our paper.

#### 2.3. Semantic Similarity

##### 2.3.1 Graph

First, we select one tag from the input question and compute the five most similar tags using the W2V model. Questions with at least one of these tags are selected. This process is recursively repeated for all tags of the new question until all tags are considered or the number of candidate questions is sufficiently reduced. The Apriori algorithm is employed to select new candidates at each step.

##### 2.3.2 SBERT -> 4_bert_score folder

In the `4_bert_score` folder, we use the BERT Score to calculate the similarity between question bodies. Due to the time-consuming nature of this process, we generate a shortlist of candidates by averaging the `tree` and `graph` candidates. The BERT Score is then calculated for candidates with higher scores.

#### 2.5. Union

We compute the average similarity scores of all candidates from the previous three phases (tree, graph, and BERT). This is done using two methods: intersections and ordering. In the first method, we find the intersection of the three candidate lists and select questions recommended by all similarity methods first, and then, other questions are selected based on their scores. In the second method, all questions are ordered and selected based on their similarity scores.

#### 2.6. Task Difficulty

Here, we compute the difficulty of tasks based on the reputation of users who have completed similar tasks. 

Continue....
