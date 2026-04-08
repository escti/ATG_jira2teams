# Jira to Teams Notifier (ATG_jira2teams)

Este repositório contém um script Python automatizado para monitorar chamados no Jira e enviar notificações em tempo real para canais do Microsoft Teams via Webhooks. O objetivo é aumentar a visibilidade de chamados críticos, SLAs prestes a vencer e pendências de interação.

## 🚀 Funcionalidades

O script envia dois cartões de mensagem distintos:

### 1. Resumo de Chamados Pessoais
Monitora os chamados atribuídos ao usuário (`currentUser()`):
- **⏳ Aguardando Atendimento**: Chamados abertos e não pausados.
- **⚠️ SLA Crítico**: Chamados com resolução prevista para menos de 1 hora.
- **🕰️ Sem Interação**: Chamados sem atualização há mais de 3 dias.

### 2. Alerta de Fila DBA (Urgente)
Monitora a fila de Banco de Dados (`DC - Banco de Dados (DBA)`):
- **🔥 Fila Não Atribuída**: Identifica chamados sem responsável que já estouraram o SLA de primeira resposta ou que irão estourar em menos de 1 hora.

## 🛠️ Pré-requisitos

- **Python 3.9+**
- **Bibliotecas**: `requests`, `pytz`, `flask`, `python-dotenv`
- **Acessos**:
  - Conta no Jira (API Token)
  - URL de Webhook do Microsoft Teams

## ⚙️ Configuração

O script utiliza variáveis de ambiente para manter as credenciais seguras. As seguintes variáveis devem ser configuradas:

| Variável | Descrição |
| :--- | :--- |
| `JIRA_SERVER` | URL da sua instância Jira (ex: `https://empresa.atlassian.net`) |
| `JIRA_USERNAME` | Seu e-mail de acesso ao Jira |
| `JIRA_PASSWORD` | Seu API Token do Jira |
| `TEAMS_WEBHOOK_URL` | URL do Webhook do canal do Teams |

## 🚀 Instalação e Execução

### Script CLI (Notificações no Teams)
1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd ATG_jira2teams
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute manualmente para teste**:
   ```bash
   python3 jira_to_teams.py
   ```

### Versão Web (Dashboard)
Para rodar a interface visual:
```bash
python3 app.py
```
Acesse no navegador: `http://localhost:5000`

