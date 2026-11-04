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
