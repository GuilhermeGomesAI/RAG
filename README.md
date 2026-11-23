# 🧠 RAG Intelligence

**Busca inteligente sobre documentação técnica de instituições de pagamento, utilizando embeddings, redes neurais e recuperação contextual de informações.**

O RAG Intelligence é um projeto experimental desenvolvido em Python para pesquisar, recuperar e organizar informações presentes na documentação pública oficial da Cielo.

O sistema combina busca semântica, busca lexical (BM25), classificação temática com uma rede neural MLP e recuperação de contexto entre trechos do mesmo documento.

Além de apresentar evidências relevantes, disponibiliza os endereços das fontes oficiais para conferência das informações.

> **Aviso:** Projeto independente e experimental, sem vínculo oficial com a Cielo. Não executa pagamentos, não autentica em ambientes privados e não substitui a documentação oficial, o suporte técnico ou os processos de homologação.

---

## 🎯 Objetivo do projeto

Desenvolver uma solução de inteligência artificial capaz de facilitar a consulta à documentação técnica de instituições de pagamento, reduzindo o tempo necessário para localizar informações sobre APIs, produtos, integrações e processos operacionais.

O projeto foi desenvolvido com foco em:

- Recuperação inteligente de informações técnicas.
- Busca semântica em português.
- Identificação automática do tema da pergunta.
- Combinação de relevância semântica e correspondência lexical.
- Recuperação de trechos complementares do mesmo documento.
- Apresentação das fontes oficiais.
- Abstenção quando não há evidências suficientes.

## 🏗️ Arquitetura e tecnologias

| Camada | Tecnologia | Responsabilidade |
|---|---|---|
| Coleta documental | Python / Crawler | Coleta de documentação pública |
| Base documental | Markdown, JSONL e PDF | Armazenamento dos conteúdos |
| Processamento | Python | Limpeza e divisão dos documentos |
| Embeddings | Sentence Transformers | Representação vetorial dos textos |
| Modelo semântico | MiniLM multilíngue | Similaridade entre perguntas e documentos |
| Busca lexical | BM25 | Correspondência de palavras e termos técnicos |
| Busca híbrida | BM25 + embeddings | Combinação de relevância lexical e semântica |
| Classificação | MLP 48→24 | Identificação do tema da pergunta |
| Contextualização | Chunk Lookup | Recuperação de trechos vizinhos |
| Interface | Streamlit | Pesquisa e visualização das evidências |

### Modelo de embeddings

Utiliza o modelo:

`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

Esse modelo transforma perguntas e documentos em representações vetoriais, permitindo localizar conteúdos semanticamente relacionados, mesmo quando não utilizam exatamente as mesmas palavras.

O modelo de embeddings é pré-treinado e não é treinado do zero neste projeto.

### Classificador neural MLP

O projeto utiliza uma rede neural MLP com arquitetura 48→24 para classificar o tema provável da pergunta.

O treinamento é realizado com exemplos definidos em `training_examples.jsonl`.

A classificação auxilia na identificação de assuntos como:

- Pix
- Conecta
- Cancelamento
- Chargeback
- Conciliação
- Segurança
- Operação de APIs
- Cielo Smart

A confiança apresentada pela MLP representa a classificação temática, não a probabilidade de uma informação estar tecnicamente correta.

---

## 🔎 Mecanismo de busca

O mecanismo de recuperação combina duas estratégias:

**1. Busca semântica**

Utiliza embeddings para identificar conteúdos relacionados ao significado da pergunta.

**2. Busca lexical**

Utiliza BM25 para identificar correspondências de palavras, expressões e termos técnicos.

**3. Busca híbrida**

Combina os resultados semânticos e lexicais por meio do parâmetro `hybrid_weight`.

Essa combinação busca equilibrar a compreensão contextual com a precisão na localização de nomes de produtos, métodos, parâmetros e funcionalidades.

### Recuperação contextual

Uma das evoluções implementadas foi a recuperação de contexto complementar.

Cada trecho indexado possui metadados que permitem identificar sua origem e posição no documento:

- `document_id`: identifica o documento de origem.
- `chunk_index`: identifica a posição do trecho dentro do documento.

Com essas informações, o mecanismo consegue localizar os trechos imediatamente anterior e posterior ao resultado principal.

O objetivo é preservar a continuidade das informações técnicas e reduzir a perda de contexto causada pela divisão dos documentos.

**Exemplo de funcionamento:**

1. A pergunta é processada.
2. O mecanismo recupera os trechos mais relevantes.
3. Para cada resultado, identifica seu documento de origem.
4. Localiza os chunks vizinhos do mesmo documento.
5. Apresenta o trecho principal e o contexto complementar na interface.

A recuperação contextual não altera a pontuação original da busca e não mistura intencionalmente trechos de documentos diferentes.

---

## 🖥️ Interface da aplicação

A interface foi desenvolvida com Streamlit.

Principais recursos:

- Seleção do ecossistema documental.
- Campo de pesquisa em linguagem natural.
- Controle da quantidade de evidências recuperadas.
- Identificação do tema provável pela MLP.
- Exibição das pontuações semântica e lexical.
- Visualização do trecho principal.
- Visualização do contexto complementar.
- Acesso direto à documentação oficial.
- Aviso quando não existem evidências suficientes.

A aplicação apresenta evidências recuperadas, não respostas geradas por um modelo de linguagem.

---

## 📊 Estado atual do projeto

Última indexação validada do ecossistema Cielo:

| Indicador | Resultado |
|---|---:|
| Trechos indexados | 877 |
| Páginas Markdown coletadas | 100 |
| PDFs coletados | 0 |
| Exemplos de treinamento da MLP | 66 |
| Temas classificados | 8 |
| Acurácia de validação cruzada da MLP | 81,82% |
| Testes automatizados | 19 aprovados |

A acurácia da MLP refere-se exclusivamente à classificação temática nos exemplos avaliados. Não representa a precisão factual da busca.

Os números acima representam uma execução específica da indexação e podem mudar conforme novas coletas e atualizações da documentação.

---

## 🚀 Instalação e execução

### Pré-requisitos

- Python 3.10 ou superior.
- Git.
- Conexão com a internet para instalar depend
