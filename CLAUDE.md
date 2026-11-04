# Projeto Trânsito SP: curso guiado de Ciência de Dados

Este repositório é, ao mesmo tempo, um projeto de dados e um curso. O aluno (Douglas) refaz para a cidade de São Paulo o estudo que fez para Bauru com ajuda de IAs (https://github.com/douglasagalbiatti/projeto-transito-bauru), agora aprendendo cada etapa. O Claude atua como tutor: o objetivo é que o aluno aprenda a fazer, e não receber o trabalho pronto.

## Como conduzir as sessões

- Use a skill `learn` (modo de aprendizagem): diagnosticar antes de ensinar, um passo e uma pergunta por mensagem, mensagens curtas.
- **Código é ensinado linha por linha.** Quando o aluno precisa escrever código, mostre poucas linhas por vez e explique o que cada uma faz e cada argumento. O aluno digita, roda e manda a saída.
- **Peça um palpite antes de cada execução** e compare com o resultado. Isso calibra a intuição sobre os dados.
- Quando o aluno erra, aponte o erro com clareza e com o motivo, sem elogio vazio. Quando ele está travado de verdade, dê um apoio concreto, como fazer o primeiro passo, e devolva o controle.
- O aluno é PhD em Física e tem ampla experiência com matemática. Não peça palpites de conta trivial nem justificativas óbvias. Concentre as perguntas no domínio dos dados (como o registro nasce, que vieses isso cria), no pandas e no git. Quando os números forem necessários para uma entrega, explique o motivo, em vez de só cobrar.
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
  - há também as tabelas `pessoas` (`pessoas-envolvidas-em-sinistros`) e `veiculos` (`veiculos-envolvidos-em-sinistros`), com uma linha por pessoa ou veículo, ligadas pelo `id_sinistro`. Elas ainda não são baixadas pelo projeto, e quase não incluem notificações.

## Arquivos

- `explorar.py`: baixa o mês mais recente do estado e conta os registros da capital por tipo.
- `baixar.py`: baixa todos os meses, filtra a capital e salva um CSV por mês em `dados/brutos/`. Baixar de novo um mês substitui a versão anterior, o que permite refazer a janela de revisão.
- `sazonalidade.py`: junta os meses, filtra de 2019 em diante sem notificações e imprime a tabela de sinistros por dia, com anos nas linhas e meses nas colunas.
- `cobertura.py`: auditoria do peso das notificações, usando a base inteira. Mostra o % por tipo e por ano, o % de notificações mês a mês em 2025 e 2026, as notificações por dia e o % de registros sem nenhuma informação de gravidade.

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

`sazonalidade.py` concluído: junta e filtra os meses (216.964 linhas: 210.271 não fatais e 6.693 fatais; palpite do aluno: 200 mil) e monta a tabela de anos (2019 a 2026) × meses, com sinistros por dia em cada célula.

Resultados da sessão de 4 de novembro de 2026:
- `len(contagem)` = 93 pares (ano, mês), igual ao palpite (7 × 12 + 9). O aluno entendeu que o `groupby` só cria grupos que existem, e que por isso um mês vazio sumiria sem aviso.
- Fevereiro de 2019 contra janeiro de 2019: a vantagem de fevereiro vai de 3% nos totais para 15% por dia. O aluno acertou o sentido, mas não estimou o tamanho.
- O aluno errou o palpite sobre os `NaN` (achou que seriam dias sem sinistro) e, depois de ser corrigido, chegou sozinho aos 3: outubro a dezembro de 2026.
- Agosto → setembro: setembro cai em 5 de 8 anos (2019 −6,4; 2020 −1,0; 2021 −2,5; 2022 −0,4; 2026 −4,8) e sobe em 3 (2023 +2,9; 2024 +2,2; 2025 +0,6). Conclusão: a sazonalidade perde força.
- Erro do aluno, corrigido: ele achou que os anos antigos já consolidados excluíam a explicação dos registros não incorporados. Na verdade, ela só vale para setembro de 2026, e a tabela não consegue testá-la.
- Experimento definido, com apoio, porque o aluno não chegou a ele sozinho: baixar setembro de 2026 de novo e comparar. Se subir bastante (de 71 para perto de 76 ou mais), isso apoia os registros não incorporados; se ficar perto de 71, sobra a variação natural. O aluno entendeu que agosto de 2026 é uma régua melhor que a média de vários anos, por causa da mudança de nível entre anos.
- **Valor de referência para o experimento:** setembro de 2026 = 71,0 sinistros por dia (cerca de 2.130), com dados baixados em 4 de novembro de 2026.

Ambiente recriado em 4 de novembro de 2026 em outro computador (Python 3.14, pandas 3.1.1). O código do projeto funciona nessa versão.

Cobertura por ano, parte das notificações, com o `cobertura.py`:
- Decisão: a auditoria usa a base inteira (2015 em diante). Os 0% de notificações de 2015 a 2018 são, eles mesmos, o achado.
- A proporção de notificações fica estável entre 33% e 37% de 2019 a 2024, sobe para 38,3% em 2025 e chega a 41,7% em 2026. O palpite do aluno, de que 2026 ficaria mais baixo, estava errado.
- Mês a mês, a hipótese de que a janela de revisão explica tudo não se sustenta: janeiro a março de 2026 já ficam entre 40% e 42% (contra 36% a 37% em 2025), e julho de 2026 é o mês mais baixo. A alta começa em meados de 2025.
- Numerador × denominador, de janeiro a setembro, por dia, 2024 → 2026: notificações 43,5 → 50,9 (+17%); sinistros com vítima 82,1 → 71,0 (−13%); total 125,6 → 121,9 (−3%). O total se conserva em parte, o que é compatível com uma migração de "não fatal" para "notificação" (cerca de dois terços da queda), mas não a prova.
- O aluno de início previu que as notificações por dia subiriam nas duas situações, e foi corrigido: um teste precisa prever resultados diferentes para as hipóteses que compara.

"Sem vítimas" × "vítimas não informadas" (Tabela 4 do `cobertura.py`):
- Pontos corrigidos: `qtd_gravidade_nao_disponivel` é a coluna das vítimas não informadas; "sem vítimas" confirmado é fatal = grave = leve = 0 com ileso > 0; 0 (contou zero) não é o mesmo que NaN (não informado); NaN numa tabela de frações pode ser 0 ÷ 0.
- Cerca de 97% das notificações vêm com as cinco colunas de gravidade vazias, de forma estável de 2019 a 2026. Nos sinistros não fatais, essa fração vai de 0,1% para 0,9% a partir de 2024. As notificações com vítimas feridas ficam em cerca de 3% ao ano, sem tendência.
- Tabela `pessoas` (conjunto `pessoas-envolvidas-em-sinistros` na mesma API, 141 meses, liga pelo `id_sinistro`): testada só com setembro de 2026, numa pasta temporária. Aparecem nela 100% dos fatais, 99,3% dos não fatais e só 2,4% das notificações (38 de 1.580, todas com pessoas leves, graves ou ilesas).
- **Conclusão para o relatório:** a alta das notificações (+17%) junto com a queda dos sinistros com vítima (−13%) é compatível com uma migração de categoria, mas não pode ser testada com os dados publicados. Confirmá-la exigiria informação do DETRAN-SP sobre o processo de registro.
- Pendente (exercício do aluno): acrescentar o item 4 à docstring do `cobertura.py`.

Sequência prevista para o restante do Módulo 3:
- **Próximo passo:** medir o restante da cobertura por ano: coordenadas válidas e hora informada.
- Medir a janela de revisão de verdade: baixar o mesmo mês em datas diferentes e comparar.
- Entrega: um relatório de qualidade dos dados.

## Diferenças esperadas em relação a Bauru

- **Volume maior:** cerca de 217 mil sinistros desde 2019, sem notificações.
- **Validação geográfica:** usar polígonos de distritos (GeoSampa, a ser verificado) no lugar de um retângulo aproximado.
- **Taxas:** calcular por população de distrito, lembrando que isso ainda não é risco.
- **Modelo:** usar divisão temporal (treinar com anos anteriores e testar com anos posteriores), em vez da `train_test_split` aleatória usada em Bauru.
