"# ATG Jira Monitor - Web

## 🎯 Visão Geral

Este projeto torna os cards do **Jira → Teams** acessíveis via interface web, permitindo que diferentes usuários acessem seus próprios chamados de forma dinâmica.

---

## 🚀 Funcionalidades

### **1. Dashboard Web**
- Interface moderna baseada em Bootstrap 5
- 4 cartões de monitoramento:
  - ⏳ Chamados Aguardando Atendimento
  - ⚠️ SLA Crítico (< 1h)
  - 🕰️ Sem Interação (+3 dias)
  - 🔥 Fila DBA Urgente

### **2. Multiusuário**
- Dropdown para alternar entre diferentes usuários
- Cada usuário vê apenas seus próprios chamados (baseado em `assignee`)
- Fila DBA é compartilhada entre todos

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
```bash
pip install -r requirements.txt
```

### **3. Configurar variáveis de ambiente**

**a) Copie o arquivo de exemplo:**
```bash
copy .env.example .env
```

**b) Edite o arquivo `.env` com suas credenciais:**
```env
# Configuração do Jira
JIRA_SERVER=http://jira.suaempresa.com.br
JIRA_USERNAME=seu_user_jira
JIRA_PASSWORD=sua_senha_jira

# Configuração do Teams (opcional - para script original)
TEAMS_WEBHOOK_URL=https://yourcompany.webhook.office.com/...
```

### **4. Testar a aplicação**
```bash
python app.py
```

### **5. Acessar o dashboard**
Abra `http://localhost:5000` no seu navegador

---

## 🎮 Como Usar

### **Primeira vez:**
1. Abra a URL do dashboard
2. Aguarde o carregamento automático (5 minutos) ou clique em "Atualizar Agora"

### **Alternar usuário:**
1. Clique no dropdown "Usuário" no topo direito
2. Selecione o usuário desejado
3. Os dados atualizam automaticamente para aquele usuário

### **Atualização manual:**
1. Clique no botão "Atualizar Agora"
2. Aguarde o spinner de carregamento
3. Dados atualizados!

---

## 🔧 Estrutura do Projeto

```
ATG_jira2teams/
├── app.py                      # Backend Flask
├── jira_service.py             # Lógica de conexão com Jira
├── jira_to_teams.py            # Script original para Teams
├── templates/
│   └── index.html              # Frontend
├── static/                     # Estáticos (se necessário)
├── requirements.txt            # Dependências Python
├── .env.example                # Exemplo de configuração
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

### **Erro: "Erro HTTP: 401 Unauthorized"**
- Verifique as credenciais no arquivo `.env`
- Teste se a autenticação funciona: `http://jira.suaempresa.com.br/rest/api/3/myself`

### **Erro: "Erro desconhecido ao carregar dados"**
- Verifique se o Jira está acessível
- Confira se as queries JQL são válidas no seu Jira
- Veja os logs no console do navegador (F12 → Console)

### **Dropdown não atualiza dados**
- Verifique se o evento `change` está sendo disparado (console do navegador)
- Abra o DevTools (F12) e veja se há erros na rede

### **Nada aparece na tela**
- Verifique se o Jira está retornando dados
- Confirme se o usuário selecionado tem chamados atribuídos

---

## 🔄 Scripts Originais

O projeto mantém o script original `jira_to_teams.py` para envio de notificações ao Teams. Ambos usam a mesma lógica de queries, garantindo consistência entre web e Teams.

---

## 📝 Autor

Equipe ATG

---

## 📞 Suporte

Para dúvidas ou problemas, verifique:
- Console do navegador (F12)
- Logs do servidor (se rodando em produção)
- Arquivo `.env` está configurado corretamente