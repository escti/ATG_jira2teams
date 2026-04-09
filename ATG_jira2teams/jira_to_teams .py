import os
import requests
from datetime import datetime
import pytz
import logging
import json

# Configurar logging para depuração
logging.basicConfig(
    filename='/home/atg/scripts/jira_to_teams.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configurações a partir de variáveis de ambiente
JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
MAX_RESULTS = 100  # Número máximo de issues por query

# Verificar variáveis de ambiente
if not all([JIRA_SERVER, JIRA_USERNAME, JIRA_PASSWORD, TEAMS_WEBHOOK_URL]):
    logging.error("Faltam variáveis de ambiente: JIRA_SERVER, JIRA_USERNAME, JIRA_PASSWORD ou TEAMS_WEBHOOK_URL")
    exit(1)

# Configurar autenticação e endpoints para Jira API v3
JIRA_API_URL_PRIMARY = f"{JIRA_SERVER}/rest/api/3/search/jql"
JIRA_API_URL_FALLBACK = f"{JIRA_SERVER}/rest/api/3/search"
auth = (JIRA_USERNAME, JIRA_PASSWORD)
headers = {"Content-Type": "application/json", "Accept": "application/json"}

# Testar autenticação com o Jira
try:
    response = requests.get(f"{JIRA_SERVER}/rest/api/3/myself", auth=auth, headers=headers)
    response.raise_for_status()
    logging.info("Autenticação com Jira bem-sucedida")
except Exception as e:
    logging.error(f"Falha na autenticação com Jira: {e}")
    exit(1)

# Fuso horário de Brasília (UTC-03:00)
tz = pytz.timezone('America/Sao_Paulo')
current_time = datetime.now(tz).strftime('%d/%m/%Y %H:%M')

# Função para executar query JQL
def run_jql_query(jql, api_url):
    try:
        payload = {
            "jql": jql,
            "maxResults": MAX_RESULTS,
            "fields": ["key", "summary", "updated"]
        }
        logging.info(f"Enviando query para {api_url}: {json.dumps(payload)}")
        response = requests.post(
            api_url,
            auth=auth,
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        issues = response.json().get("issues", [])
        logging.info(f"Query para {api_url} retornou {len(issues)} chamados: {response.text[:200]}...")
        return issues
    except Exception as e:
        logging.error(f"Erro na query para {api_url}: {e}, Resposta: {response.text if 'response' in locals() else 'N/A'}")
        return None

# Queries para o PRIMEIRO card (3 seções)
queries_first_card = [
    {
        "title": "⏳ Chamados Aguardando Atendimento",
        "jql": 'assignee = currentUser() AND statusCategory != Done AND updated <= endOfYear() AND "Tempo de resolução" != paused()'
    },
    {
        "title": "⚠️ Chamados que o SLA Vai Estourar em 1h ou menos",
        "jql": 'assignee = currentUser() AND statusCategory != Done AND updated <= endOfYear() AND "Tempo de resolução" != paused() AND "Tempo de resolução" <= remaining("1h")'
    },
    {
        "title": "🕰️ Chamados Sem Interação a Mais de 3 Dias",
        "jql": 'assignee = currentUser() AND statusCategory != Done and updatedDate <= "-3d" ORDER BY updatedDate asc'
    }
]

# Monta o PRIMEIRO MessageCard
first_message = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "0078D7",  # Azul padrão
    "title": "Seus Chamados no Jira",
    "text": f"Atualizado em: {current_time}",
    "sections": []
}

# Processa cada query do primeiro card
for query in queries_first_card:
    # Tenta a endpoint primária (/rest/api/3/search/jql)
    issues = run_jql_query(query["jql"], JIRA_API_URL_PRIMARY)
    
    # Se falhar, tenta a endpoint fallback (/rest/api/3/search)
    if issues is None:
        logging.info(f"Tentando fallback para {JIRA_API_URL_FALLBACK} na query '{query['title']}'")
        issues = run_jql_query(query["jql"], JIRA_API_URL_FALLBACK)
    
    section = {
        "activityTitle": f"**{query['title']}** ({len(issues) if issues else 'Erro'})",
        "facts": []
    }
    
    if issues is None:
        section["facts"].append({"name": "Status", "value": "Erro na consulta: falha nas duas endpoints"})
    elif not issues:
        section["facts"].append({"name": "Status", "value": "Nenhum chamado encontrado."})
    else:
        for issue in issues:
            key = issue["key"]
            summary = issue["fields"]["summary"]
            updated = issue["fields"]["updated"][:10]
            issue_url = f"{JIRA_SERVER}/browse/{key}"
            
            section["facts"].append({
                "name": f"{key}",
                "value": f"{summary} | Atualizado: {updated} | [Abrir]({issue_url})"
            })
    
    first_message["sections"].append(section)

# Adiciona botão pra ver todos os chamados no Jira
first_message["potentialAction"] = [
    {
        "@type": "OpenUri",
        "name": "Ver todos no Jira",
        "targets": [
            {
                "os": "default",
                "uri": f"{JIRA_SERVER}/issues/?jql=assignee%20%3D%20currentUser()"
            }
        ]
    }
]

# Envia o PRIMEIRO card
try:
    response = requests.post(
        TEAMS_WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        json=first_message
    )
    response.raise_for_status()
    logging.info("Primeiro card enviado com sucesso")
except Exception as e:
    logging.error(f"Erro ao enviar primeiro card: {e}, Resposta: {response.text if 'response' in locals() else 'N/A'}")

# Query para o SEGUNDO card (1 seção - Fila DBA urgente)
query_dba = {
    "title": "🔥 Fila DBA Sem Responsável Que Vai Estourar o SLA em Menos de 1h ou Já Estouraram",
    "jql": 'assignee IS EMPTY AND "Grupo Solucionador[Group Picker (single group)]" = "DC - Banco de Dados (DBA)" AND statusCategory != Done AND ("Tempo de Primeira Resposta" = breached() OR "Tempo de Primeira Resposta" <= remaining("1h"))'
}

# Monta o SEGUNDO MessageCard
second_message = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "FF0000",  # Vermelho para urgência
    "title": "Alertas de Fila DBA no Jira",
    "text": f"Atualizado em: {current_time}",
    "sections": []
}

