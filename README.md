# 🧠 Cielo Intelligence

**Busca inteligente sobre documentação técnica de instituições de pagamento, utilizando embeddings, redes neurais e recuperação contextual de informações.**

O Cielo Intelligence é um projeto experimental desenvolvido em Python para pesquisar, recuperar e organizar informações presentes na documentação pública oficial da Cielo.

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
- Conexão com a internet para instalar dependências e coletar documentação.

### 1. Clonar o repositório

```bash
git clone https://github.com/GuilhermeGomesAI/cielo-intelligence.git

cd cielo-intelligence
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar ambiente virtual

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux ou macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
pip install -e .
```

### 5. Coletar documentação

```bash
python -m csi crawl cielo --max-pages 100
```

Para uma coleta sem esse limite:

```bash
python -m csi crawl cielo
```

### 6. Construir o índice

```bash
python -m csi index cielo
```

Essa etapa processa os documentos disponíveis, gera os embeddings, treina o classificador temático e grava os artefatos do índice.

### 7. Executar a aplicação

```bash
streamlit run app.py
```

A interface estará disponível normalmente em:

`http://localhost:8501`

---

## 🧪 Testes e validação

O projeto possui testes automatizados utilizando `unittest`.

Para executar:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam funcionalidades como:

- Segurança das URLs coletadas.
- Restrições de domínio.
- Tratamento da documentação.
- Processamento dos documentos.
- Recuperação de informações.
- Recuperação de chunks vizinhos.
- Integridade de funcionalidades essenciais.

Os testes automatizados são executados offline com mecanismos de teste determinísticos.

Eles validam a lógica da aplicação, mas não medem a qualidade real do modelo de embeddings em produção.

### Avaliação de recuperação

Para avaliar o comportamento da busca:

```bash
python -m csi eval cielo -v
```

O projeto também disponibiliza comandos de calibração e treinamento:

```bash
python -m csi calibrate cielo
python -m csi retrain cielo
```

A calibração auxilia na escolha do limite mínimo de pontuação para aceitar evidências.

A pontuação de recuperação representa relevância estimada, não probabilidade de veracidade.

---

## 📁 Estrutura do projeto

```text
cielo-intelligence/
│
├── ecosystems/
│   └── cielo/
│       ├── config.json
│       ├── seed_sources.json
│       ├── seed_knowledge.md
│       ├── training_examples.jsonl
│       └── eval_questions.jsonl
│
├── src/
│   └── csi/
│       ├── config.py
│       ├── crawler.py
│       ├── indexer.py
│       ├── classifier.py
│       ├── search.py
│       ├── evaluate.py
│       └── cli.py
│
├── data/
│   └── cielo/
│       └── arquivos gerados durante a indexação
│
├── docs/
│
├── tests/
│   └── test_core.py
│
├── app.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── .gitignore
```

Os arquivos gerados durante a indexação ficam em `data/` e são tratados como artefatos locais, conforme as regras do `.gitignore`.

---

## 🌐 Expansão para outros ecossistemas

A arquitetura foi desenvolvida para permitir a inclusão de outras fontes documentais.

Além da Cielo, o projeto pode ser adaptado para documentação técnica de outras instituições de pagamento.

Exemplo de expansão:

- Stone
- Outras plataformas de pagamento
- Documentações de APIs
- Portais técnicos de integração

Para adicionar um novo ecossistema, é necessário configurar sua pasta em `ecosystems/`, incluindo os arquivos de configuração, fontes, base-semente, exemplos de treinamento e perguntas de avaliação.

Cada ecossistema possui seu próprio escopo e índice documental.

---

## 🔐 Segurança e responsabilidade

O crawler foi projetado para trabalhar com documentação pública dos domínios configurados.

O projeto não deve receber ou armazenar:

- PAN (número completo de cartão).
- CVV.
- Tokens de autenticação.
- Certificados e chaves privadas.
- Credenciais.
- Dados pessoais ou financeiros de clientes.
- Informações confidenciais de empresas.

A documentação recuperada deve sempre ser conferida na fonte oficial, especialmente quando envolver integrações financeiras, segurança, liquidação e operações de pagamento.

---

## 🛣️ Roadmap

Evoluções planejadas:

- [x] Coleta de documentação pública.
- [x] Processamento e indexação de documentos.
- [x] Embeddings multilíngues.
- [x] Busca híbrida semântica e lexical.
- [x] Classificação temática com MLP.
- [x] Recuperação contextual de chunks vizinhos.
- [x] Interface de pesquisa com Streamlit.
- [x] Exibição de evidências e fontes oficiais.
- [x] Testes automatizados da recuperação contextual.
- [ ] Diversificação dos resultados recuperados.
- [ ] Reranking contextual.
- [ ] Melhorias na avaliação com perguntas validadas por especialistas.
- [ ] Inspeção e processamento de PDFs com tabelas.
- [ ] Manifesto de versões e histórico de coleta.
- [ ] Integração futura com LLM para geração de respostas fundamentadas em evidências e citações obrigatórias.

---

## 👨‍💻 Autor

Desenvolvido por **Guilherme Gomes**.

Entusiasta de Inteligência Artificial, desenvolvimento de software e soluções tecnológicas para resolver problemas reais.

- GitHub: https://github.com/GuilhermeGomesAI
- LinkedIn: https://www.linkedin.com/in/guilherme-gomes-ia/

---

## 📄 Licença

Consulte o arquivo `LICENSE` do repositório para conhecer as condições de utilização e distribuição do projeto.
