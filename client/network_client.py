import socket
import threading

class NetworkClient:
    def __init__(self, host, port, on_message_received):
        self.host = host
        self.port = port
        self.sock = None
        self.is_running = False
        
        self.on_message_received = on_message_received

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.is_running = True
            
            threading.Thread(target=self._listen_loop, daemon=True).start()
            print("Połączono z serwerem!")
            return True
        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return False

    def _listen_loop(self):
        while self.is_running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                print(f"Message: {message}")
                
                self.on_message_received(message)
                
            except Exception as e:
                print(f"Błąd w pętli nasłuchiwania: {e}")
                self.is_running = False
                break

    def send(self, message):
        if self.sock and self.is_running:
            try:
                data = (message + "\n").encode('utf-8')
                self.sock.sendall(data)
            except Exception as e:
                print(f"Błąd wysyłania: {e}")
    
    def close_connection(self):
        self.is_running = False
        if self.sock:
            try:
                self.sock.close()
                print("Połączenie zamknięte.")
            except Exception as e:
                print(f"Błąd zamykania połączenia: {e}")