# Processa a query DBA
issues_dba = run_jql_query(query_dba["jql"], JIRA_API_URL_PRIMARY)
if issues_dba is None:
    logging.info(f"Tentando fallback para {JIRA_API_URL_FALLBACK} na query DBA")
    issues_dba = run_jql_query(query_dba["jql"], JIRA_API_URL_FALLBACK)

section_dba = {
    "activityTitle": f"**{query_dba['title']}** ({len(issues_dba) if issues_dba else 'Erro'})",
    "facts": []
}

if issues_dba is None:
    section_dba["facts"].append({"name": "Status", "value": "Erro na consulta: falha nas duas endpoints"})
elif not issues_dba:
    section_dba["facts"].append({"name": "Status", "value": "Nenhum chamado encontrado."})
else:
    for issue in issues_dba:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        updated = issue["fields"]["updated"][:10]
        issue_url = f"{JIRA_SERVER}/browse/{key}"
        
        section_dba["facts"].append({
            "name": f"{key}",
            "value": f"{summary} | Atualizado: {updated} | [Abrir]({issue_url})"
        })

second_message["sections"].append(section_dba)

# Adiciona botão pra ver a fila DBA no Jira
second_message["potentialAction"] = [
    {
        "@type": "OpenUri",
        "name": "Ver Fila DBA no Jira",
        "targets": [
            {
                "os": "default",
                "uri": f"{JIRA_SERVER}/issues/?jql={query_dba['jql'].replace(' ', '%20')}"
            }
        ]
    }
]

# Envia o SEGUNDO card
try:
    response = requests.post(
        TEAMS_WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        json=second_message
    )
    response.raise_for_status()
    logging.info("Segundo card enviado com sucesso")
except Exception as e:
    logging.error(f"Erro ao enviar segundo card: {e}, Resposta: {response.text if 'response' in locals() else 'N/A'}")

logging.info("Processo concluído")