from flask import Flask, render_template, request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Mapeamento das Planilhas e Abas Correto
PLANILHAS = {
    'PAUTAC2': {
        'id': '10T3xDfkqk-sObMk2EffHVgxYd8jFPuOjUXGD4HcoYNM',
        'range': 'REGISTRO_AUDIÊNCIAS!A1:C10'
    },
    'Painel BI': {
        'id': '1CP_2U-HQ8IzfADuoITa2iA9uAC2X1eQ-Mj9ySC4QJ-g',
        'range': 'METAS!A1:C10'
    }
}

def get_google_sheets_data(planilha_id, range_name):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=planilha_id, range=range_name).execute()
    return result.get('values', [])

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_planilha = 'PAUTAC2'  # Valor padrão
    data = []

    if request.method == 'POST':
        selected_planilha = request.form.get('planilha')
        planilha_info = PLANILHAS.get(selected_planilha)
        if planilha_info:
            data = get_google_sheets_data(planilha_info['id'], planilha_info['range'])

    return render_template('index.html', data=data, planilhas=PLANILHAS.keys(), selected=selected_planilha)

if __name__ == '__main__':
    app.run(debug=True)
