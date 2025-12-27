import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv
import os
load_dotenv()

class RoomView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label_code = ctk.CTkLabel(self, text="KOD: ----", font=("Arial", 20, "bold"), text_color="orange")
        self.label_code.place(relx=0.95, rely=0.05, anchor="ne")

        self.btn_back = ctk.CTkButton(self, text="Wyjdź do menu", command=self.confirm_exit, fg_color="red", hover_color="darkred")
        self.btn_back.place(relx=0.02, rely=0.98, anchor="sw")

        self.label = ctk.CTkLabel(self, text="Pokój gry", font=("Arial", 24))
        self.label.pack(pady=20)

        self.label_info = ctk.CTkLabel(self, text="Gracze: ", font=("Arial", 20))
        self.label_info.pack(pady=10)

        self.players_list = ctk.CTkTextbox(self, width=400, height=200)
        self.players_list.pack(pady=10)
        self.players_list.configure(state="disabled") 

        self.btn_start = ctk.CTkButton(self, text="Rozpocznij grę", command=self.start_game, fg_color="green")

    def refresh_view(self):
        if self.controller.is_host:
            self.btn_start.pack(pady=20)
        else:
            self.btn_start.pack_forget()

    def set_room_code(self, code):
        self.label_code.configure(text=f"KOD: {code}")

    def confirm_exit(self):
        answer = messagebox.askyesno("Wyjście", "Czy na pewno chcesz opuścić lobby?")
        if answer:
            self.exit_room()

    def exit_room(self):
        self.controller.network_client.send("LEAVE_ROOM")
        self.controller.show_frame("MenuView")

    def start_game(self):
        self.controller.network_client.send("START_GAME 3")

    def update_players(self, players):
        self.players_list.configure(state="normal")
        self.players_list.delete("0.0", "end")
        for i, player in enumerate(players):
            self.players_list.insert("end", f"{i+1}. {player}\n")
        self.players_list.configure(state="disabled")
