from flask import Flask, render_template, jsonify, request
from jira_service import JiraClient
import os
from dotenv import load_dotenv

load_dotenv() # Carrega do .env se existir

app = Flask(__name__)
jira_client = JiraClient()

@app.route('/')
def index():
    raw_users = os.getenv('JIRA_DASHBOARD_USERS', '')
    if raw_users:
        users = [u.strip() for u in raw_users.split(',') if u.strip()]
    else:
        # Pega o email do JIRA default para não deixar em branco, limpando apenas o prefixo
        users = [os.getenv('JIRA_USERNAME', '').split('@')[0]]

    return render_template('index.html', users=users)

@app.route('/api/data')
def get_data():
    # Verifica se há parâmetro de usuário na query string
    user = request.args.get('user')
    try:
        data = jira_client.get_dashboard_data(user=user)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # No Oracle Linux, você pode precisar abrir a porta no firewall
    app.run(host='0.0.0.0', port=5000, debug=True)
