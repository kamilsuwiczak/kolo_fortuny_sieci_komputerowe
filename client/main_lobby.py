import customtkinter as ctk
from views.menu_view import MenuView
from views.set_player_nick_view import NickSetPlayerView
from views.set_host_nick_view import NickSetHostView
from views.game_view import GameView
from views.room_view import RoomView
from network_client import NetworkClient

from dotenv import load_dotenv
import os
load_dotenv()

#zeby odpalic w .env musi byc:
# WINDOW_SIZE,
# SERVER_IP,
# SERVER_PORT

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Klient Gry")
        self.geometry(os.getenv("WINDOW_SIZE"))
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MenuView, NickSetPlayerView, NickSetHostView, GameView, RoomView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuView")
        self.network_client = NetworkClient(os.getenv("SERVER_IP"), int(os.getenv("SERVER_PORT")), self.on_message_received)
        self.network_client.connect()

    def handle_server_message(self, message):
        self.after(0, lambda: self._process_message(message))
    
    def _process_message(self, message):
        if message.startswith("PLAYERS:"):
            raw_data = message.split(":")[1]
            players_list = raw_data.split(",")
            
            if "RoomView" in self.frames:
                self.frames["RoomView"].update_players(players_list)

        elif message == "START_GAME":
            self.show_frame("GameView")

        elif message.startswith("WORD:"):
            word = message.split(":")[1]
            if "GameView" in self.frames:
                self.frames["GameView"].update_word(word)

    def show_frame(self, page_name):
        """Funkcja, która wyciąga dany widok na wierzch"""
        frame = self.frames[page_name]
        frame.tkraise() 

if __name__ == "__main__":
    app = App()
    app.mainloop()