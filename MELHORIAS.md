# Melhorias

Backlog de ideias e melhorias do ATG Jira2Teams. Novas ideias entram como `proposta`.
Ao concluir, marque a versão do `CHANGELOG.md` que a entregou.

| ID    | Ideia                                                        | Status   | Prioridade | Entregue em |
|-------|--------------------------------------------------------------|----------|------------|-------------|
| M-001 | Novo card só com TIC do tipo Epic (separar do Projetos TIC)  | entregue | alta       | 0.9.0       |

## Detalhes

### M-001 — Card "Epics TIC" na aba Projetos
- **Motivo:** nem todo ticket TIC é projeto; os do tipo **Epic** é que são projetos de fato.
- **Escopo decidido:** Epics saem do card "Projetos Ativos TIC" (`issuetype != Epic`) e ganham card próprio
  (`project IN (TIC) AND issuetype = Epic`, mesmo assignee do "Jira User"). Só Web — Teams inalterado.
- **JQL proposta (validar nome exato do tipo no Jira antes):**
  `assignee = 'X' AND project IN (TIC) AND issuetype = Epic AND resolution = Unresolved AND status NOT IN (Concluído, Backlog, Cancelado) ORDER BY updated ASC`
- **Toques:** `src/jira_service.py` (nova query `pessoais_epics_tic` + filtro no TIC atual),
  `src/templates/index.html` (novo card + `updateTable`/contadores/gráfico), bump + changelog + footer pela skill `versioning`.
