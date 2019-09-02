import pandas as pd
from pyjarowinkler import distance
from functools import reduce


def findequivalent(names_list, valor):
    higherbairro = 0
    nome_bairro = ''
    for bairro in names_list:
        x = distance.get_jaro_distance(valor, bairro)
        if x > higherbairro:
            higherbairro = x
            nome_bairro = bairro
    return nome_bairro


def padronize_column(names_list, dataframes, colunabase, colunanova=None):
    for dataframe in dataframes:
        if colunanova is None:
            dataframe[colunabase] = dataframe[colunabase].apply(lambda a: findequivalent(names_list, a))
        else:
            dataframe[colunanova] = dataframe[colunabase].apply(lambda a: findequivalent(names_list, a))
    return


def pareamentoself(dataframebase, dataframesecundario, colunas):
    duplicata = []

    dataframebase['KEY'] = reduce(lambda a,b: a+b,[dataframebase[coluna] for coluna in colunas])
    dataframesecundario['KEY'] = reduce(lambda a, b: a + b, [dataframesecundario[coluna] for coluna in colunas])
    size = len(dataframebase)
    perc = 0
    for s,(i, line) in enumerate(dataframebase.iterrows()):
        if i in duplicata:
            continue
        for i2, line2 in dataframesecundario.iterrows():
            jaro_value = distance.get_jaro_distance(line['KEY'], line2['KEY'])
            if jaro_value > 0.95:
                if line['ID'] == line2['ID']:
                    continue
                duplicata.append(i2)
                print(line['KEY'], line2['KEY'])

        if s/size*100 > perc:
            print(perc, '%')
            perc += 1

    dataframebase.drop(duplicata, axis=0, inplace=True)
    return




