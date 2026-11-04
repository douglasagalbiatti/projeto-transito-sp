import glob
import pandas as pd

arquivos = sorted(glob.glob("dados/brutos/sinistros_*.csv"))

df = pd.concat([pd.read_csv(a, sep=";", low_memory=False) for a in arquivos], ignore_index=True)
df = df[(df["ano_sinistro"] >= 2019) & (df["tipo_registro"] != "NOTIFICACAO")]

print(len(df), df["tipo_registro"].value_counts(), sep="\n")