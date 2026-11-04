"""Sinistros por dia em cada mês, de 2019 em diante (Módulo 3).

Pergunta: a queda de agosto para setembro de 2026 é sazonal? Para isso,
monta uma tabela com os anos nas linhas e os meses nas colunas. Cada célula
traz os sinistros fatais e não fatais (sem notificações) divididos pelos
dias do mês, para que meses de tamanhos diferentes possam ser comparados.

Requer dados/brutos/, criado pelo baixar.py.
Uso: .venv/bin/python sazonalidade.py
"""

import glob
import pandas as pd

# Junta os arquivos mensais da capital num único DataFrame
arquivos = sorted(glob.glob("dados/brutos/sinistros_*.csv"))
df = pd.concat([pd.read_csv(a, sep=";", low_memory=False) for a in arquivos], ignore_index=True)

# De 2015 a 2018 a base só tem sinistros fatais, por isso começa em 2019.
# As notificações saem porque quase nunca informam veículos nem vítimas.
df = df[(df["ano_sinistro"] >= 2019) & (df["tipo_registro"] != "NOTIFICACAO")]

# Conferência: total de linhas e divisão entre fatais e não fatais
print(len(df), df["tipo_registro"].value_counts(), sep="\n")

# Uma linha por par (ano, mês), com o número de sinistros.
# Conferência: devem ser 93 pares (2019 a 2025 completos, mais 9 meses de
# 2026). Um mês sem nenhum sinistro sumiria daqui sem aviso.
contagem = df.groupby(["ano_sinistro", "mes_sinistro"]).size().reset_index(name="sinistros")
print(len(contagem))

# Número de dias de cada mês, considerando anos bissextos: monta a data do
# dia 1 de cada mês e pergunta ao pandas quantos dias aquele mês tem.
datas = pd.to_datetime(dict(year=contagem["ano_sinistro"], month=contagem["mes_sinistro"], day=1))
contagem["dias"] = datas.dt.days_in_month
print(contagem.head(14))

# Taxa diária: corrige o efeito de meses com 28, 29, 30 ou 31 dias
contagem["por_dia"] = contagem["sinistros"] / contagem["dias"]

# Formato largo: anos nas linhas, meses nas colunas. Os meses que ainda não
# aconteceram (outubro a dezembro de 2026) aparecem como NaN.
tabela = contagem.pivot(index="ano_sinistro", columns="mes_sinistro", values="por_dia")
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)  # não esconde colunas com "..."
print(tabela.round(1))
