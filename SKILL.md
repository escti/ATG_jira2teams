---
name: ATG Jira2Teams Base Architecture
description: Regras intransigentes de UI/UX, arquitetura de código e release management para o monitor de filas do Jira e notificador de Teams.
---

# 1. Regras Imutáveis de UI/UX
- **Design System Obrigatório**: Abordagem "Glassmorphism" com suporte nativo a transições fluidas e micro-animações.
- **Dark Mode**: Modo Escuro é obrigatório e padrão para novas implementações. Não crie componentes apenas na versão clara.
- **Acessibilidade e Layout**: 
  - Restringir barras de rolagem em excesso (ocultar nativas ou utilizar track customizada extra fina e transparente).
  - Responsividade Mobile-first (os cards devem empilhar graciosamente e não causar scroll horizontal em tabelas ou eixos X locais).
- **Paleta de Cores**: 
  - Proibido usar red/blue genéricos de browser (ex: `red`); obrigatório o uso de gradients definidos no `:root` (Ex: `var(--accent-blue)` e `var(--accent-purple)`).
  - Alertas Críticos mantêm tons inspirados em `rgba(255,8,68,0.2)`.

# 2. Regras de Código 
- **Frontend / Frameworks**: O padrão moderno, seguro e obrigatório é o **Tailwind CSS**. Utility-first classes devem ser usadas para todo o layout, garantindo consistência, performance e facilidade de manutenção. O uso de Bootstrap ou outros frameworks legados está proibido para novas implementações e refatorações.
- **Backend / Python**: Todo código backend deve possuir `try/catch` explícitos e registrar as saídas no sistema de logging base. 

# 3. Regras de Controle de Versão e Deployment
- **Changelog Strict**: Em prol da rastreabilidade (`CHANGELOG.md`), qualquer novo CSS, fix de syntax ou tela obriga um version bump seguindo SemVer. A versão inicial do produto de testes é a `v0.1.0`. Apenas a versão de produção final atingirá `v1.0.0`.
- **Global Footer Version**: A variável de versão **DEVE** estar ancorada no UI atual e visível publicamente no rodapé da aplicação web.
