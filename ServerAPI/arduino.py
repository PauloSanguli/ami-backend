# arduino.py
import serial
import time

def enviar_serial(comando):
    try:
        comando = str(comando)
        ser = serial.Serial('COM5', 9600, timeout=1)
        time.sleep(2)  # Aguarda estabilizar

        ser.write(comando.encode())  # Envia como bytes
        print(f"[SERIAL] Enviado: {comando}")

        time.sleep(1)
        while ser.in_waiting:
            resposta = ser.readline().decode().strip()
            print(f"[ARDUINO] Respondeu: {resposta}")

        ser.close()
    except Exception as e:
        print(f"[ERRO] Falha na comunicação com Arduino: {e}")

# === Funções específicas para comandos 1 a 4 ===

def comando_1():
    enviar_serial('1')

def comando_2():
    enviar_serial('2')

def comando_3():
    enviar_serial('3')

def comando_4():
    enviar_serial('4')
