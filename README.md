"# ATG Jira Monitor - Web & Teams

## 🎯 Visão Geral

Este projeto contém **duas funcionalidades** para monitoramento de chamados do Jira:

1. **Dashboard Web** - Interface gráfica acessível via navegador
2. **Script Teams** - Envio automático de notificações para o Microsoft Teams

---

## 🚀 Funcionalidades

### **1. Dashboard Web**
- Interface moderna baseada em Bootstrap 5
- 4 cartões de monitoramento:
  - ⏳ Chamados Aguardando Atendimento
  - ⚠️ SLA Crítico (< 1h)
  - 🕰️ Sem Interação (+3 dias)
  - 🔥 Fila DBA Urgente
- Multiusuário com dropdown
- Auto-refresh e controles manuais

### **2. Script Teams**
- Envia notificações automáticas para o Microsoft Teams
- Dois cards: Pessoal (3 seções) e Fila DBA (1 seção)
- Execução manual ou agendada via cron/task scheduler

### **3. Controles de Atualização**
- Auto-refresh a cada 5 minutos
- Botão "Atualizar Agora" para refresh manual
- Tratamento de erros com mensagens visíveis na tela

---

## 📋 Pré-requisitos

- Python 3.8+
- Jira Server/DC com API v3
- Flask
- Python-dotenv
- requests

---

## 🛠️ Instalação

### **1. Clonar o repositório**
```bash
cd "C:\APPs\GitHub_Pessoal\ATG\ATG_jira2teams"
```

### **2. Instalar dependências**

**Para Web:**
```bash
pip install -r requirements.txt
```

**Para Teams (separado):**
```bash
cd services/teams
pip install -r requirements.txt
```

### **3. Configurar variáveis de ambiente**

**a) Copie os arquivos de exemplo:**
```bash
copy .env.example .env
copy services/teams/.env.example services/teams/.env
```

**b) Edite os arquivos `.env` com suas credenciais:**

**Web (`.env`):**
```env
# Configuração do Jira
JIRA_SERVER=http://jira.suaempresa.com.br
JIRA_USERNAME=seu_user_jira
JIRA_PASSWORD=sua_senha_jira
```

**Teams (`services/teams/.env`):**
```env
# Configuração do Jira
JIRA_SERVER=http://jira.suaempresa.com.br
JIRA_USERNAME=seu_user_jira
JIRA_PASSWORD=sua_senha_jira

# Configuração do Teams
TEAMS_WEBHOOK_URL=https://yourcompany.webhook.office.com/...
```

### **4. Testar a aplicação**

**Web:**
```bash
python app.py
```
Abra `http://localhost:5000` no navegador

**Teams:**
```bash
cd services/teams
python "jira_to_teams.py"
```
(Execute manualmente ou agende via cron/task scheduler)

---

## 🎮 Como Usar

### **1. Dashboard Web**

**Primeira vez:**
1. Abra a URL do dashboard
2. Aguarde o carregamento automático (5 minutos) ou clique em "Atualizar Agora"

**Alternar usuário:**
1. Clique no dropdown "Usuário" no topo direito
2. Selecione o usuário desejado
3. Os dados atualizam automaticamente para aquele usuário

**Atualização manual:**
1. Clique no botão "Atualizar Agora"
2. Aguarde o spinner de carregamento
3. Dados atualizados!

### **2. Script Teams**

**Execução manual:**
1. Abra o terminal
2. Navegue para a pasta: `cd services/teams`
3. Execute: `python "jira_to_teams.py"`
4. Verifique o log: `type jira_to_teams.log`

**Execução agendada (Windows):**
- Use Task Scheduler para rodar o script periodicamente
- Ou use `taskschd.msc` para criar uma tarefa

**Execução agendada (Linux/Mac):**
- Adicione ao crontab: `crontab -e`
- Exemplo: `*/15 * * * * cd /home/atg/scripts && python jira_to_teams.py >> /home/atg/scripts/cron.log 2>&1`

---

## 🔄 Comparativo: Web vs Teams

| Característica | Web | Teams |
|---------------|-----|-------|
| **Interface** | Navegador (Bootstrap) | Notificação inline |
| **Usuários** | Multiusuário (dropdown) | Geralmente 1 destinatário |
| **Atualização** | Auto-refresh a cada 5 min | Manual ou agendado |
| **Interatividade** | Alta (botões, links) | Baixa (links clicáveis) |
| **Persistência** | Sessão do navegador | Mensagem no chat |
| **Melhor para** | Monitoramento ativo | Alertas rápidos |

