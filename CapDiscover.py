from pyjarowinkler import distance as d
import pandas as pd
import pickle
import os
from util import util
import matplotlib.pyplot as plt

path = 'Data/Limpesa1/'

files = os.listdir(path)
all_interations = {}

if  os.path.exists('Data/pickles/jarowinkler_arrays_values.pickle'):
    all_interations = pickle.load(open('Data/pickles/jarowinkler_arrays_values.pickle', 'rb'))
    plt.hist(all_interations['Base de Dengue11'])
    plt.show()
# pickle.dump(files,open('aaaa.pickle','wb'))
# colunas_pareamento = ['Nome', 'Nome da Mae', 'Nome do Pai', 'Sexo', 'Bairro', 'Data de Nascimento']
#
#
# for file in files:
#     df = util.generateKey(pd.read_csv(path+file),colunas_pareamento)
#     file = file.split('.')[0]
#     all_interations.update({file+'1': [],file+'2': []})
#     size = len(df)
#     perc = 0
#     for s,(i,line) in enumerate(df.iterrows()):
#         biggest_value = 0
#         for j,line2 in df.iterrows():
#             if i == j:
#                 continue
#             jar_value = d.get_jaro_distance(line['key'],line2['key'])
#             all_interations[file+'1'].append(jar_value)
#             if jar_value > biggest_value :
#                 biggest_value = jar_value
#         all_interations[file+'2'].append(biggest_value)
#
#         if s / size * 100 > perc:
#             print(perc, '%')
#             perc += 1
#
#     if not os.path.exists('Data/pickles/'):
#         os.mkdir('Data/pickles/')
#
# pickle.dump(all_interations,open('Data/pickles/jarowinkler_arrays_values.pickle','wb'))


