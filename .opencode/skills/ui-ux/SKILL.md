---
name: ui-ux
description: Regras de design system, estilo visual e acessibilidade para o monitor de filas do Jira (ATG).
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

# 2. Frontend / Frameworks
- O padrão moderno, seguro e obrigatório é o **Tailwind CSS**. Utility-first classes devem ser usadas para todo o layout, garantindo consistência, performance e facilidade de manutenção. O uso de Bootstrap ou outros frameworks legados está proibido para novas implementações e refatorações.

# 3. Padrões positivos (prefira estes)
- Card padrão: container `glass-card` + header `card-header-styled` com gradiente + `tbody` próprio + contador no título (modelo em `src/templates/index.html`, bloco "Projetos Ativos TIC").
- Estados de loading usam `animate-pulse`; tabelas nunca causam scroll horizontal (mobile-first).
