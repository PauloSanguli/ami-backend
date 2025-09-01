import json
import time
from datetime import datetime
import pyttsx3
import pytz
import arduino
# Fuso horário de Angola
fuso_angola = pytz.timezone('Africa/Luanda')

# Engine de voz
engine = pyttsx3.init()

# Caminho do arquivo JSON
ARQUIVO_JSON = 'horarios.json'

# Lê os horários do arquivo JSON
def carregar_horarios():
    try:
        with open(ARQUIVO_JSON, 'r') as f:
            dados = json.load(f)
            return dados.get("horarios", [])
    except Exception as e:
        print(f"[ERRO] Não foi possível ler o JSON: {e}")
        return []

# Fala a mensagem
def falar(texto):
    engine.say(texto)
    engine.runAndWait()

# Loop contínuo para verificar hora
def verificar_horas():
    while True:
        agora = datetime.now(fuso_angola).strftime('%H:%M')
        print(f"\n⏰ Hora atual: {agora}")

        # 🔁 Recarrega o JSON toda vez
        horarios = carregar_horarios()
        print(f"[INFO] Horários carregados: {horarios}")

        for horario in horarios:
            print(f"🔍 Comparando: {agora} <=> {horario}")
            if agora == horario:
                print(f"✅ Hora bateu! {agora} == {horario}")
                falar(f"Está na hora. Agora são {agora}")
                arduino.Arduino()

        time.sleep(1)  # Aguarda 60 segundos

if __name__ == "__main__":
    verificar_horas()
