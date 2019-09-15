import pandas as pd
from pyjarowinkler import distance
import util
import pickle
from functools import reduce
import os

dfAlunos = pd.read_csv('Data/Limpesa1/Base de Alunos1.csv')
dfDengue = pd.read_csv('Data/Limpesa1/Base de Dengue1.csv')
dfOnibus = pd.read_csv('Data/Limpesa1/Base de Onibus1.csv')

keys_pareadas_alunos = pickle.load(open('Data/Limpesa1/pareamento_aluno_88.pickle','rb'))
keys_pareadas_onibus = pickle.load(open('Data/Limpesa1/pareamento_onibus_88.pickle','rb'))
duplicatas = []
for key in keys_pareadas_onibus.keys():
    if len(keys_pareadas_onibus[key]) > 0:
        duplicatas.append(keys_pareadas_onibus[key] + [key])

keys_pareadas_dengue = pickle.load(open('Data/Limpesa1/pareamento_dengue_88.pickle','rb'))
a = [dfAlunos, dfDengue, dfOnibus]
b = [keys_pareadas_alunos, keys_pareadas_dengue, keys_pareadas_onibus]
c = ['Base de Alunos2.csv','Base de Dengue2.csv','Base de Onibus2.csv']
for k,dataframe in enumerate(a):
    print(c[k][:-4])
    dataframe['KEY'] = reduce(lambda a, b: a+b, [dataframe[coluna] for coluna in ['Nome', 'Nome da Mae', 'Nome do Pai', 'Sexo', 'Bairro', 'Data de Nascimento']])
    to_remove = []
    indexes_to_remove = []
    file = open('Data/Limpesa2/logDuplicatas_' + c[k][:-4] + '.txt' , 'w')
    for i, line in dataframe.iterrows():
        if line['KEY'] in to_remove:
            print('removido ' + line['KEY'] + '  na posicao ' + str(i) + ' do arquivo ' + c[k])
            file.write('removido ' + line['KEY'] + '  na posicao ' + str(i) + ' do arquivo ' + c[k] + '\n')
            indexes_to_remove.append(i)
        if line['KEY'] in b[k].keys():
            to_remove += b[k][line['KEY']]
    print('oi')
    file.close()
    dataframe.drop(inplace = True, index = indexes_to_remove)
    dataframe.drop(['KEY'],axis = 1,inplace = True)
    dataframe.to_csv('Data/Limpesa2/' + c[k], index = False)



