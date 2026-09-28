# Bot SIARWEB Online

Bot em Python para automatizar a solicitação de refeições no sistema SIARWEB.

## Funcionalidades

* Acessa o SIARWEB automaticamente.
* Realiza o login com matrícula e data de nascimento.
* Autentica o acesso utilizando o PIN.
* Verifica o estado atual das solicitações.
* Solicita almoço e jantar quando necessário.
* Evita solicitar novamente uma refeição que já esteja registrada.
* Confirma o estado final das refeições após o processamento.
* Pode ser executado diretamente pelo GitHub Actions.

## Tecnologias

| Tecnologia                                                  |   Versão | Utilização                                                                    |
| :---------------------------------------------------------: | :------- | ----------------------------------------------------------------------------- |
| [Python](https://www.python.org/)                           |  `3.14+` | Linguagem principal do projeto                                                |
| [uv](https://docs.astral.sh/uv/)                            | `latest` | Gerenciamento do projeto, dependências e ambiente virtual                     |
| [Playwright](https://playwright.dev/python/)                | `1.63.0` | Automação do navegador e interação com o SIARWEB                              |
| [python-dotenv](https://github.com/theskumar/python-dotenv) |  `1.2.3` | Carregamento das configurações e credenciais através de variáveis de ambiente |
| [Chromium](https://www.chromium.org/)                       | `latest` | Navegador utilizado pelo Playwright para executar a automação                 |
| [GitHub Actions](https://github.com/features/actions)       | `latest` | Execução automatizada do bot na nuvem                                         |

## Como utilizar

A forma recomendada de utilizar o bot é através do GitHub Actions. Dessa forma, não é necessário instalar Python, uv, Playwright ou Chromium localmente.

### 1. Faça um Fork

Faça um fork deste repositório para a sua conta do GitHub.

### 2. Configure os Secrets

No seu fork, acesse:

**Settings → Secrets and variables → Actions → New repository secret**

Adicione os seguintes Secrets:

| Name *      | Secret *                                   | Formato         |
| ----------- | ------------------------------------------ | --------------- |
| `MATRICULA` | Matrícula utilizada para acessar o SIARWEB | 1111222AAAA3333 |
| `DATA_NASC` | Data de nascimento utilizada no login      | DDMMAAAA        |
| `PIN`       | PIN de acesso ao SIARWEB                   | 1234            |

> Os valores apresentados na coluna Formato são apenas exemplos e não devem ser utilizados como credenciais.

As credenciais devem ser adicionadas somente como Secrets do GitHub. Não coloque seus dados pessoais diretamente no código-fonte, nos arquivos do projeto ou nos logs.

### 3. Execute o workflow

Depois de configurar os Secrets, acesse a aba **Actions** do seu fork.

Selecione o workflow do bot e clique em:

**Run workflow**

O GitHub Actions irá preparar o ambiente, instalar as dependências necessárias e executar o bot automaticamente.

### 4. Consulte o resultado

Após a execução, abra a execução do workflow para acompanhar o resultado.

O log informará se:

* o login foi realizado;
* o PIN foi autenticado;
* o dashboard foi carregado;
* o almoço já estava solicitado ou foi solicitado;
* o jantar já estava solicitado ou foi solicitado;
* o processo foi concluído.

## Execução local

Para desenvolvimento ou testes, também é possível executar o projeto localmente.

Instale as dependências:

```bash
uv sync
```

Instale o navegador utilizado pelo Playwright:

```bash
uv run playwright install chromium
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis privadas no `.env`:

```env
MATRICULA=
DATA_NASC=
PIN=
```

As URLs do SIARWEB são configuradas através das seguintes variáveis:

```env
SIARWEB_URL=https://siarweb.online/index.html
DASHBOARD_URL=https://siarweb.online/app/dashboard.php
```

Execute o bot com:

```bash
uv run bot-siarweb-online
```

O navegador será aberto durante a execução para acompanhar o processo.

O arquivo `.env` contém informações privadas e não deve ser versionado.

## Fluxo

O bot segue o seguinte fluxo:

1. Acessa a página inicial do SIARWEB.
2. Abre a página de login.
3. Preenche matrícula e data de nascimento.
4. Realiza a autenticação com o PIN.
5. Acessa o dashboard.
6. Verifica as solicitações de almoço e jantar.
7. Solicita somente as refeições que ainda não foram registradas.
8. Recarrega o dashboard e confirma o estado final.

## Segurança

As informações pessoais e de autenticação são armazenadas fora do código-fonte.

Na execução pelo GitHub Actions, as credenciais são fornecidas através dos **GitHub Secrets**.

Na execução local, as credenciais são carregadas através do arquivo `.env`, que está incluído no `.gitignore`.

O arquivo `.env.example` contém apenas a estrutura das configurações e não deve conter valores privados.

Nunca compartilhe ou versione suas credenciais do SIARWEB.

## Status

Projeto em desenvolvimento.

---
