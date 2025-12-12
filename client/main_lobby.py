import customtkinter as ctk
from views.menu_view import MenuView
from views.set_player_nick_view import NickSetPlayerView
from views.set_host_nick_view import NickSetHostView
from views.game_view import GameView
from views.room_view import RoomView

from dotenv import load_dotenv
import os
load_dotenv()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Klient Gry")
        self.geometry(os.getenv("WINDOW_SIZE", "1000x600"))
        
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

    def show_frame(self, page_name):
        """Funkcja, która wyciąga dany widok na wierzch"""
        frame = self.frames[page_name]
        frame.tkraise() 

if __name__ == "__main__":
    app = App()
    app.mainloop()