# 🗺️ Mapa de Arquivos (Context Map)

> **⚠️ AVISO CRÍTICO PARA IA:** Antes de iniciar qualquer tarefa de codificação, refatoração ou planejamento neste repositório, **VOCÊ DEVE OBRIGATORIAMENTE LER AS SKILLS EM `.opencode/skills/*/SKILL.md` COMO SUA BÍBLIA ABSOLUTA**. Lá estão as regras intransigentes de arquitetura, UI/UX e controle de versão (SemVer), divididas em skills por domínio (`ui-ux`, `backend`, `versioning`), que não podem ser violadas sob nenhuma hipótese.

Este documento serve como um guia rápido detalhado da estrutura interna do projeto **ATG Jira2Teams**. Seu objetivo principal é fornecer contexto técnico imediato para a IA e desenvolvedores, evitando a necessidade de ler todos os arquivos para entender a arquitetura.

---

## 🖥️ Backend (Python)

### `src/app.py`
- **Descrição:** Servidor web principal baseado em Flask. Responsável por hospedar a interface web e servir os dados via API.
- **Rotas:**
  - `/`: Renderiza o `index.html`. Extrai inteligentemente o prefixo do `JIRA_USERNAME` para não forçar o usuário a digitar na primeira carga.
  - `/api/data`: Endpoint consumido pelo frontend para buscar os chamados atualizados via `jira_service.py`.

### `src/jira_service.py`
- **Descrição:** Classe de integração e inteligência (`JiraClient`) que faz as chamadas HTTP para a API v3 do Jira Cloud.
- **Lógica Principal:**
  - `run_jql_query()`: Executa queries (tenta endpoint primário e fallback) com tratamento de erro e logs de auditoria no terminal.
  - `get_dashboard_data()`: Centraliza as 7 queries JQL principais do sistema (Sustentação, SLA, Finalizados, Sem Interação, DBA, Projetos TIC e Projetos GPM) e injeta o "statusCategory" dinamicamente no retorno. A query SLA (pessoais_sla_critico) ainda roda internamente para alimentar badges ⏱ no card "Aguardando Atendimento". A query DBA filtra por SLA de primeira resposta (`cf[10321]`) ≤ 1h e não pausado.
  - **Mapeamento de Usuário:** O sistema agora é dinâmico, recebendo o prefixo do e-mail ou e-mail completo via input de texto livre para mapear o `assignee` com precisão, ao invés de usar dropdowns estáticos.

### `src/jira_to_teams.py`
- **Descrição:** Script autônomo (daemon) para envio de notificações ativas para o Microsoft Teams.
- **Lógica Principal:**
  - Possui um loop infinito (`while True`) restrito a rodar apenas no **minuto 59** de cada hora, entre as **07h e 17h**, de **Segunda a Sexta-feira**.
  - Consome o mesmo método `jira.get_dashboard_data()` da web para garantir paridade de dados e envia as informações formatadas em formato `MessageCard` via webhook.

---

## 🎨 Frontend

### `src/templates/index.html`
- **Descrição:** Single Page Application (SPA) do Dashboard Web.
- **Tecnologias:** HTML5, Tailwind CSS (via CDN) e Vanilla JavaScript. Sem uso de bibliotecas legadas.
- **Design e UI/UX:** 
  - Segue estritamente as regras de UI/UX do `SKILL.md` (Glassmorphism, Dark Mode obrigatório, tipografia moderna).
  - Possui um inovador **Sistema de Abas (Tabs)** dinâmicas e Layout **Masonry** via CSS Columns, evitando que o empilhamento vertical prejudique o layout.
  - Apresenta interações inteligentes como contadores em tempo real e tags de status coloridas por nome do status (ex: Em Andamento azul, Cancelado rose, Concluído verde) com fallback automático por categoria do Jira.
  - Gráfico de pizza (Chart.js) por status individual no topo das abas Sustentação e Projetos, com botões 1 a 5 para ajuste dinâmico de tamanho.
- **Lógica JS:** Faz pooling via `fetch` para a rota `/api/data`, controla auto-refresh dinâmico (5 a 60min), gerencia os estados de carregamento e renderiza gráficos interativos com Chart.js.

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

### `.opencode/skills/`
- **Descrição:** Skills do OpenCode que definem as regras de arquitetura, divididas em:
  - `ui-ux/` — Design (Glassmorphism, Dark Mode, Tailwind, paleta de cores, acessibilidade)
  - `backend/` — Tratamento de erros (try/catch, logging)
  - `versioning/` — Controle de versão (SemVer, changelog, footer, commits em pt-br)
  Consulte os `SKILL.md` dentro de cada pasta.

### `CHANGELOG.md`
- **Descrição:** Registro de alterações aderente ao Semantic Versioning (SemVer). Rastreia todas as versões em produção.

### `README.md`
- **Descrição:** Documentação oficial do projeto voltada para a instalação, parametrização e uso geral da ferramenta pelos analistas.
