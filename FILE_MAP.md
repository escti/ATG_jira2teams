# 🗺️ Mapa de Arquivos (Context Map)

> **⚠️ AVISO CRÍTICO PARA IA:** Antes de iniciar qualquer tarefa de codificação, refatoração ou planejamento neste repositório, **VOCÊ DEVE OBRIGATORIAMENTE LER O ARQUIVO `SKILL.md`**. Lá estão as regras intransigentes de arquitetura, UI/UX e controle de versão (SemVer).

Este documento serve como um guia rápido detalhado da estrutura interna do projeto **ATG Jira2Teams**. Seu objetivo principal é fornecer contexto técnico imediato para a IA e desenvolvedores, evitando a necessidade de ler todos os arquivos para entender a arquitetura.

---

## 🖥️ Backend (Python)

### `app.py`
- **Descrição:** Servidor web principal baseado em Flask. Responsável por hospedar a interface web e servir os dados via API.
- **Rotas:**
  - `/`: Renderiza o `index.html`. Lê a variável `JIRA_DASHBOARD_USERS` do `.env` para popular o dropdown de multiusuários.
  - `/api/data`: Endpoint consumido pelo frontend para buscar os chamados atualizados via `jira_service.py`.

### `jira_service.py`
- **Descrição:** Classe de integração e inteligência (`JiraClient`) que faz as chamadas HTTP para a API v3 do Jira Cloud.
- **Lógica Principal:**
  - `run_jql_query()`: Executa queries (tenta endpoint primário e fallback) com tratamento de erro e logs de auditoria no terminal.
  - `get_dashboard_data()`: Centraliza as 4 queries JQL principais do sistema.
  - **Mapeamento de Usuário:** Contém a inteligência que converte o nome curto do dropdown (ex: `thiago`) para o e-mail completo configurado no `.env` (ex: `thiago.albuquerque@...`), garantindo que o Jira sempre encontre o `assignee` correto.

### `jira_to_teams.py`
- **Descrição:** Script autônomo (daemon) para envio de notificações ativas para o Microsoft Teams.
- **Lógica Principal:**
  - Possui um loop infinito (`while True`) restrito a rodar apenas no **minuto 59** de cada hora, entre as **07h e 17h**, de **Segunda a Sexta-feira**.
  - Consome o mesmo método `jira.get_dashboard_data()` da web para garantir paridade de dados e envia as informações formatadas em formato `MessageCard` via webhook.

---

## 🎨 Frontend

### `templates/index.html`
- **Descrição:** Single Page Application (SPA) do Dashboard Web.
- **Tecnologias:** HTML5, Tailwind CSS (via CDN) e Vanilla JavaScript. Sem uso de bibliotecas legadas.
- **Design:** Segue estritamente as regras de UI/UX do `SKILL.md` (Glassmorphism, Dark Mode obrigatório, tipografia moderna).
- **Lógica JS:** Faz pooling via `fetch` para a rota `/api/data`, controla auto-refresh a cada 5 minutos e gerencia os estados de carregamento (Skeleton Loaders) da UI.

---

## ⚙️ Configuração e Infraestrutura

### `.env` / `.env.example`
- **Descrição:** Configuração de credenciais críticas e parâmetros do sistema.
- **Variáveis Principais:** `JIRA_SERVER`, `JIRA_USERNAME`, `JIRA_PASSWORD` (Token de API), `TEAMS_WEBHOOK_URL`, `JIRA_DASHBOARD_USERS`.

### `docker-compose.yml` e `Dockerfile`
- **Descrição:** Orquestração de infraestrutura como código (IaC).
- **Serviços:** Levanta o container Web (Flask na porta 5000) e o serviço `jira-notifier` que roda em background isolado no container.

### `deploy.sh`
- **Descrição:** Script bash utilitário focado em automação de deploy, planejado para instâncias Oracle Linux 8 na nuvem (OCI). Gerencia pulls, builds e monitoramento da stack.

---

## 📜 Governança e Regras

### `SKILL.md`
- **Descrição:** A "Constituição" arquitetural do projeto. Define regras rígidas sobre design (Tailwind CSS obrigatório), segurança (tratamento de erros) e padronizações para qualquer futura atualização do código.

### `CHANGELOG.md`
- **Descrição:** Registro de alterações aderente ao Semantic Versioning (SemVer). Rastreia todas as versões em produção.

### `README.md`
- **Descrição:** Documentação oficial do projeto voltada para a instalação, parametrização e uso geral da ferramenta pelos analistas.