---

## 🔧 Estrutura do Projeto

```
ATG_jira2teams/
├── app.py                      # Backend Flask (Web)
├── jira_service.py             # Lógica de conexão com Jira (Web) - *duplicado para facilitar importação*
├── templates/
│   └── index.html              # Frontend Web
├── services/
│   ├── web/                    # # Dependências Web
│   │   └── jira_service.py     # Lógica de conexão com Jira (Web) - *versão organizada*
│   └── teams/                   # Script Teams
│       ├── jira_to_teams.py    # Script para envio ao Teams
│       ├── requirements.txt    # Dependências Teams
│       └── .env.example        # Exemplo de configuração Teams
├── requirements.txt            # Dependências Python (Web)
├── .env.example                # Exemplo de configuração (Web)
└── README.md                   # Este arquivo
```

---

## 📊 Fluxo de Dados

```
Frontend (HTML/JS)
    ↓ (fetch /api/data?user=X)
Backend (Flask app.py)
    ↓ (passa parâmetro user)
JiraService (jira_service.py)
    ↓ (substitui currentUser() por 'user_name')
Jira API
    ↓ (retorna issues)
Frontend (atualiza tabelas)
```

---

## 🔍 Como Funciona o Multiusuário

O sistema substitui dinamicamente a função `currentUser()` do Jira pelo nome do usuário selecionado:

- **Sem parâmetro:** `assignee = currentUser()` → Mostra chamados do usuário logado no Jira
- **Com parâmetro:** `assignee = 'user_name'` → Mostra chamados do usuário específico

### Exemplos de Queries:

| Card | Query |
|------|-------|
| **Aguardando** | `assignee = 'user' AND statusCategory != Done` |
| **SLA Crítico** | `assignee = 'user' AND "Tempo de resolução" <= remaining("1h")` |
| **Sem Interação** | `assignee = 'user' AND updatedDate <= "-3d"` |
| **Fila DBA** | `assignee IS EMPTY AND "Grupo Solucionador" = "DC - Banco de Dados"` |

---

## 🐛 Solução de Problemas

### **Web (Dashboard)**

**Erro: "Erro HTTP: 401 Unauthorized"**
- Verifique as credenciais no arquivo `.env`
- Teste se a autenticação funciona: `http://jira.suaempresa.com.br/rest/api/3/myself`

**Erro: "Erro desconhecido ao carregar dados"**
- Verifique se o Jira está acessível
- Confira se as queries JQL são válidas no seu Jira
- Veja os logs no console do navegador (F12 → Console)

**Dropdown não atualiza dados**
- Verifique se o evento `change` está sendo disparado (console do navegador)
- Abra o DevTools (F12) e veja se há erros na rede

**Nada aparece na tela**
- Verifique se o Jira está retornando dados
- Confirme se o usuário selecionado tem chamados atribuídos

### **Teams (Script)**

**Script não inicia**
- Verifique se todas as variáveis de ambiente estão definidas
- Teste manualmente: `python "jira_to_teams.py"`
- Verifique o log: `type jira_to_teams.log`

**Erro ao enviar para Teams**
- Verifique se o webhook URL está correto
- Teste o webhook diretamente no navegador
- Confira se o usuário tem permissão para receber mensagens

**Log mostra "Erro na consulta"**
- Confira se as queries JQL são válidas no seu Jira
- Teste as queries manualmente no Jira Browser
- Verifique se os campos customizados existem ("Tempo de resolução", "Tempo de Primeira Resposta")

---

## 🔄 Scripts Originais

O projeto mantém os scripts originais em `services/teams/` para envio de notificações ao Teams. Ambos (Web e Teams) usam a mesma lógica de queries, garantindo consistência entre as funcionalidades.

---

## 📝 Autor

Equipe ATG

---

## 📞 Suporte

Para dúvidas ou problemas, verifique:

**Web:**
- Console do navegador (F12)
- Logs do servidor (se rodando em produção)
- Arquivo `.env` está configurado corretamente

**Teams:**
- Log do script: `services/teams/jira_to_teams.log`
- Variáveis de ambiente no `services/teams/.env`
- Webhook URL está ativa e correta

---

## 🔄 Fluxo de Dados

```
┌─────────────┐
│  Jira API   │
└──────┬──────┘
       │
       ├─────────────────────────────┐
       │                             │
       ▼                             ▼
┌─────────────┐              ┌─────────────┐
│  Web        │              │  Teams      │
│  Dashboard  │              │  Script     │
└─────────────┘              └─────────────┘
```