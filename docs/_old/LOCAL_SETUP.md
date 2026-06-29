# Guia de Configuração Local (Windows)

Siga estes passos para configurar e rodar o dashboard na sua máquina antes de fazer o deploy.

## 1. Instalação do Python

Como o Python não foi detectado no seu terminal, siga estes passos:
1.  Acesse [python.org/downloads](https://www.python.org/downloads/windows/).
2.  Baixe a versão estável mais recente (ex: 3.12).
3.  **IMPORTANTE**: Durante a instalação, marque a caixa **"Add Python to PATH"**. Se não fizer isso, os comandos não funcionarão no terminal.

## 2. Preparar o Ambiente

Abra o seu terminal (CMD ou Git Bash são recomendados se o PowerShell estiver bloqueado) na pasta do projeto e execute:

```cmd
# Criar ambiente virtual (isolamento de dependências)
python -m venv venv

# Ativar o ambiente (No Windows CMD)
venv\Scripts\activate
```

## 3. Instalar Dependências

Com o ambiente ativado (você verá `(venv)` no início da linha do terminal), instale as bibliotecas necessárias:

```cmd
pip install -r requirements.txt
```

## 4. Configurar Variáveis de Ambiente

O arquivo `.env` já está configurado na sua pasta. Note que eu fiz uma correção no código para aceitar as aspas que você usou, mas para futuros projetos, o ideal é não usar aspas nos valores.

Exemplo correto:
```env
JIRA_SERVER=https://suaempresa.atlassian.net
```

## 5. Rodar o Dashboard

Para iniciar o servidor localmente:

```cmd
# Garanta que está na pasta raiz do projeto
python app.py
```

O dashboard estará disponível em: [http://localhost:5000](http://localhost:5000)

---

### Dicas de Troubleshooting:
- **Erro de JQL**: Se os cards mostrarem "Falha ao carregar API", verifique se o seu **API Token** no `.env` está correto.
- **Porta Ocupada**: Se der erro de porta 5000, você pode mudar no final do arquivo `app.py`.
