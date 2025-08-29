# main.py
import json
import time
from datetime import datetime
import pyttsx3
import pytz
import arduino 

fuso_angola = pytz.timezone('Africa/Luanda')
engine = pyttsx3.init()
ARQUIVO_JSON = 'horarios.json'

def carregar_horarios():
    try:
        with open(ARQUIVO_JSON, 'r') as f:
            dados = json.load(f)
            return dados.get("horarios", [])
    except Exception as e:
        print(f"[ERRO] Não foi possível ler o JSON: {e}")
        return []

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def falar_duas_vezes(texto):
    falar(texto)
    time.sleep(0.5)
    falar(texto)

def verificar_horas():
    ja_enviados = set()
    contador = 1
    dia_atual = datetime.now(fuso_angola).date()

    while True:
        agora = datetime.now(fuso_angola)
        hora_str = agora.strftime('%H:%M')
        print(f"\n⏰ Hora atual: {hora_str}")

        # Reset diário
        if agora.date() != dia_atual:
            print("[INFO] Novo dia. Limpando comandos enviados.")
            ja_enviados.clear()
            dia_atual = agora.date()
            contador = 1

        horarios = carregar_horarios()
        print(f"[INFO] Horários carregados: {horarios}")
        
        for horario in horarios:
            if hora_str == horario and horario not in ja_enviados:
                print(f"✅ Hora {horario} bateu. Esperado: {contador}")

                # Envia o próximo da sequência
                falar_duas_vezes(f"Está na hora. Agora são {hora_str}")
                arduino.enviar_serial(contador)

                ja_enviados.add(horario)

                # Avança a sequência
                contador += 1
                if contador > 4:
                    contador = 1

        time.sleep(1)
verificar_horas()