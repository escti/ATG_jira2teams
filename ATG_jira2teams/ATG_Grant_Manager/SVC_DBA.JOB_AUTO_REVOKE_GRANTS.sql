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
                        SET STATUS = ''REVOGADO'', OBSERVACOES = OBSERVACOES || '' | Revogado automaticamente pelo JOB.''
                        WHERE ID = r.ID;
                    EXCEPTION WHEN OTHERS THEN
                        UPDATE SVC_DBA.GRANT_CONTROL
                        SET OBSERVACOES = OBSERVACOES || '' | Falha ao revogar: '' || SQLERRM
                        WHERE ID = r.ID;
                    END;
                END LOOP;
                COMMIT;
            END;',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=DAILY; BYHOUR=01; BYMINUTE=00', -- Executa todo dia à 1h da manhã
        enabled         => TRUE
    );
END;
/