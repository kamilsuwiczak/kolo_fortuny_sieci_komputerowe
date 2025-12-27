import customtkinter as ctk
from views.menu_view import MenuView
from views.set_player_nick_view import NickSetPlayerView
from views.set_host_nick_view import NickSetHostView
from views.game_view import GameView
from views.room_view import RoomView
from views.end_round_view import EndRoundView
from network_client import NetworkClient
from dotenv import load_dotenv
import os

load_dotenv()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Klient Gry")
        self.geometry(os.getenv("WINDOW_SIZE", "1100x600"))
        
        self.is_host = False
        self.player_nick = None
        self.pending_room_code = None
        self.current_page = "MenuView"

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MenuView, NickSetPlayerView, NickSetHostView, GameView, RoomView, EndRoundView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuView")
        
        ip = os.getenv("SERVER_IP", "127.0.0.1")
        port = int(os.getenv("SERVER_PORT", "12345"))
        self.network_client = NetworkClient(ip, port, self.handle_server_message)
        self.network_client.connect()

    def handle_server_message(self, message):
        parts = message.split('\n')
        for part in parts:
            if part.strip():
                self.after(0, lambda m=part: self._process_message(m))
    
    def _process_message(self, message):
        message = message.strip()

        if message.startswith("PLAYERS:"):
            if self.current_page in ["NickSetPlayerView", "NickSetHostView"]:
                if self.current_page == "NickSetPlayerView" and self.pending_room_code:
                    if "RoomView" in self.frames:
                        self.frames["RoomView"].set_room_code(self.pending_room_code)
                self.show_frame("RoomView")

            raw_data = message.split(":", 1)[1]
            players_list = [player.strip() for player in raw_data.split(",")]
            if "RoomView" in self.frames:
                self.frames["RoomView"].update_players(players_list)

        elif message.startswith("ROOM_CREATED:"):
            code = message.split(":")[1]
            if "RoomView" in self.frames:
                self.frames["RoomView"].set_room_code(code)
        
        elif message.startswith("JOIN_SUCCESS:"):
            code = message.split(":")[1]
            if "RoomView" in self.frames:
                self.frames["RoomView"].set_room_code(code)

        elif message.startswith("ERROR_NICK_TAKEN:"):
            if self.current_page in self.frames:
                frame = self.frames[self.current_page]
                if hasattr(frame, "show_error"):
                    frame.show_error("Nick jest zajęty! Wybierz inny.")

        elif message.startswith("ERROR_WRONG_ROOM_CODE:"):
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

        elif message.startswith("NEW_ROUND"):
            if "GameView" in self.frames:
                self.show_frame("GameView")
                self.frames["GameView"].start_new_round()
        
        elif message == "ROUND_OVER":
            self.show_frame("EndRoundView")
            if "EndRoundView" in self.frames:
                self.frames["EndRoundView"].start_countdown()

        elif message.startswith("LEADERBOARD:"):
        
            raw_data = message.split(":", 1)[1]
            ranking_entries = [r for r in raw_data.split(";") if r]
            
            formatted_lines = []
            for idx, entry in enumerate(ranking_entries, 1):
                if "," in entry:
                    nick, score = entry.split(",") 
                    formatted_lines.append(f"{idx}. {nick} - {score}")
                    
                    if nick == self.player_nick:
                        if "GameView" in self.frames:
                            self.frames["GameView"].update_score(score)

            formatted_ranking = "\n".join(formatted_lines)

            if "GameView" in self.frames:
                self.frames["GameView"].update_ranking(formatted_ranking)
            
            if "EndRoundView" in self.frames:
                self.frames["EndRoundView"].update_ranking(formatted_ranking)

        elif message.startswith("INCORRECT:"):
            parts = message.split(";")
            nick_part = parts[0]
            guesser_nick = nick_part.split(":")[1]

            if guesser_nick == self.player_nick:
                if "GameView" in self.frames:
                    self.frames["GameView"].show_guess_result("WRONG")
        
        elif message.startswith("CORRECT:"):
            parts = message.split(";")
            nick_part = parts[0]
            winner_nick = nick_part.split(":")[1]

            if winner_nick == self.player_nick:
                if "GameView" in self.frames:
                    self.frames["GameView"].show_guess_result("CORRECT")
            self.show_frame("EndRoundView")
            if "EndRoundView" in self.frames:
                self.frames["EndRoundView"].start_countdown()
            
        elif message.startswith("HASHPASS:"):
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