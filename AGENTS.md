# AGENTS.md — ATG Jira2Teams

> Leia `.opencode/skills/*/SKILL.md` antes de qualquer código. São a fonte de verdade
> (arquitetura, UI/UX, versionamento). `FILE_MAP.md` é o mapa de contexto; `README.md` é uso/instalação.

## Versionamento (skill `versioning` — SemVer estrito)
- Qualquer fix de tela/CSS/sintaxe obriga: bump de versão + entrada no `CHANGELOG.md` (Keep a Changelog).
- Versão deve estar visível no footer de `src/templates/index.html`.
- Commits em pt-br. `v1.0.0` reservado à produção final.
- Bugs e melhorias devem ser registrados em `BUGS.md` / `MELHORIAS.md` (regra `Backlog Obrigatório` na skill `versioning`).

## Backend (skill `backend`)
- Todo código Python com `try/catch` explícitos + logging. Sem exceção silenciosa.

## Frontend (skill `ui-ux`)
- Tailwind obrigatório; Bootstrap ou legados, proibidos.
- Dark Mode é padrão — nunca crie componente só claro.
- Sem cores genéricas (`red`/`blue`): usar `var(--accent-*)`; alerta crítico `rgba(255,8,68,0.2)`.
- Mobile-first, sem scroll horizontal; barras de rolagem nativas, evitar.

## Comandos (dev local, sem Docker)
```cmd
pip install -r requirements.txt
copy .env.example .env   & rem edite JIRA_* e TEAMS_WEBHOOK_URL
python src/app.py            & rem web Flask em :5000 (FLASK_DEBUG=true opt-in)
python src/jira_to_teams.py  & rem daemon Teams
python -m py_compile src/app.py src/jira_service.py src/jira_to_teams.py
```
- Sem testes, lint, typecheck ou CI — `py_compile` é a verificação.
- Shell de dev é Windows CMD (`copy`, sem `head`/`tail`); prod é Oracle Linux.

## Arquitetura
- 2 entrypoints, 1 fonte de dados: `src/app.py` (Flask `/` + `/api/data`) e
  `src/jira_to_teams.py` (daemon) consomem `JiraClient.get_dashboard_data()` em
  `src/jira_service.py` (API Jira v3, Server/DC ou Cloud).
- SPA em `src/templates/index.html` faz `fetch /api/data?user=X`; multiusuário via
  input livre de e-mail, fallback `JIRA_USERNAME` do `.env`.
- Bot Teams dispara só no minuto `59`, 07h–17h, seg–sex; log em `logs/jira_to_teams.log`.

## Armadilhas JQL (`get_dashboard_data()` — detalhes na skill `backend`)
- Anti-duplicidade `PENDENTE EXTERNO`, SLA `cf[10321]` do `dba_urgente` — ver skill `backend` antes de mexer.
- `JIRA_DASHBOARD_USERS` no `.env.example` é legado — frontend resolve assignee dinamicamente.

## Deploy / infra (só referência — nunca rodar em dev)
- Prod OCI via `deploy.sh` (one-liner no README); ele faz `git reset --hard`.
- `docker-compose.yml`: `jira-web` (`python3 src/app.py`) + `jira-notifier`
  (`python3 src/jira_to_teams.py`), ambos com `env_file: .env` e volume `./logs`.

## Fora do git / arquivado
- Ignorados: `.env`, `__pycache__/`, `*.log`; `logs/` e `venv/` as createdirs (hoje ausentes da árvore).
- Nunca commitar `.env` real (só `.env.example` é trackeado).
- `docs/_old/` é arquivo morto: só adicionar aviso, nunca seguir como instrução.

## Permissões do agente
- Pode sem pedir: ler arquivos, rodar `py_compile` e comandos de consulta (`git status`, `git log`, `git check-ignore`).
- Só com ordem explícita: commit, push, deploy, apagar arquivos, `git reset`.

## Skills (regra skill-first)
- Antes de executar, verifique se alguma skill cobre a tarefa; se for trabalho repetitivo
  ou com convenções próprias sem skill correspondente, PROPONHA criar/ampliar skill
  (nome, descrição, conteúdo) e aguarde aprovação antes de executar.
- Sinais: fiz algo parecido 2+ vezes; 3+ passos com ordem/gotchas próprios;
  conhecimento que futuros "eus" precisariam e não está em nenhuma skill.
- Prefira ampliar skill existente a criar nova; nunca crie skill para one-off
  ou conhecimento genérico que já está no modelo.
