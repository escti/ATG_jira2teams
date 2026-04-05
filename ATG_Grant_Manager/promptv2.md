Prompt de Engenharia: Replicação do Autoglass Oracle Auto Grant (v0.2.2)

Objetivo: Reconstruir do zero um sistema de governança de acessos temporários para Oracle.

Contexto Técnico:

Plataforma: Docker em Oracle Linux 9.7 (Arquitetura ARM64).

Banco de Dados: Oracle (Instância 'FREE', IP '167.234.242.220').

Integração: API do Jira (Atlassian) para validação de status de aprovação.

Frontend: CGI Perl com UI baseada em Tailwind CSS (Dark Mode obrigatório).

Diretório de Deploy: /opt/nexus/ATGGM.

Requisitos de Software (O que deve ser gerado):

SKILL.md: Defina as regras de ouro: Dark Mode obrigatório, proibição de scrollbars nativas, uso único de tickets Jira, validação de formato SCHEMA.TABELA, e expiração automática de 15 dias.

CHANGELOG.md: Documente a evolução da v0.1.0 (POC) até a v0.2.2 (Docker, Jira Integration, ARM64, Path /opt/nexus/ATGGM).

01_create_DbObjects.sql: DDL completa. Crie o usuário SVC_DBA, a tabela GRANT_CONTROL com coluna CHAMADO_JIRA, índice de unicidade lógica para tickets com status 'SUCESSO', e um DBMS_SCHEDULER job que execute o revoke diário.

grant_manager.sh: Script Shell que:

Carregue credenciais de um arquivo .env.

Valide o ticket no Jira via curl e jq (Status: Aprovado/Done/Concluído).

Verifique no Oracle se o ticket já foi usado com sucesso.

Execute o GRANT e o INSERT de auditoria em um único bloco transacional PL/SQL.

grant_reporter.sh: Script que extraia os dados da tabela e gere linhas <tr> HTML com estilização Tailwind (Badges para status).

audit.cgi: Interface Perl que renderize o Dashboard Dark Mode, inclua DataTables, e possua um formulário funcional para entrada de novos Grants.

Dockerfile & docker-compose.yml: Configuração para oraclelinux:9 instalando httpd, perl, jq e o oracle-instantclient-sqlplus.

Diretriz Visual:
O sistema deve ser profissional, limpo, responsivo e exibir a versão v0.2.2 no rodapé. O nome oficial é "Autoglass Oracle Auto Grant".