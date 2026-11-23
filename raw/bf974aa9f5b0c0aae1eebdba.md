---
updatedAt: 2026-09-03T18:28:49.000Z
agentTools:
  siteIndex: https://docs.cielo.com.br/llms.txt
  projectIndex: https://docs.cielo.com.br/pix-can-cbk/llms.txt
---

# Recuperar o payload JSON que representa a configuração da recorrência.

## Endpoint (location) que serve um payload que representa uma recorrência.

No momento em que o usuário pagador efetua a leitura de um QR Code composto gerado pelo recebedor, esta URL será acessada e seu conteúdo consiste em uma estrutura JWS. As informações sobre a segurança no acesso às urls encontram-se no Manual de Segurança do Pix disponível nesse __[link](https://www.bcb.gov.br/estabilidadefinanceira/comunicacaodados)__.


# OpenAPI definition

````json
{
  "openapi": "3.0.1",
  "info": {
    "version": "1.0.4",
    "title": "Cielo - Pix",
    "description": "API para geração de PIX QR CODE<br/><br/><p><strong>Autenticação:</strong><br/><ul><li><p><b>Sandbox:&nbsp;</b><a href=\"https://api2.cielo.com.br/sandbox/v2\">https://api2.cielo.com.br/sandbox/v2</a></p></li><li><p><b>Produção:&nbsp;</b><a href=\"https://api2.cielo.com.br/v2\">https://api2.cielo.com.br/v2</a></p></li></ul><p><strong>Api:</strong><br/><ul><li><p><b>Sandbox:&nbsp;</b><a href=\"https://api2.cielo.com.br/sandbox/cielo-pix/v1\">https://api2.cielo.com.br/sandbox/cielo-pix/v1</a></p></li><li><p><b>Produção:&nbsp;</b><a href=\"https://api-mtls.cielo.com.br/cielo-pix/v1\">https://api-mtls.cielo.com.br/cielo-pix/v1</a></p></li></ul><br/><p><strong>Callback de Notificação:</strong><br/><br/>Na seção <b><i>Webhook</i></b> dentro do método <b><i>Put</b></i>, há uma aba denominada <b><i>Callbacks</i></b>.<p>Nesta aba é definido o callback que será enviado para o endereço cadastrado no webhook.</p>"
  },
  "servers": [
    {
      "url": "https://api2.cielo.com.br/sandbox/cielo-pix/v1",
      "description": "Ambiente de Sandbox."
    },
    {
      "url": "https://api-mtls.cielo.com.br/cielo-pix/v1",
      "description": "Ambiente de Produção."
    }
  ],
  "paths": {
    "/rec/{recUrlAccessToken}": {
      "get": {
        "parameters": [
          {
            "name": "recUrlAccessToken",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "tags": [
          "RecPayload"
        ],
        "summary": "Recuperar o payload JSON que representa a configuração da recorrência.",
        "description": "## Endpoint (location) que serve um payload que representa uma recorrência.\n\nNo momento em que o usuário pagador efetua a leitura de um QR Code composto gerado pelo recebedor, esta URL será acessada e seu conteúdo consiste em uma estrutura JWS. As informações sobre a segurança no acesso às urls encontram-se no Manual de Segurança do Pix disponível nesse __[link](https://www.bcb.gov.br/estabilidadefinanceira/comunicacaodados)__.\n",
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "200": {
            "content": {
              "application/jose": {
                "schema": {
                  "$ref": "#/components/schemas/RecPayload"
                }
              }
            },
            "description": "# Descrição do Retorno\nO retorno desse endpoint é um objeto que apresenta estrutura JWS, conforme especificado no manual de segurança. Segue um exemplo:\n\n```jws\n  eyJ4NXQjUzI1NiI6IkJOVkdUamZsRTVBaUplWGhHbTZSaGtGUXkwQ25pejJXSlF5cTZhQ0pnTFkiLCJqa3UiOiJodHRwczpcL1wvcXItaC5zYW5kYm94LnBpeC5iY2IuZ292LmJyXC9yZXN0XC9qd2tzLmpzb24iLCJraWQiOiJOMjROSVg5R3Z3bm4ycGktV09IOG9RQ2JkSGlaSFdpbnJvWllxZGhxMlYwUENJIiwiYWxnIjoiUlMyNTYifQ.eyJpZFJlYyI6IlJOMTIzNDU2NzgyMDI0MDExNTc3ODI1NDQ1NjEyIiwidmluY3VsbyI6eyJjb250cmF0byI6IjU1ODI2MTAiLCJkZXZlZG9yIjp7ImNwZiI6IjQ1MTY0NjMyNDgxIiwibm9tZSI6IkZ1bGFubyBkZSBUYWwifSwib2JqZXRvIjoiU2VydmnDp28gZGUgU3RyZWFtbWluZyBkZSBNw7pzaWNhLiJ9LCJjYWxlbmRhcmlvIjp7ImRhdGFGaW5hbCI6IjIwMjUtMDQtMDEiLCJkYXRhSW5pY2lhbCI6IjIwMjQtMDQtMDEiLCJwZXJpZGlvY2lkYWRlIjoiTUVOU0FMIn0sInBvbGl0aWNhUmV0ZW50YXRpdmEiOiJOQU9fUEVSTUlURSIsInZhbG9yIjp7InZhbG9yUmVjIjoiMzUuMDAifSwicmVjZWJlZG9yIjp7ImNucGoiOiIyODc2NTAwNzgwMjM3MSIsIm5vbWUiOiJTdGFydHVwIE11c2ljYWwiLCJpc3BiUGFydGljaXBhbnRlIjoiMTIzNDU2NzgifSwiYXR1YWxpemFjYW8iOlt7InN0YXR1cyI6IkNSSUFEQSIsImRhdGEiOiIyMDI0LTAzLTIwVDEwOjEyOjA3LjU2N1oifV19.JQ3nwpN75M7ADuFQD1lAYRU_3QIkU34OCGXcqmn0dmmvl_JYQggZDY-2cN9waqZtf0duJkDs9EcRu-pNZQZlNMjI7DCYCNfXOgiiofdQqMikDh-D6Zq82EkiUqS7cuTg1-GWylCTF9gH6-p_D-dhYPvf-s4FinbjZNwhkX8Sn-OhlLMS8roIWSMjo_J1hN4DdL-Q5zgZBb7Hbt4OZ3CnD1GNbnsdUUyPyy2GfmIUWZEnQ2rY7gVuI7chUAksYeZVaJiH34saBw4Ou8RjHbSGmeWFLmjiTSQYisyQEyotStu6GnHLS36ElNDVlZWOUnb87N3H5FAccWaIQhit3C4wmA\n  ```\nEste objeto JWS assinado deve ser validado pelo pagador. Maiores detalhes técnicos a respeito da especificação\n  de segurança encontram-se no __[Manual de Segurança do Pix](https://www.bcb.gov.br/estabilidadefinanceira/pix)__.\n\n  Conforme pode-se verificar no exemplo acima, o objeto JWS apresenta três fragmentos separados pelo caractere `.` (ponto). São eles: `header`, `payload` e `signature`.\n\n  Em termos de funcionalidade, o fragmento que interessa ao pagador é o `payload`, que apresenta estrutura conforme especificada pelo schema do presente endpoint, contendo detalhes concernentes à recorrência.\n"
          },
          "403": {
            "$ref": "#/components/responses/AcessoNegado"
          },
          "404": {
            "$ref": "#/components/responses/NaoEncontrado"
          },
          "503": {
            "$ref": "#/components/responses/ServicoIndisponivel"
          }
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
      }
    },
    "schemas": {
      "RecPayload": {
        "type": "object",
        "title": "Payload da Recorrência",
        "required": [
          "idRec",
          "atualizacao",
          "recebedor"
        ],
        "description": "Atributos de Configuração de Recorrência",
        "allOf": [
          {
            "type": "object",
            "properties": {
              "idRec": {
                "$ref": "#/components/schemas/RecId"
              }
            }
          },
          {
            "$ref": "#/components/schemas/RecBase"
          },
          {
            "type": "object",
            "properties": {
              "recebedor": {
                "oneOf": [
                  {
                    "$ref": "#/components/schemas/PessoaJuridicaRecorrencia"
                  }
                ],
                "allOf": [
                  {
                    "type": "object",
                    "required": [
                      "ispbParticipante"
                    ],
                    "properties": {
                      "ispbParticipante": {
                        "type": "string",
                        "title": "ISPB do usuário recebedor.",
                        "description": "ISPB do usuário recebedor.",
                        "pattern": "\\d{8}"
                      }
                    }
                  }
                ]
              }
            }
          },
          {
            "$ref": "#/components/schemas/RecConfiguracao"
          },
          {
            "$ref": "#/components/schemas/RecAtualizacao"
          }
        ]
      },
      "RecBase": {
        "title": "Recorrência Base",
        "type": "object",
        "required": [
          "calendario",
          "vinculo"
        ],
        "description": "Atributos de Configuração de Recorrência",
        "properties": {
          "vinculo": {
            "type": "object",
            "title": "Descrição do Objeto da Recorrência",
            "required": [
              "contrato",
              "devedor"
            ],
            "description": "Informações sobre o objeto da recorrência.",
            "properties": {
              "objeto": {
                "type": "string",
                "title": "Identificador do objeto de vínculo",
                "description": "Campo de texto livre para informações referentes ao contrato que permitam ao usuário pagador reconhecer o objeto dos pagamentos periódicos por meio do Pix Automático.",
                "maxLength": 35,
                "example": [
                  "Conta de energia Av. Paulista, 1804",
                  "Serviço de internet banda larga",
                  "Assinatura anual"
                ]
              },
              "devedor": {
                "description": "O objeto devedor organiza as informações sobre o devedor da recorrência.",
                "oneOf": [
                  {
                    "$ref": "#/components/schemas/PessoaFisicaRecorrencia"
                  },
                  {
                    "$ref": "#/components/schemas/PessoaJuridicaRecorrencia"
                  }
                ]
              },
              "contrato": {
                "type": "string",
                "title": "Objeto da autorização",
                "description": "Número, identificador, ou código que representa o objeto da autorização (contrato, pedido etc.).",
                "maxLength": 35
              }
            }
          },
          "calendario": {
            "type": "object",
            "title": "Informações sobre calendário da recorrência",
            "required": [
              "dataInicial",
              "periodicidade"
            ],
            "description": "Informações sobre calendário da recorrência",
            "properties": {
              "dataInicial": {
                "type": "string",
                "format": "date",
                "title": "Data estimada de primeiro pagamento.",
                "description": "Trata-se de uma data, no formato `YYYY-MM-DD`, segundo ISO 8601. Data estimada de primeiro pagamento.",
                "example": "2023-04-01"
              },
              "dataFinal": {
                "type": "string",
                "format": "date",
                "title": "Data final da vigência.",
                "description": "Campo opcional que deve ser preenchido para autorizações com vigência pré-definida, devendo ser compatível com os valores informados em tipoFrequencia e a dataInicialRecorrencia. Não deve ser preenchido para autorizações por tempo indeterminado. Trata-se de uma data, no formato `YYYY-MM-DD`, segundo ISO 8601.",
                "example": "2023-04-01"
              },
              "periodicidade": {
                "type": "string",
                "title": "Periodicidade das cobranças recorrentes.",
                "enum": [
                  "SEMANAL",
                  "MENSAL",
                  "TRIMESTRAL",
                  "SEMESTRAL",
                  "ANUAL"
                ]
              }
            }
          },
          "valor": {
            "type": "object",
            "description": "Valor da recorrência. Informe exatamente um dos campos: `valorRec` (valor fixo) ou `valorMinimoRecebedor` (valor mínimo definido pelo usuário recebedor). A API recusa o objeto vazio e recusa os dois campos preenchidos ao mesmo tempo.",
            "properties": {
              "valorRec": {
                "type": "string",
                "pattern": "\\d{1,10}\\.\\d{2}",
                "title": "Valor da recorrência",
                "description": "Campo opcional, deve ser preenchido apenas quando o valor dos pagamentos for fixo ou não for sujeito a alteração durante a vigência da autorização."
              },
              "valorMinimoRecebedor": {
                "type": "string",
                "pattern": "\\d{1,10}\\.\\d{2}",
                "title": "Valor mínimo da recorrência",
                "description": "Campo opcional. Valor definido pelo usuário recebedor. Se o usuário pagador atribuir um valor máximo para os pagamentos daquela autorização, ele não poderá ser inferior ao piso definido pelo usuário recebedor. Não pode ser preenchido nas autorizações de valor fixo, ou seja, com campo valor preenchido."
              }
            }
          }
        }
      },
      "RecConfiguracao": {
        "type": "object",
        "title": "Configuração da Recorrência",
        "required": [
          "politicaRetentativa"
        ],
        "properties": {
          "politicaRetentativa": {
            "type": "string",
            "title": "Política de retentativa pós vencimento da recorrência",
            "enum": [
              "NAO_PERMITE",
              "PERMITE_3R_7D"
            ]
          }
        }
      },
      "RecId": {
        "type": "string",
        "title": "ID Recorrência",
        "description": "# Identificador da Recorrência\n\nRegra de formação:\n- RAxxxxxxxxyyyyMMddkkkkkkkkkkk (29 caracteres; \"case sensitive\", isso é, diferencia letras maiúsculas e minúsculas), sendo:\n  - \"R\":  fixo (1 caractere). \"R\" para a recorrência criada dentro do Pix;\n  - \"A\": identificação da possibilidade de novas tentativas, sendo possíveis os valores \"R\" ou \"N\" (1 caractere). \"R\" caso a recorrência permita novas tentativas de pagamento pós vencimento, ou \"N\" caso não permita novas tentativas.\n  - \"xxxxxxxx\":  identificação do agente que presta serviço para o usuário recebedor que gerou o <Id>, podendo ser: o ISPB do participante direto, o ISPB do participante indireto ou os 8 primeiros dígitos do CNPJ do prestador de serviço de iniciação (8 caracteres numéricos [0-9]);\n  - \"yyyyMMdd\":  data (8 caracteres) de criação da recorrência;\n  - \"kkkkkkkkkkk\": sequencial criado pelo agente que gerou o <Id> (11 caracteres alfanuméricos [a-z|A-Z|0-9]). Deve ser único dentro de cada \"yyyyMMdd\".\n\nDessa forma, o ID da recorrência deve ser formado de acordo com um dos tipos a seguir:\n- \"RRxxxxxxxxyyyyMMddkkkkkkkkkkk\"; para recorrência criada dentro do Pix e que permite novas tentativas de pagamento pós vencimento; ou\n- \"RNxxxxxxxxyyyyMMddkkkkkkkkkkk\"; para recorrência criada dentro do Pix e que não permite novas tentativas de pagamento pós vencimento.\n",
        "pattern": "[a-zA-Z0-9]{29}",
        "minLength": 29,
        "maxLength": 29,
        "example": "RR1234567820240115abcdefghijk"
      },
      "RecAtualizacao": {
        "type": "object",
        "title": "Histórico de atualização da recorrência.",
        "required": [
          "atualizacao"
        ],
        "properties": {
          "atualizacao": {
            "type": "array",
            "title": "Histórico de Status",
            "description": "Histórico das mudanças de status da recorrência.",
            "items": {
              "type": "object",
              "required": [
                "status",
                "data"
              ],
              "properties": {
                "status": {
                  "type": "string",
                  "title": "Status da recorrência",
                  "description": "Status da recorrência.",
                  "enum": [
                    "CRIADA",
                    "APROVADA",
                    "REJEITADA",
                    "EXPIRADA",
                    "CANCELADA"
                  ]
                },
                "data": {
                  "type": "string",
                  "format": "date-time",
                  "description": "Data e hora do registro de status atualizado. Respeita RFC 3339."
                }
              }
            }
          }
        }
      },
      "PessoaFisicaRecorrencia": {
        "type": "object",
        "required": [
          "cpf",
          "nome"
        ],
        "title": "Pessoa Física",
        "properties": {
          "cpf": {
            "type": "string",
            "title": "CPF",
            "pattern": "/^\\d{11}$/",
            "description": "CPF do usuário."
          },
          "nome": {
            "type": "string",
            "title": "Nome",
            "description": "Nome do usuário.",
            "maxLength": 140
          }
        }
      },
      "PessoaJuridicaRecorrencia": {
        "type": "object",
        "required": [
          "cnpj",
          "nome"
        ],
        "title": "Pessoa Jurídica",
        "properties": {
          "cnpj": {
            "type": "string",
            "title": "CNPJ",
            "pattern": "/^\\d{14}$/",
            "description": "CNPJ do usuário."
          },
          "nome": {
            "type": "string",
            "title": "Nome",
            "description": "Nome do usuário.",
            "maxLength": 140
          }
        }
      },
      "Problema": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "format": "uri",
            "description": "URI de referência que identifica o tipo de problema. De acordo com a RFC 7807.",
            "example": "https://pix.bcb.gov.br/api/v2/error/NaoEncontrado"
          },
          "title": {
            "type": "string",
            "description": "Descrição resumida do problema."
          },
          "status": {
            "type": "integer",
            "description": "Código HTTP do status retornado."
          },
          "detail": {
            "type": "string",
            "description": "Descrição completa do problema."
          }
        }
      }
    },
    "responses": {
      "AcessoNegado": {
        "description": "Requisição de participante autenticado que viola alguma regra de autorização.",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Problema"
            }
          }
        }
      },
      "ServicoIndisponivel": {
        "description": "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Problema"
            }
          }
        }
      },
      "NaoEncontrado": {
        "description": "Recurso solicitado não foi encontrado.",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Problema"
            }
          }
        }
      }
    }
  }
}
````