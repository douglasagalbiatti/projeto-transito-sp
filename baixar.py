"""Baixa todos os meses de sinistros do Infosiga SP e guarda só a capital.

Para cada arquivo mensal listado pela API (janeiro de 2015 em diante),
baixa o CSV do estado, filtra o município de São Paulo e salva o resultado
em dados/brutos/, com o mesmo nome do arquivo original (sinistros_MM-AAAA.csv).

Rodar de novo substitui os arquivos. Isso serve para atualizar os meses
recentes, que chegam incompletos e são revisados depois.

Uso: .venv/bin/python baixar.py  (cerca de 450 MB baixados)
"""

import io
import os
import requests
import pandas as pd

# Lista dos arquivos mensais, obtida pela API CKAN. Os links têm validade,
# então não podem ser fixados no código.
API = "https://dadosabertos.sp.gov.br/api/3/action/package_show?id=eventos-de-sinistro"
recursos = requests.get(API, timeout=60).json()["result"]["resources"]

os.makedirs("dados/brutos", exist_ok=True)

def baixar_capital(recurso):
    """Baixa um arquivo mensal do estado e devolve só as linhas da capital."""
    resposta = requests.get(recurso["url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=150)
    resposta.raise_for_status()  # interrompe se o download falhar (erro HTTP)
    # Os arquivos originais usam ";" como separador e codificação latin-1
    df = pd.read_csv(io.BytesIO(resposta.content), sep=";", encoding="latin-1", low_memory=False)
    # 3550308 é o código IBGE de São Paulo; valores não numéricos viram NaN
    codigos = pd.to_numeric(df["cod_ibge"], errors="coerce")
    return df[codigos == 3550308]

for recurso in recursos:
    # O nome do arquivo é o fim do link, sem a assinatura que vem depois do "?"
    nome = recurso["url"].split("?")[0].split("/")[-1]
    sp = baixar_capital(recurso)
    # Salvo em UTF-8 (padrão do pandas), mantendo o separador ";"
    sp.to_csv(f"dados/brutos/{nome}", sep=";", index=False)
    print(nome, len(sp))
