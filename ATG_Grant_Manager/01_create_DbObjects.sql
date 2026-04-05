CREATE BIGFILE TABLESPACE "USERS" DATAFILE SIZE 10m AUTOEXTEND ON NEXT 50m MAXSIZE 10g;
-- CREATE BIGFILE TEMPORARY TABLESPACE "TEMP" TEMPFILE SIZE 10m AUTOEXTEND ON NEXT 50m MAXSIZE 10g;

-- 1. Criar o Usuário Administrador da Ferramenta
CREATE USER "SVC_DBA" IDENTIFIED BY "Svc_DbA_2026_#" DEFAULT TABLESPACE "USERS" TEMPORARY TABLESPACE "TEMP";
	  
GRANT CONNECT, RESOURCE TO SVC_DBA;
GRANT CREATE JOB TO SVC_DBA;
GRANT UNLIMITED TABLESPACE TO SVC_DBA;

-- Permissões perigosas necessárias para a ferramenta funcionar como proxy de grants
GRANT GRANT ANY OBJECT PRIVILEGE TO SVC_DBA WITH ADMIN OPTION;

-- 2. Criar a Tabela de Controle e Sequência
CREATE SEQUENCE SVC_DBA.SEQ_GRANT_CONTROL START WITH 1 INCREMENT BY 1;

CREATE TABLE SVC_DBA.GRANT_CONTROL (
    ID               NUMBER DEFAULT SVC_DBA.SEQ_GRANT_CONTROL.NEXTVAL PRIMARY KEY,
    CHAMADO_JIRA     VARCHAR2(50)  NOT NULL, 
    USUARIO_GRANTED  VARCHAR2(128) NOT NULL,
    PRIVILEGIO       VARCHAR2(30)  NOT NULL,
    OBJETO           VARCHAR2(128) NOT NULL, 
    GRANTOR          VARCHAR2(128) NOT NULL,
    DATA_SOLICITACAO DATE DEFAULT SYSDATE NOT NULL,
    DATA_EXPIRACAO   DATE DEFAULT SYSDATE + 15 NOT NULL,
    STATUS           VARCHAR2(20)  CHECK (STATUS IN ('SUCESSO', 'ERRO', 'REVOGADO')),
    OBSERVACOES      VARCHAR2(4000)
);

COMMENT ON TABLE SVC_DBA.GRANT_CONTROL IS 'Tabela de auditoria para sistema de Grants Automáticos';
COMMENT ON COLUMN SVC_DBA.GRANT_CONTROL.CHAMADO_JIRA IS 'Chave do ticket Jira validador do Grant (Uso Único).';

-- 3. Criação de índice para otimizar a validação do Token de Uso Único
CREATE INDEX SVC_DBA.IDX_GRANT_JIRA ON SVC_DBA.GRANT_CONTROL(CHAMADO_JIRA, STATUS);

-- 4. Criar o Job de Revoke Automático (Roda diariamente à 01:00 AM)
BEGIN
    DBMS_SCHEDULER.create_job (
        job_name        => 'SVC_DBA.JOB_AUTO_REVOKE_GRANTS',
        job_type        => 'PLSQL_BLOCK',
        job_action      => '
            DECLARE
                CURSOR c_expired IS
                    SELECT ID, USUARIO_GRANTED, PRIVILEGIO, OBJETO
                    FROM SVC_DBA.GRANT_CONTROL
                    WHERE STATUS = ''SUCESSO''
                    AND DATA_EXPIRACAO < SYSDATE;
            BEGIN
                FOR r IN c_expired LOOP
                    BEGIN
                        EXECUTE IMMEDIATE ''REVOKE '' || r.PRIVILEGIO || '' ON '' || r.OBJETO || '' FROM '' || r.USUARIO_GRANTED;
                        UPDATE SVC_DBA.GRANT_CONTROL
                        SET STATUS = ''REVOGADO'', OBSERVACOES = OBSERVACOES || '' | Revogado via Job Automático.''
                        WHERE ID = r.ID;
                    EXCEPTION WHEN OTHERS THEN
                        UPDATE SVC_DBA.GRANT_CONTROL
                        SET OBSERVACOES = OBSERVACOES || '' | Falha no Revoke: '' || SQLERRM
                        WHERE ID = r.ID;
                    END;
                END LOOP;
                COMMIT;
            END;',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=DAILY; BYHOUR=1; BYMINUTE=0; BYSECOND=0',
        enabled         => TRUE,
        comments        => 'Job de revogacao de grants expirados (15 dias)'
    );
END;
/