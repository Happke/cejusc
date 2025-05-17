from flask import Flask, render_template_string, request
import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Carregar os conteúdos JSON diretamente das variáveis de ambiente
GOOGLE_TOKEN_JSON = os.getenv("GOOGLE_TOKEN_JSON")
GOOGLE_TOKEN = json.loads(GOOGLE_TOKEN_JSON)

def get_google_sheets_data(spreadsheet_id, range_name):
    creds = Credentials.from_authorized_user_info(GOOGLE_TOKEN)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])

@app.route('/')
def index():
    return render_template_string('''
        <h1>Consulta Planilhas CEJUSC</h1>
        <form action="/ver_dados" method="post">
            <label>ID da Planilha:</label><br>
            <input type="text" name="spreadsheet_id" value="10T3xDfkqk-sObMk2EffHVgxYd8jFPuOjUXGD4HcoYNM"><br>
            <label>Nome da Aba e Intervalo (ex: METAS!A1:C10):</label><br>
            <input type="text" name="range_name" value="METAS!A1:C10"><br>
            <button type="submit">Ver Dados</button>
        </form>
    ''')

@app.route('/ver_dados', methods=['POST'])
def ver_dados():
    spreadsheet_id = request.form['spreadsheet_id']
    range_name = request.form['range_name']
    try:
        data = get_google_sheets_data(spreadsheet_id, range_name)
        return render_template_string('''
            <h1>Dados da Planilha</h1>
            <table border="1">
                {% for row in data %}
                    <tr>
                        {% for cell in row %}
                            <td>{{ cell }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </table>
            <a href="/">Voltar</a>
        ''', data=data)
    except Exception as e:
        return f"<h1>Erro ao buscar dados</h1><p>{str(e)}</p><a href='/'>Voltar</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
