## Syntanx and Semantix expert recommendation
This repository contains the code of our paper. To run the code for your dataset, please follow the below instructions:

## 0. Download Dataset
We used the Stack Overflow dataset. You can download it from [archive.org](https://archive.org/details/stackexchange). Download the datasets and then extract each dataset to the data directory, in the corresponding folder. For instance, you should extract the biology dataset into the ./data/biology.

## 1. Preparation
To convert XML files to CSVs, firstly, you should run all the Python files in the `1_prepration` folder. So, you should run the Python files in the `Comments`, `Posts`, `Tags`, `User`, and `Worker` directories. Paths are relative, and all files will be stored in the `data` directory.

## 2. Requester Profile
Create profiles for requesters, tasks (works), and workers. To create requesters' profiles, run the following scripts:

