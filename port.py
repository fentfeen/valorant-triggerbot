import time, ctypes, uuid, os, keyboard, socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 65432))
    sock.listen(1)
    print("Server listening on port 65432")
  
    time.sleep(0.1)
    
    conn, addr = sock.accept()
    print(f"Connected by {addr}")
    print("hiding in 3 secs...")
    time.sleep(3)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.kernel32.SetConsoleTitleW(str(uuid.uuid4()))
    os.system('cls')
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            key = data.decode()
            if len(key) == 1 and key.isalnum():  
                keyboard.send(key)
            time.sleep(0.01)

if __name__ == "__main__":
    print("Server starting...")
    main()
