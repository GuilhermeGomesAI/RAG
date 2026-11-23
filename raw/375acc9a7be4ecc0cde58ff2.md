---
updatedAt: 2026-06-02T14:45:00.000Z
agentTools:
  siteIndex: https://docs.cielo.com.br/llms.txt
  projectIndex: https://docs.cielo.com.br/pix-can-cbk/llms.txt
---

# QR Code composto

Nas jornadas que utilizam QR Code, existem casos em que é empregado o QR Code composto, que oferece um conjunto mais amplo de funcionalidades em comparação ao QR Code estático e ao QR Code dinâmico. A principal diferença desse tipo de QR Code é a presença de uma URL adicional, inserida em um campo específico do payload. Essa URL contém as informações associadas às configurações de recorrência de pagamentos que o usuário recebedor disponibiliza ao usuário pagador.

| Jornada   | Descrição                                      |
| --------- | ---------------------------------------------- |
| Jornada 2 | QR Code apenas com *location* da recorrência   |
| Jornada 3 | QR Code de uma Cob + *location* da recorrência |

AS periodicidades possíveis são:

* Semanal;
* Mensal;
* Trimestral;
* Semestral;
* Anual.

# Política de retentativa

| Política        | Definição                                                                     | Endpoint      |
| --------------- | ----------------------------------------------------------------------------- | ------------- |
| NÃO\_PERMITE    | Não serão autorizadas retentativas após o vencimento                          | • /rec (POST) |
| PERMITE\_3R\_7D | Serão permitidas até 3 tentativas após o vencimento dentro de 7 dias corridos | • /rec (POST) |

# Status de recorrência

| Status    | Definição                                                                            | Endpoint      |
| --------- | ------------------------------------------------------------------------------------ | ------------- |
| CRIADA    | Recorrência criada pelo usuário recebedor                                            | • /cobr (GET) |
| ENVIADA   | Recorrência enviada ao PSP do pagador                                                | • /cobr (GET) |
| RECEBIDA  | Recorrência recebida pelo PSP do pagador                                             | • /cobr (GET) |
| REJEITADA | Recorrência rejeitada pelo usuário pagador, apenas para a jornada 1, via notificação | • /cobr (GET) |
| ACEITA    | Recorrência aceita pelo usuário pagador                                              | • /cobr (GET) |
| EXPIRADA  | Data da vigência da recorrência já expirada                                          | • /cobr (GET) |
| CANCELADA | Recorrência cancelada pelo usuário pagador ou recebedor                              | • /cobr (GET) |

# Tipo de jornada

| tipoJornada           | Definição                                                                                                                                                                                 | Endpoint      |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| JORNADA\_1            | Usuário pagador aceitou a recorrência através de notificação externa ao ecossistema                                                                                                       | • /rec (POST) |
| JORNADA\_2            | Usuário pagador aceitou a recorrência através de leitura de QR Code de recorrência                                                                                                        | • /rec (POST) |
| JORNADA\_3            | Usuário pagador iniciou a recorrência através de leitura de QR Code composto e pagamento de cobrança imediata. O uso desta jornada torna obrigatório o preenchimento de dadosJornada.txid | • /rec (POST) |
| AGUARDANDO\_DEFINICAO | Valor inicial posterior à criação e anterior à ativação da recorrência                                                                                                                    | • /rec (POST) |

# Dados de entrada

