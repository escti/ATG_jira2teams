# Guia de Instalação via Docker - ATG Jira2Teams

Este documento descreve como instalar e configurar o sistema de notificações Jira para Teams no servidor **srvcron** (Oracle Linux 8.10, arquitetura ARM64) utilizando Docker e Docker Compose.

## Pré-requisitos

Antes de iniciar, verifique se os seguintes serviços estão rodando no servidor:

1.  **Docker Engine**: O motor do Docker instalado e em execução.
2.  **Docker Compose**: O gerenciador de orquestração de contêineres.

### Verificação de Instalação

Execute os seguintes comandos para confirmar que os binários estão disponíveis:

```bash
# Verificar versão do Docker
docker --version

# Verificar versão do Docker Compose (ou docker-compose)
docker-compose --version
# Ou, se instalado como binário separado:
docker compose version
```

## Passo 1: Clonagem do Repositório

Navegue até a pasta onde deseja hospedar o projeto (ex: `/home/opc`) e clone o repositório:

```bash
cd ~
git clone https://github.com/escti/ATG_jira2teams.git
cd ATG_jira2teams
```

> **Nota**: Certifique-se de que a pasta `ATG_jira2teams` foi criada e que contém as pastas `services`, `docker-compose.yml` e `.env.example`.

## Passo 2: Configuração das Variáveis de Ambiente

O sistema precisa de credenciais para se conectar ao Jira e ao Microsoft Teams.

1.  Crie o arquivo `.env` copiando o modelo:
    ```bash
    cp .env.example .env
    ```

2.  Edite o arquivo `.env` com suas credenciais reais. Você pode usar `vi` ou `nano`:
    ```bash
    vi .env
    ```

3.  **Atenção**: Modifique as seguintes variáveis (substituindo pelos dados reais):
    - `JIRA_API_TOKEN`: Token de API do usuário do Jira.
    - `JIRA_EMAIL`: Email associado ao token.
    - `JIRA_HOST`: URL do seu servidor Jira (ex: `https://jira.escti.com.br`).
    - `TEAMS_WEBHOOK_URL`: URL do webhook do canal do Microsoft Teams.

    *Exemplo de estrutura:*
    ```env
    JIRA_API_TOKEN=seu_token_aqui
    JIRA_EMAIL=usuario@escti.com
    JIRA_HOST=https://jira.escti.com.br
    TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
    ```

    Salve e feche o arquivo.

## Passo 3: Levantamento dos Contêineres

Execute o comando para iniciar todos os serviços definidos no `docker-compose.yml`:

```bash
docker-compose up -d
```

Isso criará e iniciará os contêineres no modo em segundo plano (`-d`).

## Passo 4: Verificação do Status

Confirme que os contêineres estão saudáveis e rodando:

```bash
docker-compose ps
```

**Saída esperada:**
```text
NAME                    STATUS    PORTS
app_web                 Up       0.0.0.0:5000->5000/tcp
app_teams               Up       0.0.0.0:8080->8080/tcp
jira_service            Up       0.0.0.0:9000->9000/tcp
```

## Passo 5: Acesso aos Serviços

### Acesso ao Dashboard Web
Acesse o painel de monitoramento no navegador:
- **URL**: `http://10.0.0.253:5000`
- **Ação**: Verifique se os tickets do Jira estão sendo listados.

### Execução do Script de Notificação (Teams)
O script de notificação pode ser executado via linha de comando dentro do contêiner ou via cron (se configurado). Para testar manualmente:

```bash
docker-compose exec app_teams python jira_to_teams.py
```

## Passo 6: Log de Eventos

Em caso de problemas, verifique os logs dos contêineres:

```bash
# Logs do serviço Web
docker-compose logs -f app_web

# Logs do serviço Teams
docker-compose logs -f app_teams

# Logs do serviço Jira
docker-compose logs -f jira_service
```

## Dica: Persistência de Dados

Se o `docker-compose.yml` estiver configurado para usar volumes (mapeando uma pasta local para persistir dados), certifique-se de que a pasta no host exista e tenha permissões de leitura/escrita para o usuário `opc`:

```bash
# Exemplo (ajuste o nome do volume conforme o docker-compose.yml)
mkdir -p ~/atg_data
chown opc:opc ~/atg_data
```

---

**Servidor**: `srvcron` (10.0.0.253)  
**OS**: Oracle Linux 8.10 (aarch64)  
**Versão do Script**: 1.0 (Dockerizado)