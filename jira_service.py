import os
import requests
import logging
from datetime import datetime
import pytz

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JiraClient:
    def __init__(self):
        # Normaliza a URL: remove aspas (caso existam no .env) e barras finais
        self.server = os.getenv('JIRA_SERVER', '').strip('"').strip("'").rstrip('/')
        self.username = os.getenv('JIRA_USERNAME', '').strip('"').strip("'")
        self.password = os.getenv('JIRA_PASSWORD', '').strip('"').strip("'")
        self.auth = (self.username, self.password)
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # Jira Cloud v3 endpoints
        self.api_url_primary = f"{self.server}/rest/api/3/search/jql"
        self.api_url_fallback = f"{self.server}/rest/api/3/search"
        self.current_user = self.username

    def run_jql_query(self, jql, max_results=100, user=None):
        # Se for um usuário específico, substitui currentUser() por 'user_name'
        if user:
            # Em Jira Cloud, recomeda-se usar o e-mail ou accountId, mas o JQL aceita string
            jql = jql.replace("currentUser()", f"'{user}'")


        
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "fields": ["key", "summary", "updated", "status"]
        }
        
        # Tenta endpoint primária
        response = requests.post(self.api_url_primary, auth=self.auth, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            # Tenta fallback pra versão de API mais crua
            fallback = requests.post(self.api_url_fallback, auth=self.auth, headers=self.headers, json=payload)
            if fallback.status_code != 200:
                # Levanta o erro real do Jira extraindo a string da Atlassian
                try:
                    err_msgs = response.json().get("errorMessages", [])
                    err_txt = " | ".join(err_msgs) if err_msgs else response.text
                except:
                    err_txt = response.text
                raise Exception(f"Erro JQL do Jira ({response.status_code}): {err_txt}")
            response = fallback
        
        response.raise_for_status()
        return response.json().get("issues", [])

    def get_dashboard_data(self, user=None):
        queries = {
            "pessoais_aguardando": 'assignee = currentUser() AND statusCategory != Done AND updated <= endOfYear() AND "Tempo de resolução" != paused()',
            "pessoais_sla_critico": 'assignee = currentUser() AND statusCategory != Done AND updated <= endOfYear() AND "Tempo de resolução" != paused() AND "Tempo de resolução" <= remaining("1h")',
            "pessoais_sem_interacao": 'assignee = currentUser() AND statusCategory != Done and updatedDate <= "-3d" ORDER BY updatedDate asc',
            "dba_urgente": 'assignee IS EMPTY AND "Grupo Solucionador[Group Picker (single group)]" = "DC - Banco de Dados (DBA)" AND statusCategory != Done AND ("Tempo de Primeira Resposta" = breached() OR "Tempo de Primeira Resposta" <= remaining("1h"))'
        }
        
        results = {}
        for key, jql in queries.items():
            issues = self.run_jql_query(jql, user=user)
            results[key] = self._format_issues(issues) if issues is not None else []
            
        return results

    def _format_issues(self, issues):
        formatted = []
        for issue in issues:
            formatted.append({
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "updated": issue["fields"]["updated"][:10],
                "url": f"{self.server}/browse/{issue['key']}"
            })
        return formatted
