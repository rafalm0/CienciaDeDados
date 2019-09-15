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


def pareamento(dataframebase, dataframepareando,outroDataframe, colunas,pathbasesaida,pathpareandosaida,outropath, valor_match = 0.89):
    dataframebase['KEY'] = reduce(lambda a, b: a+b, [dataframebase[coluna] for coluna in colunas])
    dataframepareando['KEY'] = reduce(lambda a, b: a + b, [dataframepareando[coluna] for coluna in colunas])
    outroDataframe['KEY'] = reduce(lambda a, b: a + b, [outroDataframe[coluna] for coluna in colunas])
    if not 'ID_UNICO' in dataframebase.columns:
        dataframebase['ID_UNICO'] = range(0, len(dataframebase))
    size = len(dataframebase)
    x = size
    id_unicos = []
    perc = 0
    matches = {}
    usados = []
    for j, line2 in dataframepareando.iterrows():
        for i, line in dataframebase.iterrows():
            jaro_value = distance.get_jaro_distance(line['KEY'], line2['KEY'])
            if (jaro_value > valor_match) and (i not in usados):
                if line2['ID'] not in matches:
                    matches[line2['ID']] = []
                matches[line2['ID']].append([jaro_value, line['ID_UNICO']])
        if line2['ID'] not in matches.keys():
            id_unicos.append(size)
            size += 1
        else:
            g = sorted(matches[line2['ID']], key = lambda a: a[0], reverse = True)[0][1]
            id_unicos.append(g)
            usados.append(g)
        if j/size*100 > perc:
            print(perc, '%')
            perc += 1
    dataframepareando['ID_UNICO'] = id_unicos


    matches = {}
    id_unicos = []
    for j, line2 in outroDataframe.iterrows():
        for i, line in dataframebase.iterrows():
            jaro_value = distance.get_jaro_distance(line['KEY'], line2['KEY'])
            if (jaro_value > valor_match) and (i not in usados):
                if line2['ID'] not in matches:
                    matches[line2['ID']] = []
                matches[line2['ID']].append([jaro_value, line['ID_UNICO']])
        if line2['ID'] not in matches.keys():
            id_unicos.append(size)
            size += 1
        else:
            g = sorted(matches[line2['ID']], key = lambda a: a[0], reverse = True)[0][1]
            id_unicos.append(g)
            usados.append(g)
        if j/size*100 > perc:
            print(perc, '%')
            perc += 1
    outroDataframe['ID_UNICO'] = id_unicos
    dataframepareando.to_csv(pathpareandosaida)
    dataframebase.to_csv(pathbasesaida)
    outroDataframe.to_csv(outropath)
    return


def pareamentoself(dataframebase, colunas, highest_only = False, valor_match = 0.89):

    dataframebase['KEY'] = reduce(lambda a, b: a+b, [dataframebase[coluna] for coluna in colunas])
    size = len(dataframebase)
    perc = 0
    matches = {}
    id_key = {}
    for i, line in dataframebase.iterrows():
        id_key[line['KEY']] = line['ID']
        highest_match = 0
        highest_match_name = None
        for key in matches.keys():
            jaro_value = distance.get_jaro_distance(line['KEY'], key)
            if jaro_value > valor_match:  # deu match
                if not highest_only:
                    matches[key].append(line['KEY'])
                elif jaro_value > highest_match:
                    highest_match = jaro_value
                    highest_match_name = key
        if highest_match_name is not None:
            matches[highest_match_name].append(line['KEY'])
        else:
            matches[line['KEY']] = []

        if i/size*100 > perc:
            print(perc, '%')
            perc += 1

    return matches, id_key


