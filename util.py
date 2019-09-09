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


def pareamentoself(dataframebase, colunas, highest_only = False):

    dataframebase['KEY'] = reduce(lambda a, b: a+b, [dataframebase[coluna] for coluna in colunas])
    size = 5000
    perc = 0
    valor_match = 0.85
    matches = {}
    for i, line in dataframebase.iterrows():
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

    return matches
