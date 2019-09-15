import pandas as pd
from pyjarowinkler import distance
import util
import pickle
import os

dfAlunos = pd.read_csv('Data/Base de Alunos0.csv', sep=';')
dfDengue = pd.read_csv('Data/Base de Dengue0.csv', sep=';')
dfOnibus = pd.read_csv('Data/Base de Onibus0.csv', sep=';')
bairros = pd.read_csv('Data/limitebairro.csv', sep=',')
dfAlunos['Sexo'] = dfAlunos['Sexo'].apply(lambda a: 'H' if a == 'm' else 'M')
dfAlunos['Data de Nascimento'] = dfAlunos['Data de Nascimento'].apply(lambda a: '/'.join(a.split(' ')[0].split('-')))
listaBairros = list(bairros['NOME'])

dfDengue['Sexo'] = dfDengue['Sexo'].apply(lambda a: 'H' if a == 'M' else 'M')

dfOnibus['Data de Nascimento'] = dfOnibus['Data de Nascimento'].apply(lambda a: '/'.join([str(a)[:2], str(a)[2:4], str(a)[-4:]]))


dfs = [dfDengue, dfAlunos, dfOnibus]
util.padronize_column(listaBairros, dfs, 'Bairro')
print(1)
if not os.path.exists('Data/Limpesa1/'):
    os.mkdir("Data/Limpesa1/")

dfAlunos.to_csv('Data/Limpesa1/Base de Alunos1.csv', index=False, encoding='utf-8')
dfOnibus.to_csv('Data/Limpesa1/Base de Onibus1.csv', index=False, encoding='utf-8')
dfDengue.to_csv('Data/Limpesa1/Base de Dengue1.csv', index=False, encoding='utf-8')

colunas_pareamento = ['Nome', 'Nome da Mae', 'Nome do Pai', 'Sexo', 'Bairro', 'Data de Nascimento']
Alunos_pareamento, id_chave_alunos = util.pareamentoself(dfAlunos, colunas_pareamento,0.86)
Onibus_pareamento, id_chave_onibus = util.pareamentoself(dfOnibus, colunas_pareamento,0.86)
Dengue_pareamento, id_chave_dengue = util.pareamentoself(dfDengue, colunas_pareamento,0.86)

pickle.dump(Alunos_pareamento,open('Data/pareamento_aluno_86.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)
pickle.dump(Onibus_pareamento,open('Data/pareamento_onibus_86.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)
pickle.dump(Dengue_pareamento,open('Data/pareamento_dengue_86.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)

pickle.dump(id_chave_dengue,open('Data/pareamento_aluno_id_key_86.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)
pickle.dump(id_chave_alunos,open('Data/pareamento_onibus_id_key_86.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)
pickle.dump(id_chave_onibus,open('Data/pareamento_dengue_id_key_86.pickle', 'wb'), protocol = pickle.HIGHEST_PROTOCOL)

# util.pareamentoself(dfAlunos, dfAlunos, colunas_pareamento)
# dfAlunos.to_csv('Base de Alunos2.csv', index=False, encoding='utf-8')
# util.pareamentoself(dfOnibus, dfOnibus, colunas_pareamento)
#
# dfOnibus.to_csv('Base de Onibus2.csv', index=False, encoding='utf-8')
# util.pareamentoself(dfDengue, dfDengue, colunas_pareamento)
#
# dfDengue.to_csv('Base de Dengue2.csv', index=False, encoding='utf-8')
#
#
# pass



