from flask import Flask, render_template, jsonify
from jira_service import JiraClient
import os
from dotenv import load_dotenv

load_dotenv() # Carrega do .env se existir

app = Flask(__name__)
jira_client = JiraClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    try:
        data = jira_client.get_dashboard_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # No Oracle Linux, você pode precisar abrir a porta no firewall
    app.run(host='0.0.0.0', port=5000, debug=True)
