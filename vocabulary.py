import random
from database import vocabulary_time_update
from database import query_times

vocabulary = []

def init_vocabulary():
    f = open('vocabulary.txt','r',encoding="utf-8")
    for i in f.readlines():
        vocabulary.append(i)
    return
def get_vocabulary():
    return random.choice(vocabulary)
def compare_vocabulary(name,user,answer):

    s2 = ''
    for i in str(answer):
        if( i == ' ' ): break
        else: s2 += i

    ouo = ''
    correct = True

    print(answer)
    print('ouo')

    for i in (0,len(str(s2))):
        print(i)
        if ( i >= len(user) ):
            ouo += '.'
            correct = False
        elif( user[i] == s2[i] ):
            ouo += user[i]
        else:
            ouo += '.'
            correct = False

    
    if( correct == True ):
        ouo = '1'
        vocabulary_time_update(name,0)
    else:
        now_times = query_times(name)
        vocabulary_time_update(name,now_times+1)
    
    return ouo
