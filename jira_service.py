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

    def run_jql_query(self, jql, max_results=100):
        logging.info(f"Executando JQL no Jira: {jql}")
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
        issues = response.json().get("issues", [])
        logging.info(f"Jira retornou {len(issues)} resultados.")
        return issues

    def get_dashboard_data(self, user=None):
        # Resolução inteligente de usuário
        if user:
            user_clean = user.strip().lower()
            # Se for o prefixo do username configurado (ex: thiago -> thiago.albuquerque@...)
            if user_clean in self.username.lower():
                assignee_email = self.username
            # Se for um nome curto sem @, tenta anexar o domínio do JIRA_USERNAME
            elif "@" not in user_clean and "@" in self.username:
                domain = self.username.split("@")[1]
                assignee_email = f"{user_clean}@{domain}"
            else:
                assignee_email = user.strip()
        else:
            assignee_email = self.username
        
        queries = {
            "pessoais_aguardando": f"assignee = '{assignee_email}' AND project NOT IN (TIC, GPM) AND resolution = Unresolved AND status not in (Concluído,Backlog,Cancelado) ORDER BY status desc, updated ASC, 'Tempo de resolução' DESC",
            "pessoais_sla_critico": f"assignee = '{assignee_email}' AND project NOT IN (TIC, GPM) AND statusCategory != Done AND updated <= endOfYear() AND 'Tempo de resolução' != paused() AND 'Tempo de resolução' <= remaining('1h')",
            "pessoais_sem_interacao": f"assignee = '{assignee_email}' AND project NOT IN (TIC, GPM) AND statusCategory != Done and updatedDate <= '-3d' ORDER BY updatedDate ASC",
            "pessoais_projetos": f"assignee = '{assignee_email}' AND project IN (TIC, GPM) AND resolution = Unresolved AND status NOT IN (Concluído, Backlog, Cancelado) ORDER BY status DESC, updated ASC",
            "pessoais_finalizados_mes": f"assignee = '{assignee_email}' AND project NOT IN (TIC, GPM) AND resolution = done AND status not in (Concluído, Backlog, Cancelado) AND resolved >= startOfMonth() ORDER BY created DESC, status DESC, updated ASC, 'Tempo de resolução' DESC",
            "dba_urgente": 'assignee = empty AND project NOT IN (TIC, GPM) AND status NOT IN (Done, "Concluído(a)", Encerrado, Cancelado, Canceled, Reprovado, "Aguardando Aprovação") AND "grupo solucionador[group picker (single group)]" = "DC - Banco de Dados (DBA)" ORDER BY cf[10321] ASC, created DESC'
        }
        
        results = {}
        for key, jql in queries.items():
            try:
                issues = self.run_jql_query(jql)
                results[key] = self._format_issues(issues) if issues else []
            except Exception as e:
                logging.error(f"Erro na query '{key}': {e}")
                results[key] = []
            
        return results

    def _format_issues(self, issues):
        formatted = []
        for issue in issues:
            status_name = "Desconhecido"
            status_category = "new"
            
            if "status" in issue["fields"] and issue["fields"]["status"]:
                status_name = issue["fields"]["status"]["name"]
                if "statusCategory" in issue["fields"]["status"]:
                    status_category = issue["fields"]["status"]["statusCategory"].get("key", "new")
                
            formatted.append({
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "status": status_name,
                "status_category": status_category,
                "updated": issue["fields"]["updated"][:10],
                "url": f"{self.server}/browse/{issue['key']}"
            })
        return formatted