| Campo                        | Definição                                                                                                                                                                                                                                                                                                                                                                             | Obrigatório | Tamanho | Tipo        | Exemplo                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------- | ----------- | --------------------------------------------------------------- |
| vinculo                      | Informações sobre o objeto da recorrência.                                                                                                                                                                                                                                                                                                                                            | Sim         | –       | Objeto      | –                                                               |
| objeto (vínculo)             | Identificador do objeto de vínculo.                                                                                                                                                                                                                                                                                                                                                   | Não         | 35      | String      | "Conta de água Av. Brasil, 2804"                                |
| contrato (vínculo)           | Número, identificador ou código que representa o objeto da autorização (contrato, pedido etc.).                                                                                                                                                                                                                                                                                       | Sim         | 35      | String      | ContratoXYZ                                                     |
| devedor (vínculo)            | O objeto devedor organiza as informações sobre o devedor da recorrência.                                                                                                                                                                                                                                                                                                              | Sim         | –       | Objeto      | –                                                               |
| cpf (devedor)                | CPF do usuário. Não pode ser utilizado ao mesmo tempo que o CNPJ.                                                                                                                                                                                                                                                                                                                     | Sim         | 11      | String      | 09591481080 — Pattern: `/^\d{11}$/`                             |
| cnpj (devedor)               | CNPJ do usuário. Não pode ser utilizado ao mesmo tempo que o CPF.                                                                                                                                                                                                                                                                                                                     | Sim         | 14      | String      | 3202386000185 — Pattern: `/^\d{14}$/`                           |
| nome (devedor)               | Nome do usuário.                                                                                                                                                                                                                                                                                                                                                                      | Sim         | 140     | String      | Ciclano de Tal                                                  |
| calendario                   | Informações sobre o calendário de recorrência.                                                                                                                                                                                                                                                                                                                                        | Sim         | –       | Objeto      | –                                                               |
| datainicial (calendário)     | Data no formato YYYY-MM-DD, segundo ISO 8601. Representa a estimativa do primeiro pagamento.                                                                                                                                                                                                                                                                                          | Sim         | –       | String      | 2025-03-01                                                      |
| dataFinal (calendário)       | Campo opcional para autorizações com vigência pré-definida. Compatível com tipoFrequencia e datainicialRecorrencia. Não deve ser preenchido para autorizações de tempo indeterminado. Data ISO 8601 no formato YYYY-MM-DD.                                                                                                                                                            | Não         | –       | String      | 2025-03-01                                                      |
| periodicidade                | Periodicidade das cobranças recorrentes.                                                                                                                                                                                                                                                                                                                                              | Sim         | –       | String ENUM | MENSAL                                                          |
| valor                        | Objeto que agrupa informações de valor.                                                                                                                                                                                                                                                                                                                                               | Não         | –       | Objeto      | –                                                               |
| valorRec (valor)             | Campo opcional. Preenchido apenas quando o valor dos pagamentos é fixo ou não está sujeito a alteração durante a vigência da autorização.                                                                                                                                                                                                                                             | Não         | –       | String      | 100.00 — Pattern: `\d{1,10}\.\d{2}`                             |
| valorMinimoRecebedor (valor) | Campo opcional. Valor definido pelo usuário recebedor. Se o usuário pagador atribuir um valor máximo para os pagamentos daquela autorização, ele não poderá ser inferior ao piso definido pelo usuário recebedor. Não pode ser preenchido nas autorizações de valor fixo, ou seja, com campo valor preenchido.                                                                        | Não         | –       | String      | 100.00 — Pattern: `\d{1,10}\.\d{2}`                             |
| politicaRetentativa          | Política de retentativas pós-vencimento de recorrência. Determinará se após a data de liquidação determinada na cobrança recorrente será autorizada o reagendamento com data superior a data do vencimento. NAO\_PERMITE: Não será autorizado retentativas após o vencimento PERMITE\_3R\_7D: Será permitida até 3 tentativas após o vencimento dentro do período de 7 dias corridos. | Sim         | –       | String ENUM | NAO\_PERMITE                                                    |
| loc                          | Identificador da *location* a ser informada na criação da recorrência.                                                                                                                                                                                                                                                                                                                |             | –       |             | –                                                               |
| recebedor                    | O objeto recebedor organiza as informações sobre o usuário recebedor da recorrência.                                                                                                                                                                                                                                                                                                  | Sim         | –       | Object      | –                                                               |
| cnpj (recebedor)             | CNPJ do usuário recebedor. Não pode ser utilizado ao mesmo tempo que o CPF.                                                                                                                                                                                                                                                                                                           | Sim         | 14      | String      | 32023886000185 — Pattern: `/^\d{14}$/`                          |
| nome (recebedor)             | Nome do usuário recebedor.                                                                                                                                                                                                                                                                                                                                                            | Sim         | 140     | String      | Empresa de Serviços S.A.                                        |
| ativacao                     | Dados relacionados à confirmação da ativação da recorrência.                                                                                                                                                                                                                                                                                                                          | Não         | –       | Object      | –                                                               |
| dadosJornada (ativacao)      | Dado de preenchimento obrigatório quando utilizada a Jornada 3. Este campo deve ser removido pelo PSP Recebedor quando a ativação for realizada pelas jornadas 1, 2 ou 4.                                                                                                                                                                                                             | Não         | –       | Object      | JORNADA\_3                                                      |
| txid (dadosJornada)          | Identificador da transação. O campo txid determina o identificador da transação. O objetivo desse campo é ser um elemento que possibilite ao PSP do recebedor apresentar ao usuário recebedor a funcionalidade de conciliação de pagamentos. Na pacs.008, é referenciado como TransactionIdentification `<txId>` ou idConciliacaoRecebedor.                                           | Não         | –       | String      | 33beb661bed4a4892feff47dbeb2cd5 — Pattern: `[a-zA-Z0-9]{26,35}` |

