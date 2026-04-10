import os
import requests
from datetime import datetime
import pytz
import logging
import json
from jira_service import JiraClient

# Configurar logging
logging.basicConfig(
    filename='logs/jira_to_teams.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
JIRA_SERVER = os.getenv('JIRA_SERVER')

if not TEAMS_WEBHOOK_URL:
    logging.error("Variável TEAMS_WEBHOOK_URL não configurada")
    exit(1)

jira = JiraClient()

# Fuso horário de Brasília
tz = pytz.timezone('America/Sao_Paulo')
current_time = datetime.now(tz).strftime('%d/%m/%Y %H:%M')

def send_to_teams(payload):
    try:
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(f"Erro ao enviar para o Teams: {e}")
        return False

# Obter dados do Jira
data = jira.get_dashboard_data()

# --- PRIMEIRO CARD (Pessoais) ---
first_message = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "0078D7",
    "title": "Seus Chamados no Jira",
    "text": f"Atualizado em: {current_time}",
    "sections": []
}

sections_config = [
    {"key": "pessoais_aguardando", "title": "⏳ Chamados Aguardando Atendimento"},
    {"key": "pessoais_sla_critico", "title": "⚠️ Chamados que o SLA Vai Estourar em 1h ou menos"},
    {"key": "pessoais_sem_interacao", "title": "🕰️ Chamados Sem Interação a Mais de 3 Dias"}
]

for config in sections_config:
    issues = data.get(config["key"], [])
    section = {
        "activityTitle": f"**{config['title']}** ({len(issues)})",
        "facts": []
    }
    
    if not issues:
        section["facts"].append({"name": "Status", "value": "Nenhum chamado encontrado."})
    else:
        for issue in issues:
            section["facts"].append({
                "name": issue["key"],
                "value": f"{issue['summary']} | Atualizado: {issue['updated']} | [Abrir]({issue['url']})"
            })
    first_message["sections"].append(section)

first_message["potentialAction"] = [{
    "@type": "OpenUri",
    "name": "Ver todos no Jira",
    "targets": [{"os": "default", "uri": f"{JIRA_SERVER}/issues/?jql=assignee%20%3D%20currentUser()"}]
}]

send_to_teams(first_message)

# --- SEGUNDO CARD (DBA) ---
dba_issues = data.get("dba_urgente", [])
second_message = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "FF0000",
    "title": "Alertas de Fila DBA no Jira",
    "text": f"Atualizado em: {current_time}",
    "sections": [{
        "activityTitle": f"**🔥 Fila DBA Sem Responsável (SLA Crítico)** ({len(dba_issues)})",
        "facts": []
    }]
}

if not dba_issues:
    second_message["sections"][0]["facts"].append({"name": "Status", "value": "Nenhum chamado encontrado."})
else:
    for issue in dba_issues:
        second_message["sections"][0]["facts"].append({
            "name": issue["key"],
            "value": f"{issue['summary']} | Atualizado: {issue['updated']} | [Abrir]({issue['url']})"
        })

second_message["potentialAction"] = [{
    "@type": "OpenUri",
    "name": "Ver Fila DBA no Jira",
    "targets": [{"os": "default", "uri": f"{JIRA_SERVER}/issues/?jql=assignee%20IS%20EMPTY%20AND%20%22Grupo%20Solucionador%5BGroup%20Picker%20(single%20group)%5D%22%20%3D%20%22DC%20-%20Banco%20de%20Dados%20(DBA)%22"}]
}]

send_to_teams(second_message)

logging.info("Processo concluído via Service")