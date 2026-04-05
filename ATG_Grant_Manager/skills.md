name: "Grant Manager V2 - Core Architecture & UI"
description: "Sistema de gerenciamento e auditoria de grants temporários no Oracle com validação Jira e revogação automática."

1. Regras Imutáveis de UI/UX

Design System: Modo Escuro (Dark Mode) estritamente obrigatório em todas as interfaces visuais.

Estilização: Uso exclusivo de Tailwind CSS para responsividade. Proibida a utilização de cores fora da paleta primária pré-definida.

Navegação: Design fluido e responsivo. É expressamente proibida a presença de barras de rolagem nativas (uso obrigatório de scrollbar-hide ou similar).

Consistência: A versão atual do CHANGELOG.md deve ser renderizada dinamicamente no rodapé global do sistema.

2. Regras de Código e Arquitetura

Ambiente OS: Scripts shell padronizados para execução em Oracle Linux 8.

Segurança de Acesso: Credenciais de banco de dados e APIs (Jira) jamais devem ser expostas em texto claro no código. Uso obrigatório de variáveis de ambiente (.env).

Validação de Entrada: O script deve validar a presença do formato SCHEMA.TABELA no campo OBJETO. Privilégios restritos a SELECT, INSERT, DELETE e UPDATE.

Auditoria de Resiliência: Qualquer status, seja sucesso ou erro de banco de dados, deve ser obrigatoriamente inserido na tabela SVC_DBA.GRANT_CONTROL. Em caso de falha, o status deve ser gravado como ERRO com detalhes.

3. Camada de Integração e Governança (Jira)

Validação Externa: O sistema deve realizar uma chamada via API (cURL/JSON) ao Jira antes de qualquer execução de DDL no Oracle.

Estado de Aprovação: O grant só será liberado se o status do chamado for 'Aprovado', 'Done' ou 'Concluído'.

Token de Uso Único: Cada chave de chamado (ex: INFRA-123) deve ser verificada contra a tabela SVC_DBA.GRANT_CONTROL. Se existir registro prévio com status 'SUCESSO', a operação é abortada.