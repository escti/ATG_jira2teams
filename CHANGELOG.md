# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
