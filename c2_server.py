from flask import Flask, render_template, request
import socket
import threading

app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 9999
BUFFER = 2024

server_thread = None
conn = None

def start_server():
    global conn
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    conn, addr = server_sock.accept()
    print("Server connected.")

def receive_output():
    global conn
    while True:
        try:
            output = conn.recv(BUFFER).decode()
            if not output:
                break
            return(output)
        except Exception as e:
            print("Error:", e)
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_server', methods=['POST'])
def start_server_route():
    global server_thread
    if not server_thread or not server_thread.is_alive():
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
        return render_template('index.html', server_started=True)
    else:
        return render_template('index.html', server_started=True, output="Server is already running.")

@app.route('/send_command', methods=['POST'])
def send_command():
    global conn
    if not conn:
        return render_template('index.html', server_started=False, output="Error: Server is not running or connection failed.")
    try:
        command = request.form['command']
        conn.send(command.encode())
        output = receive_output()
        return render_template('index.html', server_started=True, output=output)
    except Exception as e:
        print("Error:", e)
        return render_template('index.html', server_started=False, output="Error: Failed to send command.")

if __name__ == '__main__':
    app.run(debug=True)
