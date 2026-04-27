# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
