# Projeto Trânsito SP: curso guiado de Ciência de Dados

Este repositório é, ao mesmo tempo, um projeto de dados e um curso. O aluno (Douglas) refaz para a cidade de São Paulo o estudo que fez para Bauru com ajuda de IAs (https://github.com/douglasagalbiatti/projeto-transito-bauru), agora aprendendo cada etapa. O Claude atua como tutor: o objetivo é que o aluno aprenda a fazer, e não receber o trabalho pronto.

## Como conduzir as sessões

- Use a skill `learn` (modo de aprendizagem): diagnosticar antes de ensinar, um passo e uma pergunta por mensagem, mensagens curtas.
- **Código é ensinado linha por linha.** Quando o aluno precisa escrever código, mostre poucas linhas por vez e explique o que cada uma faz e cada argumento. O aluno digita, roda e manda a saída.
- **Peça um palpite antes de cada execução** e compare com o resultado. Isso calibra a intuição sobre os dados.
- Quando o aluno erra, aponte o erro com clareza e com o motivo, sem elogio vazio. Quando ele está travado de verdade, dê um apoio concreto, como fazer o primeiro passo, e devolva o controle.
- Teste o código antes de passá-lo ao aluno, de preferência com `.venv/bin/python` em uma cópia fora do repositório.
- Escreva em português do Brasil.

## Ambiente

```bash
python3 -m venv .venv          # no Ubuntu/Debian, pode exigir: sudo apt install python3-venv
.venv/bin/pip install pandas requests
.venv/bin/python baixar.py     # recria dados/brutos/ (141 arquivos mensais, cerca de 450 MB baixados)
```

- `dados/` fica fora do git (está no `.gitignore`), porque o `baixar.py` reconstrói esses arquivos.
- O remoto `origin` usa SSH (`git@github.com:douglasagalbiatti/projeto-transito-sp.git`). Em outro computador, cadastre a chave SSH dele no GitHub.

## Fonte dos dados

- Infosiga SP (DETRAN-SP), pela API CKAN: `https://dadosabertos.sp.gov.br/api/3/action/package_show?id=eventos-de-sinistro`. Há um CSV de sinistros por mês, de janeiro de 2015 em diante; na última consulta, ia até setembro de 2026.
- Os links dos arquivos têm assinatura com validade (até maio de 2027). Sempre obtenha os links pela API, nunca deixe fixos no código.
- Os CSVs vêm com `sep=";"` e `encoding="latin-1"`. Os arquivos salvos em `dados/brutos/` estão em UTF-8.
- A capital é filtrada por `cod_ibge == 3550308`, convertendo a coluna com `pd.to_numeric(..., errors="coerce")`.
- `tipo_registro` tem três valores: `SINISTRO FATAL`, `SINISTRO NAO FATAL` e `NOTIFICACAO`.
- Ressalvas:
  - de 2015 a 2018, a base contém só sinistros fatais;
  - as notificações quase nunca informam veículos nem vítimas;
  - os meses recentes chegam incompletos e são revisados depois;
  - os óbitos contam até 30 dias após o sinistro;
  - há também as tabelas `pessoas` e `veiculos`, que ainda não foram usadas.

## Arquivos

- `explorar.py`: baixa o mês mais recente do estado e conta os registros da capital por tipo.
- `baixar.py`: baixa todos os meses, filtra a capital e salva um CSV por mês em `dados/brutos/`. Baixar de novo um mês substitui a versão anterior, o que permite refazer a janela de revisão.
- `sazonalidade.py`: junta os meses e filtra de 2019 em diante, sem notificações (parte 1 pronta).

## Estrutura do curso

Cada módulo usa um erro registrado na `ERRATA.md` do projeto de Bauru como ponto de partida.

| # | Módulo | Status |
|---|---|---|
| 1 | Pergunta e unidade de análise | Concluído |
| 2 | Aquisição de dados (API, filtro, download) | Concluído |
| 3 | Auditoria dos dados: cobertura, ausentes, viés de registro | **Em andamento** |
| 4 | Limpeza e variáveis, com funções testáveis em `src/` e testes | Pendente |
| 5 | Estatística descritiva: proporções, taxas, denominadores | Pendente |
| 6 | Inferência: IC, testes, ausência de evidência, comparações múltiplas | Pendente |
| 7 | Análise espacial: distritos, população do Censo 2022, taxas por 100 mil | Pendente |
| 8 | Modelagem: baseline, AUC, calibração, vazamento, divisão temporal | Pendente |
| 9 | Comunicação: relatório, associação vs. causa | Pendente |
| 10 | Produto: painel em Streamlit, testes, GitHub Actions | Pendente |

### Módulo 1: concluído

Conceitos que o aluno já domina:
1. O que uma linha representa (sinistro, pessoa ou notificação)?
2. O numerador e o denominador contam a mesma unidade?
3. Qual regra decide quem entra na base?

Pontos trabalhados:
- A letalidade dos atropelamentos em Bauru mudou de 9,09% para 11,63% por causa de dois vieses opostos: as notificações puxavam para baixo, e os anos de 2015 a 2018, só com fatais, puxavam para cima. Também foram distinguidos "óbitos ÷ sinistros" e "sinistros com óbito ÷ sinistros".
- O aluno de início não percebeu o viés de seleção de 2015 a 2018 e precisou de apoio.

Ficha da primeira pergunta para São Paulo:

| Campo | Conteúdo |
|---|---|
| Pergunta | Os sinistros com motocicleta ocorrem mais em que dia da semana? |
| Indicador | Sinistros com moto por dia da semana |
| Unidade | Sinistro |
| Base | 2019 em diante, sem notificações, `qtd_motocicleta` > 0 |
| O que não responde | Risco (não há volume de motos por dia); casos só registrados como notificação ficam invisíveis |

### Módulo 2: concluído

Achados:
- Em setembro de 2026, a capital teve 27,9% dos registros do estado (palpite do aluno: 40%). O valor está próximo da participação da capital na população do estado (25,8%, Censo 2022), mas a população não mede a exposição ao trânsito.
- Em setembro de 2026, 42,6% dos registros da capital são notificações.
- Em 2015, a capital teve 1.062 registros, todos fatais; em 2019, foram 44.316.
- Conceito trabalhado: janela de revisão. Os meses recentes precisam ser baixados de novo, porque, sem isso, eles parecem ter menos óbitos e mais notificações do que de fato tiveram.

### Módulo 3: em andamento

Pergunta atual: setembro de 2026 tem menos registros do que agosto. A queda vem da falta de registros ainda não incorporados, de sazonalidade ou de variação natural?

Já feito:
- Correção pelo número de dias: o calendário explica cerca de um terço da queda, e setembro continua 6,7% abaixo por dia.
- Em 2019, setembro também fica abaixo de agosto por dia (−7,5%).
- O aluno entendeu que um ano não basta e que o teste certo compara o mesmo par de meses em vários anos.
- Ponto corrigido: a variação natural nunca é "confirmada"; é o que sobra quando não aparece um padrão consistente.

Tabela desenhada:
- Linhas: anos de 2019 a 2026
- Colunas: meses
- Célula: sinistros por dia (fatais mais não fatais, sem notificações, divididos pelos dias do mês)

`sazonalidade.py` parte 1, já pronta: juntar e filtrar os dados. Deu 216.964 linhas (210.271 não fatais e 6.693 fatais); o palpite do aluno foi 200 mil.

**Próximo passo:** a parte 2 do `sazonalidade.py`, já ensinada linha por linha mas ainda não digitada pelo aluno:

```python
contagem = df.groupby(["ano_sinistro", "mes_sinistro"]).size().reset_index(name="sinistros")
datas = pd.to_datetime(dict(year=contagem["ano_sinistro"], month=contagem["mes_sinistro"], day=1))
contagem["dias"] = datas.dt.days_in_month
contagem["por_dia"] = contagem["sinistros"] / contagem["dias"]
tabela = contagem.pivot(index="ano_sinistro", columns="mes_sinistro", values="por_dia")
pd.set_option("display.width", 200)
print(tabela.round(1))
```

Pergunta pendente para o aluno: em quantos dos 8 anos setembro fica abaixo de agosto, e qual explicação ganha força? Deixe o aluno ler a tabela e concluir; não entregue a resposta.

Sequência prevista para o restante do Módulo 3:
- Medir a cobertura por ano: proporção de notificações, coordenadas válidas e hora informada.
- Separar "sem vítimas" de "vítimas não informadas".
- Medir a janela de revisão de verdade: baixar o mesmo mês em datas diferentes e comparar.
- Entrega: um relatório de qualidade dos dados.

## Diferenças esperadas em relação a Bauru

- **Volume maior:** cerca de 217 mil sinistros desde 2019, sem notificações.
- **Validação geográfica:** usar polígonos de distritos (GeoSampa, a ser verificado) no lugar de um retângulo aproximado.
- **Taxas:** calcular por população de distrito, lembrando que isso ainda não é risco.
- **Modelo:** usar divisão temporal (treinar com anos anteriores e testar com anos posteriores), em vez da `train_test_split` aleatória usada em Bauru.
