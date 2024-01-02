import pandas as pd
import numpy as np
def main():

    df = pd.read_csv('playlist.csv')
    size = df.shape

    songs = size[1] -1
    participant = size[0]
    # print(df)

    partial_order = df.values
    # print(partial_order)
    RV = np.zeros((songs,songs))

    for i in range(0, participant):
        temp = 1
        m = songs
        while m > 0:
            for j in range(temp,songs):
                if partial_order[i][temp] > partial_order[i][j+1] and partial_order[i][temp] != 0 and partial_order[i][j+1] != 0:
                     RV[temp-1][j] += -1
                     RV[j][temp-1] += 1
                if partial_order[i][temp] < partial_order[i][j+1] and partial_order[i][temp] != 0 and partial_order[i][j+1] != 0:
                    RV[temp-1][j] += 1
                    RV[j][temp-1] += -1
                # print(alpha[0][1],alpha[1][0])
            temp += 1
            m -= 1

    for i in range(0,songs):
        for j in range(0,songs):
            if RV[i][j] < 0 :
                RV[i][j] = -1
            if RV[i][j] > 0 :
                RV[i][j] = 1
            else:
                RV[i][j] = 0

    total =[]
    for i in range(0,songs):
        sum_row = 0
        for j in range(0,songs):
            sum_row += RV[i][j]
        total.append(sum_row)

    total = (list(enumerate(total,1)))
    l = sorted(total,key=lambda element: element[1],reverse=True)
    print(l)
    final_dict = {}
    i = 1
    for element in l:
        final_dict[element[0]] = i
        i += 1

    return ((dict(sorted(final_dict.items()))))


main()
