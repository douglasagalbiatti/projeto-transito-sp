import io
import os
import requests
import pandas as pd

API = "https://dadosabertos.sp.gov.br/api/3/action/package_show?id=eventos-de-sinistro"
recursos = requests.get(API, timeout=60).json()["result"]["resources"]

os.makedirs("dados/brutos", exist_ok=True)

def baixar_capital(recurso):
    resposta = requests.get(recurso["url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=150)
    resposta.raise_for_status()
    df = pd.read_csv(io.BytesIO(resposta.content), sep=";", encoding="latin-1", low_memory=False)
    codigos = pd.to_numeric(df["cod_ibge"], errors="coerce")
    return df[codigos == 3550308]

for recurso in recursos:
    nome = recurso["url"].split("?")[0].split("/")[-1]
    sp = baixar_capital(recurso)
    sp.to_csv(f"dados/brutos/{nome}", sep=";", index=False)
    print(nome, len(sp))