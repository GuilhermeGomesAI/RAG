---
updatedAt: 2026-09-03T18:28:49.000Z
agentTools:
  siteIndex: https://docs.cielo.com.br/llms.txt
  projectIndex: https://docs.cielo.com.br/pix-can-cbk/llms.txt
---

# Cancelar o Webhook.

Endpoint para cancelamento do webhook. Não é a única forma pela qual um webhook pode ser
removido.


# OpenAPI definition

```json
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
    "/webhookrec": {
      "delete": {
        "tags": [
          "WebhookRec"
        ],
        "summary": "Cancelar o Webhook.",
        "description": "Endpoint para cancelamento do webhook. Não é a única forma pela qual um webhook pode ser\nremovido.\n",
        "security": [
          {
            "bearerAuth": []
          }
        ],
        "responses": {
          "204": {
            "description": "Webhook para notificações foi cancelado."
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
```