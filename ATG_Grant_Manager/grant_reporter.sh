#!/bin/bash
# ==============================================================================
# Artefato: grant_reporter.sh
# Objetivo: Extrair dados de auditoria do Oracle e formatar as linhas em HTML
# ==============================================================================

if [[ -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_TNS" ]]; then
    echo "<tr><td colspan='10' class='px-4 py-4 text-center text-red-500 font-bold'>ERRO DE SISTEMA: Variáveis de ambiente do Banco de Dados não localizadas. Contate a infraestrutura.</td></tr>"
    exit 1
fi

sqlplus -s /nolog <<EOF
CONNECT ${DB_USER}/${DB_PASSWORD}@${DB_TNS}
SET HEADING OFF FEEDBACK OFF PAGESIZE 0 LINESIZE 32767 TRIMSPOOL ON TRIMOUT ON

SELECT 
    '<tr class="hover:bg-gray-800 transition-colors">' ||
    '<td class="px-4 py-3 border-b border-gray-700 font-medium text-gray-300">' || ID || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700 font-mono text-blue-400">' || NVL(CHAMADO_JIRA, 'N/A') || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700">' || USUARIO_GRANTED || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700 font-semibold">' || PRIVILEGIO || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700">' || OBJETO || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700 text-gray-400">' || GRANTOR || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700">' || TO_CHAR(DATA_SOLICITACAO, 'DD/MM/YYYY HH24:MI') || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700 text-yellow-500">' || TO_CHAR(DATA_EXPIRACAO, 'DD/MM/YYYY HH24:MI') || '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700">' || 
        CASE STATUS 
            WHEN 'SUCESSO' THEN '<span class="px-2 py-1 text-xs font-bold rounded-full bg-green-900 text-green-300 border border-green-700">SUCESSO</span>'
            WHEN 'ERRO' THEN '<span class="px-2 py-1 text-xs font-bold rounded-full bg-red-900 text-red-300 border border-red-700">ERRO</span>'
            WHEN 'REVOGADO' THEN '<span class="px-2 py-1 text-xs font-bold rounded-full bg-gray-700 text-gray-400 border border-gray-600">REVOGADO</span>'
            ELSE '<span class="px-2 py-1 text-xs font-bold rounded-full bg-yellow-900 text-yellow-300">' || STATUS || '</span>'
        END || 
    '</td>' ||
    '<td class="px-4 py-3 border-b border-gray-700 text-xs text-gray-400 truncate max-w-xs" title="' || REPLACE(OBSERVACOES, '"', '&quot;') || '">' || NVL(OBSERVACOES, '-') || '</td>' ||
    '</tr>'
FROM SVC_DBA.GRANT_CONTROL
ORDER BY ID DESC;
EXIT;
EOF