## Exemplo de entrada

```html
{
  "vinculo": {
    "contrato": "63100862",
    "devedor": {
      "cpf": "45164632481",
      "nome": "Fulano de Tal"
    },
    "objeto": "Serviço de Streamming de Música."
  },
  "calendario": {
    "dataFinal": "2025-04-01",
    "dataInicial": "2024-04-01",
    "periodicidade": "MENSAL"
  },
  "valor": {
    "valorRec": "35.00"
  },
  "politicaRetentativa": "NAO_PERMITE",
  "loc": 108,
  "ativacao": {
    "dadosJornada": {
      "txid": "33beb661beda44a8928fef47dbeb2dc5"
    }
  }
}
```

# Dados de saída

| Campo                       | Definição                                                                                                                                                                                                                                                                                                                                                                             | Obrigatório | Tamanho | Tipo          | Exemplo                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------- | ------------- | -------------------------------------------------------------------- |
| dataFinal (calendario)      | Campo opcional que deve ser preenchido para autorizações com vigência pré-definida, devendo ser compatível com os valores informados em tipoFrequencia e a dataInicialRecorrencia. Não deve ser preenchido para autorizações por tempo indeterminado. Trata-se de uma data, no formato YYYY-MM-DD, seguindo ISO 8601.                                                                 | Não         |         | String        | 2025-03-01                                                           |
| periodicidade               | Periodicidade das cobranças recorrentes.                                                                                                                                                                                                                                                                                                                                              | Sim         |         | String (ENUM) | MENSAL                                                               |
| valor                       | Campo opcional, deve ser preenchido apenas quando o valor dos pagamentos for fixo ou não for sujeito à alteração durante a vigência da autorização.                                                                                                                                                                                                                                   | Não         |         | Object        |                                                                      |
| valorRec (valor)            |                                                                                                                                                                                                                                                                                                                                                                                       | Não         |         | String        | 100.00 <br /> Pattern: \d\{1,10}.\d\{2}                              |
| valorMinimoRecbedor (valor) | Campo opcional. Valor definido pelo usuário recebedor. Se o usuário pagador atribuir um valor máximo para os pagamentos daquela autorização, ele não poderá ser inferior ao piso definido pelo usuário recebedor. Não pode ser preenchido nas autorizações de valor fixo, ou seja, com campo valor preenchido.                                                                        | Não         |         | String        | 100.00 <br /> Pattern: \d\{1,10}.\d\{2}                              |
| politicaRetentativa         | Política de retentativa após vencimento da recorrência. Determinará se após a data de liquidação determinada na cobrança recorrente será autorizado o reagendamento com data superior à data do vencimento. NÃO\_PERMITE: Não será autorizado retentativas após o vencimento PERMITE\_3R\_7D: Será permitida até 3 tentativas após o vencimento dentro do período de 7 dias corridos. | Sim         |         | String (ENUM) | NAO\_PERMITE                                                         |
| loc                         | Location do payload completa                                                                                                                                                                                                                                                                                                                                                          | Não         |         | Object        |                                                                      |
| criacao (loc)               | Data e hora em que o location foi criada. Respeita RFC 3339                                                                                                                                                                                                                                                                                                                           | Não         |         | String        | 2023-12-10T07:10:05.115Z                                             |
| id (loc)                    | Identificador da location a ser informada na criação de uma recorrência                                                                                                                                                                                                                                                                                                               | Não         |         | Int64         | 108                                                                  |
| location (loc)              | Localização do payload a ser informada na criação da recorrência                                                                                                                                                                                                                                                                                                                      | Não         | 77      | String        | pix.example.com/q/v2/rec/2353c790eefb11eaadc10242ac120002            |
| idRec (loc)                 | Identificador da recorrência                                                                                                                                                                                                                                                                                                                                                          | Não         | 29      | String        | RR1234567820240115abcdefghijk <br /> Pattern: \[a-zA-Z0-9]\{29}      |
| atualizacao                 | Histórico das mudanças de status da recorrência                                                                                                                                                                                                                                                                                                                                       | Sim         |         | Object        |                                                                      |
| status                      | Status da recorrência                                                                                                                                                                                                                                                                                                                                                                 | Sim         |         | String (ENUM) | CRIADA                                                               |
| data                        | Data e hora do registro do status atualizado. Respeita RFC 3339                                                                                                                                                                                                                                                                                                                       | Sim         |         | String        | 2023-12-19T12:28:05.230Z                                             |
| recebedor                   | O objeto devedor organiza as informações sobre o devedor da recorrência. CNPJ do usuário. Não pode ser utilizado ao mesmo tempo que o CPF.                                                                                                                                                                                                                                            | Sim         |         | Object        |                                                                      |
| cnpj (recebedor)            |                                                                                                                                                                                                                                                                                                                                                                                       | Sim         | 14      | String        | 8202386000185 <br /> Pattern: ^\d\{14}$                              |
| nome (recebedor)            | Nome do usuário recebedor                                                                                                                                                                                                                                                                                                                                                             | Sim         | 140     | String        | Empresa de Serviços S.A                                              |
| ativacao                    | Dados relacionados à confirmação da ativação da recorrência                                                                                                                                                                                                                                                                                                                           | Não         |         | Object        |                                                                      |
| dadosJornada (ativacao)     | Dado de preenchimento obrigatório quando utilizada a Jornada 3. Este campo deve ser removido pelo PSP Recebedor quando a ativação for realizada pelas jornadas 1, 2 ou 4.                                                                                                                                                                                                             | Não         |         | Object        |                                                                      |
| tipoJornada                 | Dado relacionado ao caminho percorrido pelo processo de adesão à recorrência pelo usuário pagador, os valores possíveis são                                                                                                                                                                                                                                                           | Sim         |         | String (ENUM) | JORNADA\_3                                                           |
| txid (dadosJornada)         | Identificador da transação. O campo txid determina o identificador da transação. O objetivo desse campo é ser um elemento que possibilite ao PSP do recebedor apresentar ao usuário recebedor a funcionalidade de conciliação de pagamentos. Na pacs.008, é referenciado como TransactionIdentification `<txId>` ou idConciliacaoRecebedor.                                           | Não         |         | String        | 33beb661beda44a8928fef47dbeb2dc5 <br />Pattern: \[a-zA-Z0-9]\{26,35} |

