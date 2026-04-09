Guia de Implantação Orquestrada (Docker) - Autoglass Oracle Auto Grant

Este documento define os procedimentos rigorosos para a conteinerização e implantação do sistema no servidor srv-atlas (10.0.0.83 - Oracle Linux 9.7 ARM64).

Fase 1: Preparação do Ambiente no srv-atlas

Acesse seu servidor via SSH e certifique-se de que o Docker e o Docker Compose estão instalados e operantes.

# Conectando ao servidor
ssh root@10.0.0.83

# Criando o diretório da aplicação no novo disco e caminho especificado
mkdir -p /opt/nexus/ATGGM
cd /opt/nexus/ATGGM


Transfira os seguintes arquivos estritamente para este diretório:

audit.cgi

grant_reporter.sh

grant_manager.sh

Fase 2: Configuração de Credenciais (.env)

Crie o arquivo .env na raiz do diretório /opt/nexus/ATGGM. Nunca adicione este arquivo ao controle de versão (Git).

# /opt/nexus/ATGGM/.env

# Credenciais de Banco de Dados (Apontamento V2 - Banco FREE)
DB_USER=SVC_DBA
DB_PASSWORD=SuaSenhaSeguraAqui
DB_TNS=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=167.234.242.220)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=FREE)))

# Credenciais de Integração Jira
JIRA_SERVER=[https://servicedesk-autoglass.atlassian.net](https://servicedesk-autoglass.atlassian.net)
JIRA_USERNAME=thiago.albuquerque@autoglass.com.br
JIRA_PASSWORD=Sua_Chave_De_Acesso_Aqui


Fase 3: Manifestos de Orquestração (Docker)

Crie os dois arquivos abaixo no mesmo diretório (/opt/nexus/ATGGM). Eles instruem o Docker a construir um servidor Apache autossuficiente com suporte a CGI, Perl, JQ e o Oracle SQL*Plus para arquitetura ARM64.

Arquivo 1: Dockerfile

Crie o arquivo chamado Dockerfile e insira o conteúdo abaixo.

# Utilizando a imagem oficial do Oracle Linux 9 (Compatível com ARM64 do seu srv-atlas)
FROM oraclelinux:9

# Instalação de dependências do sistema: Apache, Perl, JQ e Oracle Instant Client
RUN dnf -y update && \
    dnf -y install httpd perl jq wget tar && \
    dnf -y install oracle-instantclient-release-el9 && \
    dnf -y install oracle-instantclient-sqlplus && \
    dnf clean all

# Configuração do Apache para habilitar CGI
RUN sed -i 's/#LoadModule cgid_module modules\/mod_cgid.so/LoadModule cgid_module modules\/mod_cgid.so/' /etc/httpd/conf/httpd.conf && \
    sed -i 's/Options Indexes FollowSymLinks/Options Indexes FollowSymLinks ExecCGI/' /etc/httpd/conf/httpd.conf && \
    sed -i 's/#AddHandler cgi-script .cgi/AddHandler cgi-script .cgi .pl/' /etc/httpd/conf/httpd.conf

# Preparação de diretórios
RUN mkdir -p /var/www/cgi-bin /usr/local/bin

# Cópia dos artefatos da aplicação
COPY audit.cgi /var/www/cgi-bin/audit.cgi
COPY grant_reporter.sh /usr/local/bin/grant_reporter.sh
COPY grant_manager.sh /usr/local/bin/grant_manager.sh

# Ajuste rigoroso de permissões
RUN chown -R apache:apache /var/www/cgi-bin/ /usr/local/bin/ && \
    chmod 755 /var/www/cgi-bin/audit.cgi && \
    chmod 755 /usr/local/bin/grant_reporter.sh && \
    chmod 755 /usr/local/bin/grant_manager.sh

# Redirecionamento da rota principal para o CGI
RUN echo "RedirectMatch ^/$ /cgi-bin/audit.cgi" > /etc/httpd/conf.d/redirect.conf

# Exposição da porta web
EXPOSE 80

# Comando de inicialização do Apache em foreground
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]


Arquivo 2: docker-compose.yml

Crie o arquivo chamado docker-compose.yml e insira o conteúdo abaixo.

version: '3.8'

services:
  grant-manager-web:
    build: .
    container_name: autoglass_grant_manager
    ports:
      - "80:80"
    env_file:
      - .env
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"


Fase 4: Inicialização e Implantação

Com os arquivos posicionados, execute os comandos de construção da imagem e inicialização do contêiner.

# 1. Garanta que você está no diretório correto
cd /opt/nexus/ATGGM

# 2. Construa e levante o ambiente em background (-d)
docker compose up -d --build

# 3. Verifique a resiliência do contêiner
docker compose ps
docker compose logs -f


Fase 5: Homologação

Abra seu navegador web corporativo.

Acesse o endereço IP da sua máquina virtual: http://10.0.0.83

O Apache redirecionará automaticamente para o script CGI, carregando a interface Dark Mode do "Autoglass Oracle Auto Grant".

A partir deste momento, o contêiner herdará as credenciais de IP (167.234.242.220) e TNS do banco FREE localizadas no .env de /opt/nexus/ATGGM e as repassará para os scripts shell de forma estritamente isolada e segura.