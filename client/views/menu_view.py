import customtkinter as ctk
from dotenv import load_dotenv
import os
load_dotenv()

class MenuView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 

        self.label = ctk.CTkLabel(self, text="Koło fortuny", font=("Arial", 24))
        self.label.pack(pady=20)

        self.label_info = ctk.CTkLabel(self, text="- - - - - - - - - ", font=("Arial", 70))
        self.label_info.pack(pady=10)
        
        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.pack()
        
        self.btn_join = ctk.CTkButton(self.button_container, text="Dołącz do pokoju", command=self.go_to_nick_player)
        self.btn_join.pack(side = "left", padx=20, pady=80)

        self.btn_create = ctk.CTkButton(self.button_container, text="Stwórz nowy pokój", command=self.go_to_nick_host)
        self.btn_create.pack(side = "left", padx=20, pady=80)

    def go_to_nick_player(self):
        print("Przełączam na widok playera")
        # self.controller.show_frame("NickSetPlayerView")

    def go_to_nick_host(self):
        print("Przełączam na widok hosta")
        # self.controller.show_frame("NickSetHostView")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry(os.getenv("WINDOW_SIZE", "1000x600"))
    menu_view = MenuView(parent=app, controller=app)
    menu_view.pack(fill="both", expand=True)
    app.mainloop()