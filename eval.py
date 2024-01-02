import pandas as pd
import csv
import numpy as np
from sklearn.metrics import average_precision_score

# first load the data for personal grades and get average:
users_df = pd.read_csv('playlist.csv')
rows, cols = users_df.shape # (4,31)
dict_of_average = {}
for x in range(1,cols):
    sum = 0
    for index, row in users_df.iterrows():
        sum += row[x]
    sum = sum/rows
    if sum == 0:
        sum = cols
    dict_of_average[x] = sum
print(dict_of_average)

# load the social grades:
df = pd.read_excel(f'https://docs.google.com/spreadsheets/d/1xe2n0HlL3Lqphav5NLdm0bz2XncqoKUxu-w0o7lQP1c/export?format=xlsx', sheet_name='social')
alg1 = df['grade1'].to_list()
for i in range(0, len(alg1)): 
    alg1[i] = int(alg1[i])
print(alg1)
alg2 = (df['grade2'].to_list())
for i in range(0, len(alg2)): 
    alg2[i] = round((int(alg2[i]) /30),2)
list_true1 = []
list_true2 = []
for x in range(30):
    if (dict_of_average[x+1] >= alg1[x]-1) and (dict_of_average[x+1] <= alg1[x]+1):
        list_true1.append(1)
    else:
        list_true1.append(0)
    if (dict_of_average[x+1] >= alg2[x]-1) and (dict_of_average[x+1] <= alg2[x]+1):
         list_true2.append(1)
    else:
        list_true2.append(0)

print(list_true1)
print(list_true2)

# get mean average presicion for first algorithm:
alg1 = (np.array(alg1))/30
list_true1 = np.array(list_true1)
score1 = average_precision_score(list_true1, alg1)
print(score1)

# second algroithm :
alg2 = (np.array(alg2))/30
list_true2 = np.array(list_true2)
score2 = average_precision_score(list_true2, alg2)
print(score2)



