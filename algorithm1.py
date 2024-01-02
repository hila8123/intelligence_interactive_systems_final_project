import pandas as pd
import math
from csv import reader


def main():

    df = pd.read_csv('playlist.csv')
    size = df.shape
    num_of_voters = size[0]
    num_of_preferences = size[1]-1
    #print(size)

    scores = []
    # scores2 = []

    T = []
    with open('playlist.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        help = 0
        for row in csv_reader:
            if help != 0:
                T.append(row[1:])
            help = help + 1

    for i in range(len(T)):
        for j in range(len(T[0])):
            if T[i][j] == '0':
                T[i][j] = '21'

    #print(T)

    num_ = 21
    #print(new_b(T[0],max_))

    for j in range(0, num_of_voters):
        total_ = 0
        # total_2 = 0
        b = (new_b(T[j], num_))
        #print(b)
        for i in range(0,num_of_voters):
            C_ = (new_b(T[i], num_))
            sum1 = (Kp(b, C_, num_of_preferences))
            # sum2 = (K_haus(b, C_, num_of_preferences))
            total_ += sum1
            # total_2 += sum2
        scores.append(total_ /num_of_voters)
        # scores2.append(total_2/num_of_voters)

    #print(scores)
    winner_score = min(scores)
    winner = scores.index(winner_score)
    #print('The winner Kp is:', winner, ',score:', winner_score)
    # print(((new_b(T[winner], num_))))
    my_dict = ((new_b(T[winner], num_)))
    my_dict2 = {}
    for x,y in my_dict.items():
        if len(y) == 1:
            my_dict2[y[0]] = x
        else:
            for item in y:
                my_dict2[item] = x
    #my_dict2 = {y[0]:x for x,y in my_dict.items()}
    return (dict(sorted(my_dict2.items())))


def Kp (B, C, num):

    const_p = 0.5
    D = make_D(B, C, num)
    R1 = R(B, C)
    R2 = R(C, B)

    return (D + (const_p*(R1 + R2)))

def K_haus (B , C , num):

    D = make_D(B, C, num)
    R1 = R(B, C)
    R2 = R(C, B)

    return (D + (max(R1,R2)))

def sum_Bi (B): # sum (|ci| 2 or |bi| 2)
    total = 0
    const = 2
    for i in range(1,len(B)+1):
        temp = len(B[i])
        temp2 = math.factorial(temp)
        if temp >=2 :
            temp3 = math.factorial(temp-const)
            total += (temp2/(temp3*2))

    return total

def R(B , C):

     return sum_Bi(C) - all_Cij(C, B)


def all_Cij (C , B ):# sum (|cij| 2)

    total = 0
    const = 2
    for j in range (1, len(B)+1):
        for i in range(1,len(C)+1):
            cij = C_ij(B[j],C,i)
            if cij >= 2 :
                temp = math.factorial(cij)
                temp2 = math.factorial(cij-2) * const
                total += (temp/temp2)

    return int(total)


def new_b(row , max_):

    scores = {}
    for i in range(1, max_+1):
        temp = []
        for j in range(len(row)):
            if row[j] == str(i):
                #temp.append(scores[i])
                temp.append(j+1)
                scores[i] = temp

    return scores

def C_ij (Bi , C , m):

    count = 0
    start = m
    if len(Bi) == 1:
        return 1
    # for i in range(start,len(C)+1):
    temp = list(C[start])
    for j in range(len(Bi)):
        if temp.count(Bi[j]) != 0:
            count += 1

    return count

def make_D(B,C ,num):

    b = B
    c = C
    count_D = 0
    bi = 0
    bj = 0
    ci = 0
    cj = 0
    for i in range(0,num-1):
        for j in range(i+1,num):
            for m in range(1,len(c)+1):

                list_ = list(b[m])
                if i in list_ and j not in list_: #i>j in b
                    bi = m
                elif i not in list_ and j in list_: #j>i in b
                    bj = m

                list1 = list(c[m])
                if i in list1 and j not in list1: #i>j in b
                    ci = m
                elif i not in list1 and j in list1:  # j>i in b
                    cj = m
        if bi != 0 and bj != 0 and ci != 0 and cj != 0:
            if bi < bj and ci > cj or bi > bj and ci < cj:
                count_D += 1

    return count_D

def trun_to_dic(A):

    s = {}
    for i in range(len(A)):

        s[i+1] = A[i]

    return s

main()
