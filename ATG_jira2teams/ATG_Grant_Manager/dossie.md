Dossiê Técnico: Autoglass Oracle Auto Grant (V2.2)
1. Visão Geral
O Autoglass Oracle Auto Grant é uma solução de governança e automação de privilégios de banco de dados. Ele resolve o problema de "acessos esquecidos" ao implementar grants temporários que se auto-revogam após 15 dias, vinculando cada liberação a um chamado aprovado no Jira.
2. Arquitetura de Sistema
A solução é executada de forma isolada via Docker no servidor srv-atlas (10.0.0.83).
Core: Shell Script (Bash) e Perl.
Runtime: Apache HTTPD (CGI-BIN).
Banco Alvo: Oracle 19c/21c (Instância: FREE).
Orquestração: Docker Compose.
3. Fluxo de Trabalho (Workflow)
Solicitação: O administrador insere o Ticket Jira, Usuário, Objeto e Privilégio na interface Web.
Validação Jira: O sistema consulta a API do Jira. Se o ticket não estiver como "Aprovado" ou "Concluído", a operação é abortada.
Validação de Unicidade: O sistema consulta a tabela SVC_DBA.GRANT_CONTROL. Se o ticket já foi usado para um grant bem-sucedido, a operação é bloqueada (Anti-reuso).
Execução: O Grant é executado no banco via SQL*Plus e registrado simultaneamente na auditoria.
Revogação: Um Job interno do Oracle (DBMS_SCHEDULER) varre a tabela diariamente às 01:00 AM e revoga grants onde SYSDATE > DATA_EXPIRACAO.
4. Segurança e Compliance
Segurança de Credenciais: Nenhuma senha é armazenada em código. Todas as chaves residem no arquivo /opt/nexus/ATGGM/.env, protegido por permissões de sistema.
Princípio do Menor Privilégio: O usuário SVC_DBA é o único com GRANT ANY OBJECT PRIVILEGE, atuando como um proxy controlado.
Auditoria Imutável: Cada tentativa (Erro ou Sucesso) é registrada com timestamp, grantor e log do Oracle.
5. Estrutura de Diretórios (Deploy)
Localização: /opt/nexus/ATGGM
Arquivo
Função
audit.cgi
Interface Web (Frontend)
grant_manager.sh
Lógica de Execução e Validação Jira
grant_reporter.sh
Gerador de Relatório HTML
Dockerfile
Definição da Imagem do Contêiner
docker-compose.yml
Orquestrador do Serviço
.env
Credenciais Sensíveis (Não rastreado no Git)

6. Próximos Passos Recomendados
Implementar chamada AJAX no frontend para evitar o alert() provisório.
Configurar SSL (HTTPS) no Apache do contêiner para proteger o tráfego de rede.
Integrar com o Microsoft Teams para notificar o usuário quando o grant expirar.
