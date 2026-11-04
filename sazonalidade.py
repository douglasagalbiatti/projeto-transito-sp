import glob
import pandas as pd

arquivos = sorted(glob.glob("dados/brutos/sinistros_*.csv"))

df = pd.concat([pd.read_csv(a, sep=";", low_memory=False) for a in arquivos], ignore_index=True)
df = df[(df["ano_sinistro"] >= 2019) & (df["tipo_registro"] != "NOTIFICACAO")]

print(len(df), df["tipo_registro"].value_counts(), sep="\n")

contagem = df.groupby(["ano_sinistro", "mes_sinistro"]).size().reset_index(name="sinistros")
print(len(contagem))

datas = pd.to_datetime(dict(year=contagem["ano_sinistro"], month=contagem["mes_sinistro"], day=1))
contagem["dias"] = datas.dt.days_in_month
print(contagem.head(14))

contagem["por_dia"] = contagem["sinistros"] / contagem["dias"]

tabela = contagem.pivot(index="ano_sinistro", columns="mes_sinistro", values="por_dia")
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)
print(tabela.round(1))