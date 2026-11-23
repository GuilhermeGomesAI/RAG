---
updatedAt: 2026-11-09T20:09:35.000Z
agentTools:
  siteIndex: https://docs.cielo.com.br/llms.txt
  projectIndex: https://docs.cielo.com.br/pix-can-cbk/llms.txt
---

# Credenciais e autenticação

Abaixo, você aprende como solicitar credenciais Sandbox e, em seguida, credenciais Produção.

# Solicitação de credenciais Sandbox

Para obter acesso ao ambiente Sandbox, solicite à Cielo, por meio do e‑mail <apipix.suporte@cielo.com.br>, as seguintes credenciais:

* Client ID e Client Secret (utilizados para autenticação via OAuth2);
* Chave Pix transacional (tipo: aleatória).

No ambiente Sandbox, gere uma cobrança e obtenha o Pix copia e cola retornado pela API. Envie esse código por e-mail para <apipix.suporte@cielo.com.br> para que a Cielo efetue o pagamento. Configure um tempo de expiração maior para o Pix copia e cola.

<Callout icon="ℹ️" theme="info">
  API não retorna diretamente uma imagem de QR Code, a API retorna apenas o Pix copia e cola, utilizado para realizar o pagamento. A geração do QR Code a partir desse código é de responsabilidade do parceiro integrador, que deve implementá-la em seu próprio backend.
</Callout>

# Solicitação de credenciais Produção

Para transacionar em nome dos clientes da Cielo, os parceiros devem ter as seguintes chaves do cliente:

* Client ID
* Client Secret
* Chave Pix

<Callout icon="🚧" theme="warn">
  Cada estabelecimento comercial precisa ter credenciais próprias.
</Callout>

Siga o passo-a-passo abaixo para gerar credenciais de Produção:

1. Faça login no site Cielo e clique em **Pix**;
2. No menu à esquerda, selecione a opção **Configurações do Pix**.&#x20;

![](https://files.readme.io/695eac2a52082709536d2deb98eb8a45270223fd58e6f6f7b702a5f5bb6042af-2_blur.png)

3. Clique em **Credenciais do Pix** e, em seguida, em **Criar credencial**.

![](https://files.readme.io/6bc00c0dd1288b8e684bfab8d12a8de817e6a6210e6adf5b9c1aabf1a49c4e27-1_blur.png)

<br />

5. Selecione a **Plataforma parceira**.&#x20;

![](https://files.readme.io/500aec31ef49a48f439c3f92d81326b4df93ac3b756b26447602a8f0b0816d18-3_blur.png)

5. Clique em **Criar**.

![](https://files.readme.io/6f980fd3c26383c73c40958d7a232a13c910fd79880f6f89593e70161bcf9a26-4_blur.png)

<br />

6. Confirme a plataforma selecionada clicando em **Continuar**.
7. Em seguida, aceite os termos e condições para criações de credenciais marcando a caixa e clique e&#x6D;**&#x20;Criar credencial**.

![](https://files.readme.io/91357bcde091269fe45b4682bd406c5a155ab037eac2e8d1d6999f8830bad766-5_blur.png)

8. Complete o processo de autenticação.&#x20;

Pronto! Credencial criada com sucesso. Agora, você pode baixar ou copiar suas credenciais para realizar onboarding no portal parceiro.

![](https://files.readme.io/535da1e7d6d156ce3157a3e621ec81e14963b18bff5b1b8d45e01cee8ba02b6a-blurcredenciais.png)

<br />

<Callout icon="far fa-octagon-exclamation" theme="error">
  As credenciais precisam ser copiadas/baixadas dentro de 3 minutos. Caso contrário, será necessário gerar uma nova credencial.
</Callout>