Passo a passo:

Esta solução é dividida em:

Camada de Banco de Dados: DDL, Permissões e Job de Revogação Automática.

Camada de Servidor Web: Configuração básica do Apache para executar Shell Scripts.

Camada de Aplicação: O script grant_manager.sh (backend) e o interface.cgi (frontend).

1. Preparação do Banco de Dados
Primeiro, precisamos preparar o usuário SVC_DBA e a tabela de controle. O usuário precisa de privilégios elevados para conceder grants em nome de outros owners (GRANT ANY PRIVILEGE ou GRANT ANY OBJECT PRIVILEGE com WITH ADMIN OPTION é perigoso, então, idealmente, o SVC_DBA deve ter permissões explícitas ou ser um usuário administrativo contido).

Assumirei que SVC_DBA tem os privilégios necessários.

1.1. DDL da Tabela SVC_DBA.GRANT_CONTROL
Aqui utilizamos uma SEQUENCE para o ID e definimos DATA_EXPIRACAO com um valor default de 15 dias a partir da criação.

Execute o script "CREATE_TABLE_SVC_DBA.GRANT_CONTROL.sql" no banco alvo.

1.2. Automação do Revoke (Job no Banco)
O Shell Script realiza o Grant. Para garantir o Revoke após 15 dias, a melhor prática no Oracle é usar o DBMS_SCHEDULER. Um script externo via cron é menos seguro e dependente do SO.

Execute o script "SVC_DBA.JOB_AUTO_REVOKE_GRANTS.sql"

2. Configuração do Servidor Web (Oracle Linux 8)
Para que o usuário acesse via Chrome/Firefox, instalaremos o Apache.

# 2.0.1
yum update -y;yum upgrade -y;

# 2.1. Instalar Apache
dnf install -y httpd

# 2.2. Habilitar e Iniciar
systemctl enable --now httpd

# 2.3. Liberar Firewall (Porta 80)
firewall-cmd --permanent --add-service=http
firewall-cmd --reload

# 2.4. Configurar SELinux para permitir que o Apache conecte no Oracle
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_can_network_connect_db 1

A pasta padrão para scripts CGI geralmente é /var/www/cgi-bin/. Garantiremos que os scripts criados lá tenham permissão de execução.

3. Script de Backend (grant_manager.sh)
Este é o "motor" do sistema. Ele aceita parâmetros posicionais ou variáveis de ambiente. Por segurança e para atender ao requisito, ele contém as credenciais (hardcoded).

Caminho do arquivo: /usr/local/bin/grant_manager.sh 
Permissões: chmod +x /usr/local/bin/grant_manager.sh

4. Front-End (Interface Web CGI)
Este script gera o HTML e chama o script backend.

Caminho do arquivo: /var/www/cgi-bin/index.cgi 
Permissões: chmod +x /var/www/cgi-bin/index.cgi

Nota: No Oracle Linux, o SELinux pode bloquear conexões de scripts CGI ao Oracle. Se tiver problemas, verifique setsebool -P httpd_can_network_connect_db 1.

5. Aplicação das Permissões de Segurança (Crucial)
Como estamos lidando com senhas hardcoded, as permissões de arquivo são sua única defesa no sistema operacional. Execute os comandos abaixo no seu servidor Oracle Linux 8.

# 1. Definir ownership: o arquivo pertence ao root, mas o grupo do apache pode ler/executar
chown root:apache /usr/local/bin/grant_manager.sh
chown root:apache /var/www/cgi-bin/index.cgi

# 2. Restringir Backend (grant_manager.sh)
# 750: Root faz tudo, Grupo (apache) lê e executa, Outros não fazem nada.
chmod 750 /usr/local/bin/grant_manager.sh

# 3. Restringir Frontend
chmod 755 /var/www/cgi-bin/index.cgi

# 4. SELinux (Obrigatório no Oracle Linux 8 se estiver Enforcing)
# Permite que o Apache conecte na rede (para falar com o listener Oracle)
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_can_network_connect_db 1

# 5. Teste de Segurança
# Tente ler o arquivo como um usuário comum (não root, não apache). Deve dar "Permission denied".
su - usuario_comum -c "cat /usr/local/bin/grant_manager.sh"

6. Resumo da Operação e Fluxo
O usuário acessa http://<IP-DO-SERVIDOR>/cgi-bin/index.cgi.

Preenche o formulário.

Ao clicar em "Executar Grant", o Apache passa os dados para o script index.cgi.

O index.cgi limpa os inputs e chama /usr/local/bin/grant_manager.sh.

O grant_manager.sh conecta no Oracle (TNS DELTA1) com as credenciais fixas.

O script tenta executar o GRANT e, em seguida, faz o INSERT na tabela GRANT_CONTROL.

Se tudo der certo, o status SUCESSO é gravado. Se falhar (ex: tabela não existe), o status ERRO e a mensagem do Oracle (ORA-XXXX) são gravados.

O resultado volta para o navegador.

15 dias depois: O Job SVC_DBA.JOB_AUTO_REVOKE_GRANTS roda automaticamente no banco, revoga o acesso e atualiza o status para REVOGADO.

##################
PLUS
##################
1. Backend de Relatório: grant_reporter.sh
Este script é responsável por formatar os dados brutos do Oracle em HTML. Usaremos lógica condicional no SQL para aplicar classes CSS (Badges) dependendo do Status.

Caminho: /usr/local/bin/grant_reporter.sh 
Permissões: chmod 750 (root:apache)

2. Frontend de Auditoria: audit.cgi
Este script monta a "casca" da página. Incluí o DataTables e jQuery (via CDN) para transformar uma tabela HTML simples em uma tabela interativa poderosa com busca e paginação, sem esforço adicional de programação.

Caminho: /var/www/cgi-bin/audit.cgi 
Permissões: chmod 755

3. Ajuste de Permissões (Segurança)
Assim como fizemos anteriormente, precisamos garantir que o Apache consiga executar o script backend, mas que ele permaneça seguro.

Execute como root:
# 1. Definir ownership
chown root:apache /usr/local/bin/grant_reporter.sh
chown root:apache /var/www/cgi-bin/audit.cgi

# 2. Permissões Restritas (Backend)
chmod 750 /usr/local/bin/grant_reporter.sh

# 3. Permissões de Execução Web (Frontend)
chmod 755 /var/www/cgi-bin/audit.cgi

##################
📍 Parte 5: Teste Final
##################
Abra o navegador e acesse: http://137.131.239.145/cgi-bin/index.cgi.

Preencha com um teste válido (ex: Usuario SCOTT, Objeto HR.COUNTRIES).

Clique em Conceder Acesso.

Deverá aparecer a mensagem verde de Sucesso.

Clique no botão Ver Auditoria para confirmar o registro na tabela.