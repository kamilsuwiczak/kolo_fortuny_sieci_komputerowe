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

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Klient Gry")
        self.geometry(os.getenv("WINDOW_SIZE"))
        
        self.is_host = False
        self.player_nick = None
        self.pending_room_code = None
        self.current_page = "MenuView"

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
        
        ip = os.getenv("SERVER_IP", "127.0.0.1")
        port = int(os.getenv("SERVER_PORT"))
        self.network_client = NetworkClient(ip, port, self.handle_server_message)
        self.network_client.connect()

    def handle_server_message(self, message):
        self.after(0, lambda: self._process_message(message))
    
    def _process_message(self, message):
        message = message.strip()

        if message.startswith("PLAYERS:"):
            if self.current_page in ["NickSetPlayerView", "NickSetHostView"]:
                if self.current_page == "NickSetPlayerView" and self.pending_room_code:
                    if "RoomView" in self.frames:
                        self.frames["RoomView"].set_room_code(self.pending_room_code)
                self.show_frame("RoomView")

            raw_data = message.split(":")[1]
            players_list = [player.strip() for player in raw_data.split(",")]
            if "RoomView" in self.frames:
                self.frames["RoomView"].update_players(players_list)

        elif message.startswith("ROOM_CODE:"):
            code = message.split(":")[1]
            if "RoomView" in self.frames:
                self.frames["RoomView"].set_room_code(code)

        elif message == "ERROR_NICK_TAKEN":
            if self.current_page in self.frames:
                frame = self.frames[self.current_page]
                if hasattr(frame, "show_error"):
                    frame.show_error("Nick jest zajęty! Wybierz inny.")

        elif message == "ERROR_WRONG_ROOM_CODE":
            if "NickSetPlayerView" in self.frames:
                self.frames["NickSetPlayerView"].show_error("Pokój o takim kodzie nie istnieje!")

        elif message.startswith("HOST_CHANGE:"):
            new_host_nick = message.split(":")[1].strip()
            if self.player_nick == new_host_nick:
                self.is_host = True
            else:
                self.is_host = False
            if "RoomView" in self.frames:
                self.frames["RoomView"].refresh_view()

        elif message == "START_GAME":
            self.show_frame("GameView")
        
        elif message.startswith("NEW_ROUND"):
            if "GameView" in self.frames:
                self.frames["GameView"].start_new_round()

        elif message.startswith("WORD:"):
            word = message.split(":")[1]
            if "GameView" in self.frames:
                self.frames["GameView"].update_word(word)

    def show_frame(self, page_name):
        self.current_page = page_name
        frame = self.frames[page_name]
        frame.tkraise() 

if __name__ == "__main__":
    app = App()
    app.mainloop()