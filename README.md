"# ATG Jira Monitor - Web & Teams

## 🎯 Visão Geral

Este projeto contém **duas funcionalidades** para monitoramento de chamados do Jira:

1. **Dashboard Web** - Interface gráfica acessível via navegador
2. **Script Teams** - Envio automático de notificações para o Microsoft Teams

---

## 🚀 Funcionalidades

### **1. Dashboard Web**
- Interface fluida com **Sistema de Abas (Tabs)** e layout **Masonry** (Colunas dinâmicas).
- Suporte nativo ao Dark Mode usando Tailwind CSS.
- Abas de monitoramento:
  - 🕒 **Sustentação & DBA**: Aguardando Atendimento, SLA Crítico (< 1h), Sem Interação (+3 dias) e DBA Urgente.
  - 🚀 **Projetos Ativos**: Chamados específicos de escopos de projeto (TIC/GPM).
  - ✅ **Finalizados**: Histórico visual do que foi entregue no mês.
- Multiusuário com input livre de e-mail e auto-refresh dinâmico (5 a 60 minutos).

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

## 🛠️ Instalação (Produção na OCI)

O sistema conta com uma esteira de deploy 100% automatizada. Para instalar ou atualizar o sistema no servidor de produção (Oracle Linux), um humano precisa executar apenas 1 comando:

```bash
curl -sSL https://raw.githubusercontent.com/escti/ATG_jira2teams/main/deploy.sh | bash
```

**O que o script faz sozinho:**
1. Instala Git e Docker (se não existirem)
2. Clona ou sincroniza o repositório (`git reset --hard`)
3. Valida a existência do arquivo `.env` de segurança
4. Destrói containers antigos, recria a build com as novas modificações e limpa o lixo de memória do Docker

*(Atenção: Na primeira vez, o script irá pausar pedindo que você edite o `.env` com seu Token do Jira antes de prosseguir).*

---

## 🛠️ Modo Desenvolvimento Local
Caso não queira rodar em containers para criar testes na própria máquina:
1. `pip install -r requirements.txt`
2. `copy .env.example .env` e o edite.
3. Para UI web: `python src/app.py`
4. Para fluxo bot: `python src/jira_to_teams.py`

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

Para facilitar o entendimento profundo da arquitetura, criamos um mapa detalhado. 
👉 **Consulte o arquivo [FILE_MAP.md](FILE_MAP.md)** para ver a explicação de lógica, funções e métodos de cada um dos arquivos abaixo.

```
ATG_jira2teams/
├── docs/                       # Documentações de setup e versões antigas
├── src/                        # Código-fonte da aplicação
│   ├── app.py                  # Backend Flask (Web)
│   ├── jira_service.py         # Lógica integrada de conexão com Jira
│   ├── jira_to_teams.py        # Loop Bot do Teams
│   └── templates/
│       └── index.html          # Frontend Web
├── docker-compose.yml          # Setup da Stack na OCI
├── Dockerfile                  # Build base para python e deps OCI
├── requirements.txt            # Dependências unificadas Python
├── .env.example                # Exemplo de configuração unificada
├── README.md                   # Documentação Unificada
└── FILE_MAP.md                 # 🗺️ Mapa detalhado de contexto para IA e Devs
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

| Card | Query (simplificada) |
|------|-------|
| **Aguardando** | `assignee = 'user' AND project NOT IN (...) AND statusCategory != Done` |
| **SLA Crítico** | `assignee = 'user' AND "Tempo de resolução" <= remaining("1h")` |
| **Sem Interação** | `assignee = 'user' AND updatedDate <= "-3d"` |
| **Projetos Ativos** | `assignee = 'user' AND project IN (TIC, GPM)` |
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