## Exemplo de saída

<br />

```html
{
  "idRec": "RN1234567820240115abcdefghijk",
  "vinculo": {
    "contrato": "63100862",
    "devedor": {
      "cpf": "45164632481",
      "nome": "Fulano de Tal"
    },
    "objeto": "Serviço de Streamming de Música."
  },
  "calendario": {
    "dataFinal": "2025-04-01",
    "dataInicial": "2024-04-01",
    "periodicidade": "MENSAL"
  },
  "politicaRetentativa": "NAO_PERMITE",
  "recebedor": {
    "cnpj": "01602606113708",
    "nome": "Empresa de Serviços SA"
  },
  "valor": {
    "valorRec": "35.00"
  },
  "status": "CRIADA",
  "loc": {
    "criacao": "2023-12-10T07:10:05.115Z",
    "id": 108,
    "location": "pix.example.com/qr/v2/rec/2353c790eefb11eaadc10242ac120002",
    "idRec": "RN1234567820240115abcdefghijk"
  },
  "ativacao": {
    "dadosJornada": {
      "tipoJornada": "JORNADA_3",
      "txid": "33beb661beda44a8928fef47dbeb2dc5"
    }
  },
  "atualizacao": [
    {
      "data": "2023-12-19T12:28:05.230Z",
      "nome": "CRIADA"
    }
  ]
}
```

# Códigos de retorno

<br />

| Código HTTP | Descrição Técnica        | Quando ocorre                                                           |
| ----------- | ------------------------ | ----------------------------------------------------------------------- |
| **200**     | Sucesso                  | Requisição processada corretamente.                                     |
| **201**     | Criado                   | Recurso criado com sucesso (ex: recorrência ou cobrança).               |
| **400**     | Requisição inválida      | Campos obrigatórios ausentes, formato inválido, valores fora do padrão. |
| **401**     | Não autorizado           | Token de acesso ausente, inválido ou expirado.                          |
| **403**     | Proibido                 | O `client_id` não tem permissão para acessar o recurso.                 |
| **404**     | Não encontrado           | ID de recorrência, cobrança ou devolução não existe.                    |
| **409**     | Conflito                 | Tentativa de criar uma recorrência ou cobrança com `txid` já existente. |
| **422**     | Entidade não processável | Dados válidos em estrutura, mas com regras de negócio violadas.         |
| **500**     | Erro interno do servidor | Falha inesperada no processamento da requisição.                        |
| **503**     | Serviço indisponível     | API fora do ar, manutenção ou instabilidade temporária.                 |