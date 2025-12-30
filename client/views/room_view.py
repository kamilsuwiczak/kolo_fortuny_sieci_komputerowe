import customtkinter as ctk
from tkinter import messagebox

class RoomView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.place(relx=0.95, rely=0.05, anchor="ne")

        self.label_nick = ctk.CTkLabel(self.info_frame, text="NICK: ---", font=("Arial", 16, "bold"))
        self.label_nick.pack(anchor="e")

        self.label_code = ctk.CTkLabel(self.info_frame, text="KOD: ----", font=("Arial", 20, "bold"), text_color="orange")
        self.label_code.pack(anchor="e")

        self.btn_back = ctk.CTkButton(self, text="Wyjdź do menu", command=self.confirm_exit, fg_color="red", hover_color="darkred")
        self.btn_back.place(relx=0.02, rely=0.98, anchor="sw")

        self.label = ctk.CTkLabel(self, text="Pokój gry", font=("Arial", 24))
        self.label.pack(pady=20)

        self.label_info = ctk.CTkLabel(self, text="Gracze: ", font=("Arial", 20))
        self.label_info.pack(pady=10)

        self.players_list = ctk.CTkTextbox(self, width=400, height=200)
        self.players_list.pack(pady=10)
        self.players_list.configure(state="disabled") 

        self.rounds_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.label_rounds = ctk.CTkLabel(self.rounds_frame, text="Liczba rund:", font=("Arial", 16))
        self.label_rounds.pack(side="left", padx=10)

        self.rounds_var = ctk.StringVar(value="3")
        self.rounds_option = ctk.CTkOptionMenu(self.rounds_frame, values=["2", "3", "4", "5", "6", "7", "8", "9"], variable=self.rounds_var)
        self.rounds_option.pack(side="left")

        self.btn_start = ctk.CTkButton(self, text="Rozpocznij grę", command=self.start_game, fg_color="green")

    def refresh_view(self):
        if self.controller.is_host:
            self.rounds_frame.pack(pady=5)
            self.btn_start.pack(pady=20)
        else:
            self.rounds_frame.pack_forget()
            self.btn_start.pack_forget()

    def update_room_info(self, code, nick):
        self.label_code.configure(text=f"KOD: {code}")
        self.label_nick.configure(text=f"Gracz: {nick}")

    def confirm_exit(self):
        answer = messagebox.askyesno("Wyjście", "Czy na pewno chcesz opuścić lobby?")
        if answer:
            self.exit_room()

    def exit_room(self):
        self.controller.network_client.send("LEAVE_ROOM")
        self.controller.show_frame("MenuView")

    def start_game(self):
        rounds = self.rounds_var.get()
        self.controller.network_client.send(f"START_GAME {rounds}")

    def update_players(self, players):
        self.players_list.configure(state="normal")
        self.players_list.delete("0.0", "end")
        for i, player in enumerate(players):
            self.players_list.insert("end", f"{i+1}. {player}\n")
        self.players_list.configure(state="disabled")