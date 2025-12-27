import customtkinter as ctk

class EndGameView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label_title = ctk.CTkLabel(self, text="KONIEC GRY", font=("Arial", 40, "bold"), text_color="red")
        self.label_title.pack(pady=(50, 20))

        self.label_subtitle = ctk.CTkLabel(self, text="Ostateczny Ranking", font=("Arial", 24))
        self.label_subtitle.pack(pady=(0, 20))

        self.ranking_box = ctk.CTkTextbox(self, width=500, height=300, font=("Arial", 18))
        self.ranking_box.pack(pady=10)
        self.ranking_box.configure(state="disabled")

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(pady=40)

        self.btn_room = ctk.CTkButton(self.buttons_frame, text="Wróć do pokoju", command=self.go_to_room, width=200, height=50, fg_color="blue", hover_color="darkblue")
        self.btn_room.pack(side="left", padx=20)

        self.btn_menu = ctk.CTkButton(self.buttons_frame, text="Wróć do menu", command=self.go_to_menu, width=200, height=50, fg_color="red", hover_color="darkred")
        self.btn_menu.pack(side="left", padx=20)

    def update_final_ranking(self, ranking_text):
        self.ranking_box.configure(state="normal")
        self.ranking_box.delete("0.0", "end")
        self.ranking_box.insert("0.0", ranking_text)
        self.ranking_box.configure(state="disabled")

    def go_to_room(self):
        self.controller.show_frame("RoomView")

    def go_to_menu(self):
        self.controller.network_client.send("LEAVE_ROOM")
        self.controller.show_frame("MenuView")