"""Auditoria da cobertura por ano: o peso das notificações (Módulo 3).

Diferente da análise, a auditoria usa a base inteira, de 2015 em diante e
com notificações, porque o objetivo é documentar onde a regra de registro muda.

Imprime três tabelas:
1. composição de cada ano por tipo de registro, em %;
2. % de notificações mês a mês em 2025 e 2026, para testar se a alta de
   2026 vem da janela de revisão (se viesse, os meses recentes seriam os mais
   altos);
3. notificações por dia em cada mês, de 2019 em diante, para separar
   "mais notificações" de "menos sinistros com vítima" (o numerador cresce
   ou o denominador encolhe?).

Requer dados/brutos/, criado pelo baixar.py.
Uso: .venv/bin/python cobertura.py
"""

import glob
import pandas as pd
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)  # não esconde colunas com "..."

# Junta todos os meses da capital, sem filtro de ano nem de tipo
arquivos = sorted(glob.glob("dados/brutos/sinistros_*.csv"))
df = pd.concat([pd.read_csv(a, sep=";", low_memory=False) for a in arquivos], ignore_index=True)

# Tabela 1: % de cada tipo de registro por ano. normalize="index" faz cada
# linha (ano) somar 100%. De 2015 a 2018 só aparecem sinistros fatais.
notif = pd.crosstab(df["ano_sinistro"], df["tipo_registro"], normalize="index")
print((notif * 100).round(1))

# Tabela 2: % de notificações em cada mês de 2025 e 2026. O ano de 2025, já
# revisado, serve de régua para 2026.
recente = df[df["ano_sinistro"] >= 2025]
mensal = pd.crosstab([recente["ano_sinistro"], recente["mes_sinistro"]], recente["tipo_registro"], normalize="index")
print((mensal["NOTIFICACAO"] * 100).round(1).unstack())  # unstack: meses nas colunas

# Tabela 3: notificações por dia (contagem, não proporção), com a mesma
# lógica do sazonalidade.py. Comparada com a tabela de sinistros por dia,
# mostra se as notificações aumentaram de fato.
notificacoes = df[(df["ano_sinistro"] >= 2019) & (df["tipo_registro"] == "NOTIFICACAO")]
cont = notificacoes.groupby(["ano_sinistro", "mes_sinistro"]).size().reset_index(name="notificacoes")
datas = pd.to_datetime(dict(year=cont["ano_sinistro"], month=cont["mes_sinistro"], day=1))
cont["por_dia"] = cont["notificacoes"] / datas.dt.days_in_month
print(cont.pivot(index="ano_sinistro", columns="mes_sinistro", values="por_dia").round(1))

# Tabela 4: % de registros sem nenhuma informação de gravidade (as cinco
# colunas vazias), por ano e tipo. Nesses casos, não dá para distinguir
# "sem vítimas" de "vítimas não informadas": NaN é ausência de informação,
# e não zero.
gravidade = ["qtd_gravidade_fatal", "qtd_gravidade_grave", "qtd_gravidade_leve", "qtd_gravidade_ileso", "qtd_gravidade_nao_disponivel"]
df["sem_info"] = df[gravidade].isna().all(axis=1)  # True se as cinco estão vazias
print((pd.crosstab(df["ano_sinistro"], df["tipo_registro"], values=df["sem_info"], aggfunc="mean") * 100).round(1))  # média de True/False = fração

# Tabela 5: % de coordenadas por situação (válida, fora do retângulo do
# município, zero ou ausente), por ano. As colunas vêm como texto com
# vírgula decimal e precisam ser convertidas.
lat = pd.to_numeric(df["latitude"].str.replace(",", "."), errors="coerce")
lon = pd.to_numeric(df["longitude"].str.replace(",", "."), errors="coerce")
dentro = lat.between(-24.01, -23.36) & lon.between(-46.83, -46.36)
df["coord"] = "fora"
df.loc[dentro, "coord"] = "valida"
df.loc[lat.isna() | lon.isna(), "coord"] = "ausente"
df.loc[(lat == 0) | (lon == 0), "coord"] = "zero"
print((pd.crosstab(df["ano_sinistro"], df["coord"], normalize="index") * 100).round(1))

# Tabela 6: % de coordenadas ausentes mês a mês, de 2024 a 2026, para
# localizar quando a falta começou e se ela é estável.
r = df[df["ano_sinistro"] >= 2024]
ausente = r["coord"] == "ausente"
print((pd.crosstab([r["ano_sinistro"], r["mes_sinistro"]], ausente, normalize="index")[True] * 100).round(1).unstack())

# Tabela 7: % de coordenadas ausentes por tipo de registro, de 2024 a 2026
print((pd.crosstab([r["ano_sinistro"], r["tipo_registro"]], ausente, normalize="index")[True] * 100).round(1).unstack())

# Tabela 8: qualidade da hora, por ano e tipo de registro.
# - ausente: hora não informada;
# - minuto 00: sinal de hora arredondada. Com anotação exata, ficaria em
#   torno de 1/60 ≈ 1,7%; bem acima disso, a hora foi estimada.
minuto = pd.to_numeric(df["hora_sinistro"].str[3:5], errors="coerce")
df["hora_ausente"] = df["hora_sinistro"].isna()
df["minuto_00"] = minuto == 0
hora = df.groupby(["ano_sinistro", "tipo_registro"])[["hora_ausente", "minuto_00"]].mean() * 100
print(hora.round(1).unstack())