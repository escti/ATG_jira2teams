Changelog

All notable changes to this project will be documented in this file.
The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.

[v0.2.2] - 2026-03-31

Changed

Migração do diretório de implantação base para /opt/nexus/ATGGM.

Atualização da string de conexão do banco de dados (TNS) para apontar para a instância FREE no IP 167.234.242.220.

Atualização do rodapé da interface UI para refletir a nova versão (v0.2.2).

[v0.2.1] - 2026-03-30

Added

Módulo de integração com API do Jira para validação de chamados via cURL e jq no grant_manager.sh.

Regra de negócio para "Single-use Token" (um grant com sucesso por chamado).

Nova coluna CHAMADO_JIRA e índice IDX_GRANT_JIRA aplicados na DDL da tabela SVC_DBA.GRANT_CONTROL.

Changed

Refatoração total do script executável para suportar transações PL/SQL em bloco.

Security

Isolamento de todas as credenciais (DB e Jira) em variáveis de ambiente.