---
name: backend
description: Regras de arquitetura, JQL e tratamento de erros no backend Python do monitor de filas do Jira (ATG).
---

# Backend / Python
- Todo código backend deve possuir `try/catch` explícitos e registrar as saídas no sistema de logging base.
- Padrão de query em `get_dashboard_data()` (`src/jira_service.py`):
```python
try:
    issues = self.run_jql_query(jql)
    results[key] = self._format_issues(issues) if issues else []
except Exception as e:
    logging.error(f"Erro na query '{key}': {e}")
    results[key] = []
```

# JQL (esta skill é dona destas regras)
- `PENDENTE EXTERNO` tem regra anti-duplicidade entre Aguardando (<3d) e Sem Interação (≥3d) — não mexer sem ler o README.
- `dba_urgente` filtra SLA de 1ª resposta (`cf[10321]`) ≤ 1h restante e não pausado.
- Novas queries seguem o mesmo molde: `assignee = '{assignee_email}'` + filtros de projeto/status + `ORDER BY`; validar a JQL no navegador do Jira antes de codar (ex: nome exato de `issuetype`).
