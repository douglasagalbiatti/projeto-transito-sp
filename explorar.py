import io
import requests
import pandas as pd

API = "https://dadosabertos.sp.gov.br/api/3/action/package_show?id=eventos-de-sinistro"
recursos = requests.get(API, timeout=60).json()["result"]["resources"]
ultimo = recursos[-1]
print(ultimo["name"])

resposta = requests.get(ultimo["url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=150)
# O arquivo vem separado por ";" e não está em UTF-8
df = pd.read_csv(io.BytesIO(resposta.content), sep=";", encoding="latin-1", low_memory=False)
print(df.shape)

# Sua parte começa aqui
codigos = pd.to_numeric(df["cod_ibge"], errors='coerce')
e_capital = codigos == 3550308
sp = df[e_capital]

print(f'{len(sp)} de {len(df)} registros: {len(sp)/len(df):.1%}')
print(sp["tipo_registro"].value_counts())