## Syntax and Semantix expert recommendation
This repository contains the code of our paper. To run the code for your dataset, please follow the below instructions:

## Progress
To use this code for your purposes and dataset, follow and run the files in order based on their numbers. Each folder is named with a number to indicate the sequence, from `1_preparation` to `4_MLP`. Within each folder, if order matters, the files follow a similar pattern; otherwise, you can run them in any order. Detailed instructions for each section are provided below.

## 0. Download Dataset
We used the Stack Exchange dataset. You can download it from [archive.org](https://archive.org/details/stackexchange). Download the datasets and then extract each dataset to the data directory, in the corresponding folder. For instance, you should extract the `biology` dataset into the `./data/biology`.

## 1. Preparation
To convert XML files to CSVs, firstly, you should run all the Python files in the `1_prepration` folder. So, you should run the Python files in the `Comments`, `Posts`, `Tags`, `User`, and `Worker` directories. Paths are relative, and all files will be stored in the `data` directory. You may change the name of the directory for each different dataset in the Python codes.

## 2. situation_vector
This folder is responsible for computing the Syntax and Semantic similarities between texts. In the `W2V` folder, we first compute the permutation of tags, to have the all possible sequence of questions' tags, in `1_seprate_tags`, then train and create word2vec vectors in `2_create_word2vec`. 

In the `2_tree` folder, we sort the questions' tags separately based on the number of tags, then, compute the Syntax similarity between questions via the `tree`.   
