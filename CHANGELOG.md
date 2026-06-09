# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.3] - 2026-06-09
### Changed
- Cores dos badges de status agora são definidas pelo nome do status (não apenas pela `statusCategory` do Jira). Mapeamento: BACKLOG / Aguardando Atendimento / Aguardando Aprovação / Pendente Externo (cinza), Em Andamento / Em Atendimento (azul), Priorizado (âmbar), Cancelado (rose), Concluído (verde). Fallback automático para cor por categoria cobre status não mapeados. Aplicado em todas as abas.

## [0.7.2] - 2026-06-09
### Changed
- Ordenação das queries `pessoais_projetos_tic` e `pessoais_projetos_gpm` simplificada para `ORDER BY updated ASC`, exibindo os chamados menos atualizados primeiro (topo) e os mais novos por último. A mudança é refletida tanto no dashboard web quanto nas mensagens do Teams (que consomem o mesmo `get_dashboard_data()`).

## [0.7.1] - 2026-06-09
### Fixed
- Notificações do navegador agora disparam também com a aba visível, removendo a restrição `document.hidden` que impedia o alerta durante o uso ativo do dashboard.

## [0.7.0] - 2026-06-08
### Added
- Notificações no navegador (Browser Notification API) ao detectar novos chamados ou alterações de status no dashboard, com som de alerta via Web Audio API.
- Badge dinâmico no título da aba (ex: `(3) Jira Dashboard - ATG`) indicando mudanças não visualizadas, resetado ao focar a aba.
- Sistema de diff client-side que compara os dados do último fetch com o novo, ignorando a aba "Finalizados" e a primeira carga.

### Changed
- Otimização do ciclo de polling: detecção de mudanças agora é feita antes da re-renderização, e notificações só disparam quando a aba está em background.
- Reset automático do estado de notificações ao trocar o usuário no input.

## [0.6.1] - 2026-05-12
### Added
- Gráfico de pizza por status individual nas abas Sustentação e Projetos, com botão seletor de tamanho (1 a 5) para ajuste dinâmico da altura do canvas.

## [0.6.0] - 2026-05-12
### Added
- Separação do card "Projetos Ativos" em dois cards independentes: "Projetos Ativos TIC" e "Mudanças Ativas GPM", cada um com sua própria query JQL, exibição em colunas lado a lado e seções separadas no notificador Teams.

### Changed
- Removido `debug=True` do Flask em produção, controlado agora via variável de ambiente `FLASK_DEBUG`.
- Limpeza de comentários obsoletos no `requirements.txt` que referenciavam estrutura legada `services/teams/`.
- Adicionada criação automática do diretório `logs/` no `jira_to_teams.py` para evitar falhas em deploy manual.
- Documentação (`README.md`, `FILE_MAP.md`) atualizada: substituídas referências de "dropdown" para "input de texto" e contagem de queries (6 → 7).

## [0.5.0] - 2026-04-27
### Changed
- **Reestruturação Arquitetural**: Código-fonte migrado para a pasta `src/` e arquivos legados movidos para `docs/`, seguindo as melhores práticas do ecossistema Python.
- Atualização do `Dockerfile` e `docker-compose.yml` para mapear os novos caminhos do backend.
- Simplificação da esteira de deploy no `README.md` (One-liner install).
- Reforço do prompt de IA no `FILE_MAP.md` exigindo o cumprimento estrito do `SKILL.md`.

## [0.4.2] - 2026-04-27
### Fixed
- Reordenação da "Fila DBA Urgente" para priorizar os tickets pelo Tempo de Resolução (SLA), do mais crítico (menor tempo) para o menos crítico.

## [0.4.1] - 2026-04-27
### Fixed
- Correção de sobreposição na fila "Aguardando Atendimento" com a exclusão explícita do status `PENDENTE EXTERNO`.
- Ajuste na fila "SLA Crítico (< 1h)" limitando o escopo estritamente aos status `Em atendimento` e `Aguardando atendimento`.
- Padronização da ordenação das filas ("Aguardando Atendimento", "Sem Interação" e "Projetos Ativos") para `Status`, `Tempo de resolução` (SLA) e Data de Atualização (`updated`).

## [0.4.0] - 2026-04-19
### Added
- Separação de Projetos: Criada uma query específica para projetos (TIC e GPM), excluindo-os nativamente das filas de sustentação diária via JQL `project IN`.
- Novo Layout UX via Sistema de Abas (Tabs): As filas foram divididas em 3 abas (Sustentação & DBA, Projetos Ativos, Finalizados).
- Layout Masonry (Colunas Fluidas): A Aba de Sustentação teve sua grid ajustada para colunas independentes para evitar buracos verticais no agrupamento dos cards.
- Status Dinâmico e Colorido: Extração do `statusCategory` do Jira (new, indeterminate, done) renderizando cores dinâmicas para o badge do status do chamado na tela.
- Contadores dinâmicos ao lado do título de cada aba mostrando a contagem de tickets daquela fila em tempo real.

### Changed
- Refatoração do campo de Usuário (Jira User): O sistema agora recorta apenas a extensão (domínio) e carrega o nome do usuário completo automaticamente ao abrir.
- O card de "Fila DBA Urgente" perdeu sua coluna lateral fixa e foi internalizado na primeira posição da Aba Sustentação.

## [0.3.0] - 2026-04-19
### Added
- Colapsabilidade nos agrupamentos de chamados (Cards) via clique no título com transição de ícones (chevron).
- Textos orientativos (helper texts/tooltips) adicionados aos botões de sincronia e auto-refresh.
- Dropdown dinâmico para controle do tempo de Auto-refresh (5m, 10m, 15m, 30m, 60m).
- 5º Card: "Chamados Finalizados (Este Mês)".

### Changed
- Refatoração do dropdown de Seleção de Usuário (Visão) para um input de texto livre e dinâmico, suportando até 50 caracteres para e-mails longos corporativos.
- Queries JQL atualizadas para alinhar com os "Custom Fields" legados do Jira Corporativo.

## [0.2.0] - 2026-04-13
### Changed
- Refatoração completa da UI: Substituição total do Bootstrap 5 pelo **Tailwind CSS**.
- Implementação de Dark Mode nativo do Tailwind.
- Melhoria na performance de carregamento via otimização de CSS utilitário.
- Atualização do sistema de Grid e Componentes para maior flexibilidade responsiva.

## [0.1.0] - 2026-04-13
### Added
- Inicialização do sistema sob nova arquitetura de Controle de Qualidade (`SKILL.md`) e Controle de Versão (`CHANGELOG.md`).
- Implementação unificada do rodapé (Footer) no Dashboard WEB contendo a respectiva versão semântica de interface.
- Consolidação do backend para validação das chaves do Jira com suporte visual a Dark Theme reativo.
