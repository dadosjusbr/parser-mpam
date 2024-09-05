# coding: utf8
from cmath import nan
import sys
import os
from coleta import coleta_pb2 as Coleta
import pandas as pd

CONTRACHEQUE = "contracheque"
INDENIZACOES = "indenizações"

HEADERS = {
    CONTRACHEQUE: {
        "Remuneração do Cargo Efetivo": 5,
        "Outras Verbas Remuneratórias, Legais ou Judiciais": 6,
        "Função de Confiança ou Cargo em Comissão": 7,
        "Gratificação Natalina": 8,
        "Férias (1/3 constitucional)": 9,
        "Abono de Permanência": 10,
        "Contribuição Previdenciária": 14,
        "Imposto de Renda": 15,
        "Retenção por Teto Constitucional": 16,
        "Descontos Diversos": 17,
    },
    INDENIZACOES: {
        "Auxílio Alimentação": 5,
        "Indenização de Transporte": 6,
        "Auxílio Moradia": 7,
        "Ajuda de Custo": 8,
        "Auxílio Saúde": 9,
        "Férias Indenizadas": 10,
        "Licença Prêmio Indenizada": 11,
        "Outras Indenizações": 12,
        "Insalubridade/Periculosidade": 13,
        "Serviços Extraordinários": 14,
        "Substituição de Função": 15,
        "Exercício Acumulativo": 16,
        "Convocações": 17,
        "Outras Remunerações Temporárias": 18,
    },
}


def parse_employees(fn, chave_coleta):
    employees = {}
    counter = 1
    forbidden_words = ["Ministério", "Remuneração", "Fonte", "GRUPO", "NOME"]
    for row in fn:
        matricula = row[1]
        for word in forbidden_words:
            if word in row[2]:
                name = nan
                break
            else:
                name = row[2]
        funcao = row[3]

        if pd.isna(row[4]):
            local_trabalho = ""
        else:
            local_trabalho = row[4]

        if not is_nan(name):
            membro = Coleta.ContraCheque()
            membro.id_contra_cheque = chave_coleta + "/" + str(counter)
            membro.chave_coleta = chave_coleta
            membro.nome = str(name)
            membro.matricula = matricula
            membro.funcao = funcao
            membro.local_trabalho = local_trabalho
            membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            membro.ativo = True
            membro.remuneracoes.CopyFrom(cria_remuneracao(row, CONTRACHEQUE))
            employees[name] = membro
            counter += 1
    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        remuneracao.valor = format_value(row[value])
        if categoria == CONTRACHEQUE:
            if value == 5:
                remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
            elif value in [14, 15, 16, 17]:
                remuneracao.valor = remuneracao.valor * (-1)
                remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
            elif value in [6, 7, 8, 9, 10, 11]:
                remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        else:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")

        remu_array.remuneracao.append(remuneracao)
    return remu_array


def update_employees(fn, employees, categoria):
    for row in fn:
        name = str(row[2]).rstrip()
        if name in employees.keys():
            emp = employees[name]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[name] = emp
    return employees


def is_nan(string):
    return string != string


def parse(data, chave_coleta):
    employees = {}
    folha = Coleta.FolhaDePagamento()
    try:
        employees.update(parse_employees(data.contracheque, chave_coleta))
        update_employees(data.indenizatorias, employees, INDENIZACOES)

    except KeyError as e:
        sys.stderr.write(
            "Registro inválido ao processar contracheque ou indenizações: {}".format(
                e
            )
        )
        os._exit(1)
    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha


def format_value(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if is_nan(element):
        return 0.0
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")
        elif "," in element:
            element = element.replace(",", ".")
        elif "-" in element:
            element = 0.0

    return float(element)