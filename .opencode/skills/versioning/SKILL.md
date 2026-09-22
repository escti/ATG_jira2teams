---
name: ATG Versioning
description: Regras de controle de versão, changelog, footer e commits para o projeto Jira2Teams.
---

# 1. Changelog Strict
- Em prol da rastreabilidade (`CHANGELOG.md`), qualquer novo CSS, fix de syntax ou tela obriga um version bump seguindo SemVer. A versão inicial do produto de testes é a `v0.1.0`. Apenas a versão de produção final atingirá `v1.0.0`.

# 2. Global Footer Version
- A variável de versão **DEVE** estar ancorada no UI atual e visível publicamente no rodapé da aplicação web.

# 3. Commits em Português
- Mensagens de commit devem ser escritas em português brasileiro (pt-br), mantendo consistência com a documentação e o público-alvo do projeto.

# 4. Backlog Obrigatório
- Todo bug encontrado no caminho deve ser registrado em `BUGS.md` (seção Abertos, seguindo o template) antes ou junto da correção; ao corrigir, mover para Resolvidos com a versão do `CHANGELOG.md` que entregou o fix.
- Toda ideia/melhoria deve entrar em `MELHORIAS.md` como `proposta` com o próximo ID livre (`M-002`, …); ao concluir, preencher `Entregue em` com a versão do changelog.
- Exceção: correção trivial óbvia (ex: typo) feita no mesmo commit pode ir só ao changelog, sem registro em `BUGS.md`.
