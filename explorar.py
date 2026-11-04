"""Primeiro contato com os dados do Infosiga SP.

Baixa o arquivo mais recente de sinistros do estado e mostra quantos
registros são da capital e de que tipo eles são. Não salva nada em disco.

Uso: .venv/bin/python explorar.py
"""

import io
import requests
import pandas as pd

# A API CKAN do portal de dados abertos lista os arquivos do conjunto
# "eventos-de-sinistro", um por mês. Os links têm assinatura com validade,
# por isso são sempre obtidos pela API, e nunca fixados no código.
API = "https://dadosabertos.sp.gov.br/api/3/action/package_show?id=eventos-de-sinistro"
recursos = requests.get(API, timeout=60).json()["result"]["resources"]
ultimo = recursos[-1]  # o último da lista é o mês mais recente
print(ultimo["name"])

# Baixa o arquivo. O User-Agent de navegador evita que o servidor recuse o
# pedido de um script.
resposta = requests.get(ultimo["url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=150)
# O arquivo vem separado por ";" e não está em UTF-8
df = pd.read_csv(io.BytesIO(resposta.content), sep=";", encoding="latin-1", low_memory=False)
print(df.shape)

# Filtra a capital pelo código IBGE do município de São Paulo (3550308).
# A coluna mistura números e textos; errors="coerce" transforma o que não
# for número em NaN, em vez de interromper o script com erro.
codigos = pd.to_numeric(df["cod_ibge"], errors='coerce')
e_capital = codigos == 3550308
sp = df[e_capital]

# Participação da capital no estado e contagem por tipo de registro
# (SINISTRO FATAL, SINISTRO NAO FATAL e NOTIFICACAO).
print(f'{len(sp)} de {len(df)} registros: {len(sp)/len(df):.1%}')
print(sp["tipo_registro"].value_counts())
