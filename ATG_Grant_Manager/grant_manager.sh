#!/bin/bash
# ==============================================================================
# Artefato: grant_manager.sh
# Objetivo: Validar chamados no Jira e conceder Grants com auditoria no Oracle
# Requisitos: jq, sqlplus
# Execução: ./grant_manager.sh <JIRA_ID> <USER_GRANTED> <PRIV> <SCHEMA.OBJ> <GRANTOR>
# ==============================================================================

# 1. Carregamento de Variáveis de Ambiente (Segurança)
if [[ -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_TNS" || -z "$JIRA_SERVER" ]]; then
    echo "ERRO DE SEGURANÇA: Credenciais de banco de dados ou Jira ausentes no ambiente."
    exit 1
fi

# 2. Captura e Validação de Argumentos
TICKET_ID=$(echo "$1" | tr '[:lower:]' '[:upper:]')
USUARIO_GRANTED=$(echo "$2" | tr '[:lower:]' '[:upper:]')
PRIVILEGIO=$(echo "$3" | tr '[:lower:]' '[:upper:]')
OBJETO=$(echo "$4" | tr '[:lower:]' '[:upper:]')
GRANTOR=$(echo "$5" | tr '[:lower:]' '[:upper:]')

if [[ -z "$TICKET_ID" || -z "$USUARIO_GRANTED" || -z "$PRIVILEGIO" || -z "$OBJETO" || -z "$GRANTOR" ]]; then
    echo "USO CORRETO: $0 <TICKET_JIRA> <USUARIO_DESTINO> <PRIVILEGIO> <SCHEMA.TABELA> <SOLICITANTE>"
    exit 1
fi

if [[ ! "$PRIVILEGIO" =~ ^(SELECT|INSERT|UPDATE|DELETE)$ ]]; then
    echo "FALHA DE VALIDAÇÃO: Privilégio '$PRIVILEGIO' não autorizado."
    exit 1
fi

if [[ ! "$OBJETO" =~ ^[A-Z0-9_]+\.[A-Z0-9_]+$ ]]; then
    echo "FALHA DE VALIDAÇÃO: O objeto '$OBJETO' deve seguir estritamente o formato SCHEMA.TABELA."
    exit 1
fi

# 3. Integração Jira (Validação Externa)
echo "[SISTEMA] Consultando status do chamado $TICKET_ID no Jira Server..."
JIRA_RESPONSE=$(curl -s -u "${JIRA_USERNAME}:${JIRA_PASSWORD}" \
    -X GET \
    -H "Accept: application/json" \
    "${JIRA_SERVER}/rest/api/2/issue/${TICKET_ID}?fields=status")

STATUS_JIRA=$(echo "$JIRA_RESPONSE" | jq -r '.fields.status.name')

if [ "$STATUS_JIRA" == "null" ] || [ -z "$STATUS_JIRA" ]; then
    echo "ERRO DE INTEGRAÇÃO: Chamado ${TICKET_ID} não encontrado ou credenciais rejeitadas."
    exit 1
fi

if [[ "$STATUS_JIRA" != "Aprovado" && "$STATUS_JIRA" != "Concluído" && "$STATUS_JIRA" != "Done" ]]; then
    echo "ACESSO NEGADO: O chamado ${TICKET_ID} encontra-se em '${STATUS_JIRA}'. Requer aprovação gerencial."
    exit 1
fi
echo "[SISTEMA] Governança validada. Ticket Aprovado."

# 4. Execução Transacional no Oracle
echo "[SISTEMA] Iniciando injeção PL/SQL no banco de dados ($DB_TNS)..."

sqlplus -s /nolog <<EOF
CONNECT ${DB_USER}/${DB_PASSWORD}@${DB_TNS}
SET HEADING OFF FEEDBACK OFF SERVEROUTPUT ON

DECLARE
    v_count NUMBER;
    v_err_msg VARCHAR2(4000);
BEGIN
    SELECT COUNT(*) INTO v_count FROM SVC_DBA.GRANT_CONTROL 
    WHERE CHAMADO_JIRA = '${TICKET_ID}' AND STATUS = 'SUCESSO';
    
    IF v_count > 0 THEN
        DBMS_OUTPUT.PUT_LINE('FALHA DE GOVERNANCA: O chamado ${TICKET_ID} ja foi utilizado. Token de uso unico violado.');
        RETURN;
    END IF;

    BEGIN
        EXECUTE IMMEDIATE 'GRANT ${PRIVILEGIO} ON ${OBJETO} TO ${USUARIO_GRANTED}';
        
        INSERT INTO SVC_DBA.GRANT_CONTROL (CHAMADO_JIRA, USUARIO_GRANTED, PRIVILEGIO, OBJETO, GRANTOR, STATUS, OBSERVACOES)
        VALUES ('${TICKET_ID}', '${USUARIO_GRANTED}', '${PRIVILEGIO}', '${OBJETO}', '${GRANTOR}', 'SUCESSO', 'Grant executado com sucesso e auditado.');
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('SUCESSO: Privilegios concedidos e registrados na auditoria.');
        
    EXCEPTION
        WHEN OTHERS THEN
            v_err_msg := SQLERRM;
            INSERT INTO SVC_DBA.GRANT_CONTROL (CHAMADO_JIRA, USUARIO_GRANTED, PRIVILEGIO, OBJETO, GRANTOR, STATUS, OBSERVACOES)
            VALUES ('${TICKET_ID}', '${USUARIO_GRANTED}', '${PRIVILEGIO}', '${OBJETO}', '${GRANTOR}', 'ERRO', 'Falha no comando GRANT: ' || v_err_msg);
            COMMIT;
            DBMS_OUTPUT.PUT_LINE('ERRO_ORACLE: ' || v_err_msg);
    END;
END;
/
EXIT;
EOF

echo "[SISTEMA] Operação finalizada."