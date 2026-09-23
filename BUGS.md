# Bugs

Registro de bugs encontrados no ATG Jira2Teams. Ao achar um bug pelo caminho,
adicione em **Abertos** seguindo o template. Ao corrigir, mova para **Resolvidos**
com a versão do `CHANGELOG.md` que entregou a correção.

## Abertos

_Nenhum bug registrado no momento._

## Resolvidos

### `name` das skills fora da spec do opencode
- **Data:** 2026-09-23
- **Onde:** `.opencode/skills/*/SKILL.md` (frontmatter)
- **Como reproduzir:** comparar o `name` com a regex oficial `^[a-z0-9]+(-[a-z0-9]+)*$` e com o nome do diretório
- **Esperado:** `name` minúsculo e igual ao diretório (`backend`, `ui-ux`, `versioning`)
- **Atual:** estava `ATG Backend`, `ATG UI/UX`, `ATG Versioning` (maiúsculas, espaços, `/`)
- **Severidade:** média (funcionava, mas fora da spec — risco de quebra em updates do opencode)
- **Correção:** renomeados para `backend`, `ui-ux`, `versioning`; sem bump (só docs/regras)

### Template
```md
### <título curto>
- **Data:** AAAA-MM-DD
- **Onde:** web (card/aba) / Teams (qual seção) / backend
- **Como reproduzir:** passo a passo
- **Esperado:** o que deveria acontecer
- **Atual:** o que acontece
- **Severidade:** baixa / média / alta / crítica
```
