# Cielo Intelligence

Busca semântica com redes neurais sobre a **documentação pública oficial** da Cielo. Recupera trechos com URL de origem, classifica o tema da pergunta e **se abstém quando a documentação não traz evidência**.

> Projeto experimental, não oficial. Não executa pagamentos, não autentica em áreas privadas e não substitui documentação, suporte ou homologação.

## O que é (e o que não é)

| Camada | Implementação | Natureza |
|---|---|---|
| Base documental | `crawler.py` (llms.txt + `.md` + PDFs, host oficial, respeita robots.txt) | coleta |
| Camada neural | `paraphrase-multilingual-MiniLM-L12-v2` (embeddings) | rede pré-treinada, **não treinada aqui** |
| Busca híbrida | BM25 (palavras exatas) somado aos embeddings (`hybrid_weight`) | dá peso a nomes de produto |
| Classificação | MLP (48→24) sobre os embeddings, treinada em `training_examples.jsonl` | rede treinada aqui, com exemplos sintéticos revisáveis |
| Resposta | trechos + URL + aviso de "sem evidência" | recuperação (RAG sem gerador) |

Não é um LLM treinado do zero. Nada aqui afirma que "o modelo aprendeu toda a documentação": `data/<eco>/index_meta.json` registra exatamente quantas páginas/PDFs/trechos foram processados e se o índice veio só da base-semente (`seed_only`).

## Uso local

Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .                  # registra o pacote csi (src/) e o comando `csi`

python -m csi crawl cielo --max-pages 100   # teste pequeno; sem flag = tudo
python -m csi index cielo                   # embeddings + MLP + index_meta.json
python -m csi eval cielo -v                 # recall@k, MRR, tema, produto, abstenção (-v = pergunta por pergunta)
python -m csi calibrate cielo               # sugere o min_score a partir das perguntas de avaliação
python -m csi retrain cielo                 # retreina só a MLP de tema (rápido), sem refazer o índice
python -m csi ask cielo "Quais os requisitos do Tap on Phone para iOS?"
streamlit run app.py
```

Sem rodar o `crawl`, o `index` usa só a base-semente (`ecosystems/<eco>/seed_knowledge.md`) e o app avisa isso. Se o `llms.txt` estiver fora do ar, o crawler cai para as páginas de `seed_sources.json` + `.md`.

## Testes

```bash
python -m unittest discover -s tests -v
```

Rodam offline com um encoder determinístico (sem baixar modelo, sem acessar os portais). Eles validam a lógica; **não medem a qualidade do modelo real**. Para isso use `python -m csi eval <eco>` depois de indexar.

## Calibração antes de confiar nos resultados

1. **`min_score`** (`ecosystems/*/config.json`, padrão 0,40) é a pontuação híbrida mínima do 1º resultado para responder. Rode `python -m csi calibrate <eco>`: a tabela mostra, para cada limite, quantas respostas erradas seriam entregues e quantas certas seriam perdidas. Prefira o menor limite com **zero respostas erradas entregues**. Com poucas perguntas é só ponto de partida.
2. **`wrong_answers_delivered`** (no `eval`) é a métrica de segurança principal: respostas com evidência, mas da página errada, e perguntas fora do escopo respondidas.
3. **`training_examples.jsonl`** tem exemplos sintéticos e revisáveis (cerca de 5 a 9 por tema). Nenhuma pergunta de `eval_questions.jsonl` pode aparecer no treino; um teste verifica isso. Amplie os exemplos antes de interpretar `category_accuracy`.
4. **Produto pela fonte:** `product_families` mapeia o 1º trecho do caminho da URL a um produto. Só vale para portais cuja URL é organizada por produto, como o da Cielo.
5. `eval_questions.jsonl` cobre só páginas da base-semente. Depois do crawl completo, acrescente perguntas validadas por especialista.

## Estrutura

```
ecosystems/<eco>/   config.json, seed_*, training_examples.jsonl, eval_questions.jsonl
src/csi/            config, crawler, indexer, classifier, search, evaluate, cli
app.py              interface Streamlit com seletor de ecossistema
tests/              testes offline
data/               artefatos gerados (ignorado pelo git)
docs/               escopo e metodologia de cada ecossistema
```


## Outros ecossistemas

O projeto suporta mais de um portal: para adicionar (por exemplo, a Stone), crie uma pasta em `ecosystems/` com `config.json`, `seed_sources.json`, `seed_knowledge.md`, `training_examples.jsonl` e `eval_questions.jsonl`.

## Segurança

Só conteúdo público do host configurado. Nunca coloque PAN, CVV, trilhas, tokens, certificados ou dados de clientes em `data/`, nos exemplos ou nas perguntas.

## Próximos passos

Manifesto com versão/data (hash e data de coleta já são gravados), inspeção visual de PDFs com tabelas, perguntas avaliadas por especialista e, só depois, um LLM gerador com citação obrigatória e recusa sem suporte.
