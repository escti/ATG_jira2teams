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

## 🛠️ Instalação (Recomendado via Docker na OCI)

Este projeto é preparado para o Docker Compose, especialmente com host Oracle Linux 8. 

### **1. Clonar o repositório**
No servidor que hospedará a aplicação:
```bash
cd ~
git clone https://github.com/escti/ATG_jira2teams.git
cd ATG_jira2teams
```

### **2. Configurar variáveis de ambiente**
Copie o arquivo de exemplo:
```bash
cp .env.example .env
```
Edite o arquivo `.env` com suas credenciais (ajustando a URL do painel Webhook e conta do JIRA):
```env
JIRA_SERVER=https://jira.suaempresa.com.br
JIRA_USERNAME=usuario@escti.com
JIRA_PASSWORD=seu_token_aqui
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
```

### **3. Iniciar a stack de acompanhamento**
```bash
docker-compose up -d
```
Verifique se tudo está OK com `docker-compose ps`.

---

## 🛠️ Modo Desenvolvimento Local
Caso não queira rodar em containers para criar testes na própria máquina:
1. `pip install -r requirements.txt`
2. `copy .env.example .env` e o edite.
3. Para UI web: `python app.py`
4. Para fluxo bot: `python jira_to_teams.py`

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

### **2. Bot Microsoft Teams**

**Funcionamento em Fundo (Docker):**
Após lançada pela instalação, o Bot passará a rodar automaticamente e não requer ativação manual. 
Sempre que uma hora se passar (entre as 07h e 17h, **de segunda a sexta-feira**) ele baterá automaticamente o relógio interno no minuto `59` para puxar os novos resultados e mandar os Cards.

Cheque a atividade utilizando:
```bash
docker-compose logs -f jira-notifier
```

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
├── jira_service.py             # Lógica integrada de conexão com Jira
├── jira_to_teams.py            # Loop Bot do Teams
├── _old/                       # Pasta com docs e versões antigas de scripts
├── templates/
│   └── index.html              # Frontend Web
├── docker-compose.yml          # Setup da Stack na OCI
├── Dockerfile                  # Build base para python e deps OCI
├── requirements.txt            # Dependências unificadas Python
├── .env.example                # Exemplo de configuração unificada
└── README.md                   # Este arquivo (Documentação Unificada)
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

### **Teams (Bot Automático)**

**Nada é disparado?**
- Verifique se as variáveis de integração estão íntegras e salvas antes do run.
- Lembre-se do loop: Ele enviará as notificações unicamente no minuto `59` de horas entre `07:00` e `17:00`, de **segunda a sexta-feira**. Aos finais de semana ou fora do horário, ele estará apensas hibernando.
- Tente `docker logs jira-notifier` e avalie possíveis erros nos registros internos. Pode ter sido disparada alguma exceção tratada pelas try/excepts durante o último despertar.

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