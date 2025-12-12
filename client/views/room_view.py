import customtkinter as ctk
from dotenv import load_dotenv
import os
load_dotenv()

class RoomView(ctk.CTkFrame):
    def __init__(self, parent, controller, player_type = "player"):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Pokój gry", font=("Arial", 24))
        self.label.pack(pady=20)

        self.label_info = ctk.CTkLabel(self, text="Gracze: ", font=("Arial", 20))
        self.label_info.pack(pady=10)

        self.players_list = ctk.CTkTextbox(self, width=400, height=200)
        self.players_list.pack(pady=10)
      
        self.players_list.configure(state="disabled") 

        if player_type == "host":
            self.btn_start = ctk.CTkButton(self, text="Rozpocznij grę", command=self.start_game)
            self.btn_start.pack(pady=20)


    def start_game(self):
        print("Gra rozpoczęta!")
        
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry(os.getenv("WINDOW_SIZE", "1000x600"))
    players = ["player1", "player2", "player3"]
    room_view = RoomView(parent=app, controller=app, player_type="host")
    room_view.players_list.configure(state="normal")
    room_view.players_list.insert("0.0", "\n".join(f"{i+1}. {name}" for i, name in enumerate(players)))
    room_view.players_list.configure(state="disabled")
    room_view.pack(fill="both", expand=True)
    app.mainloop()
