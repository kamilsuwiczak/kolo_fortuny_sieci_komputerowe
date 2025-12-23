import customtkinter as ctk

class NickSetPlayerView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.inputs_container = ctk.CTkFrame(self, fg_color="transparent")
        self.inputs_container.pack(pady=70) 

        self.nick_frame = ctk.CTkFrame(self.inputs_container, fg_color="transparent")
        self.nick_frame.pack(side="left", padx=20) 
        
        self.label_nick = ctk.CTkLabel(self.nick_frame, text="Ustaw swój nick", font=("Arial", 20))
        self.label_nick.pack(pady=(0, 10))

        self.entry_nick = ctk.CTkEntry(self.nick_frame, placeholder_text="NICK")
        self.entry_nick.pack()

        self.code_frame = ctk.CTkFrame(self.inputs_container, fg_color="transparent")
        self.code_frame.pack(side="left", padx=20)

        self.label_code = ctk.CTkLabel(self.code_frame, text="Wpisz kod pokoju", font=("Arial", 20))
        self.label_code.pack(pady=(0, 10))

        self.entry_code = ctk.CTkEntry(self.code_frame, placeholder_text="KOD POKOJU")
        self.entry_code.pack()

        self.label_error = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 14))
        self.label_error.pack(pady=5)

        self.btn_confirm = ctk.CTkButton(self, text="Potwierdź", width=200, height=40, command=self.confirm_nick)
        self.btn_confirm.pack(pady=10)

    def show_error(self, message):
        self.label_error.configure(text=message)

    def confirm_nick(self):
        nick = self.entry_nick.get()
        code = self.entry_code.get()

        if not nick or not code:
            self.show_error("Wypełnij wszystkie pola!")
            return
        
        if len(nick) > 50:
            self.show_error("Nick jest za długi!")
            return
        
        if ' ' in nick:
            self.show_error("Nick nie może zawierać spacji!")
            return

        if ' ' in code: 
            self.show_error("Kod pokoju nie może zawierać spacji!")
            return

        self.show_error("")

        self.controller.is_host = False
        self.controller.player_nick = nick
        self.controller.pending_room_code = code
        
        self.controller.network_client.send(f"JOIN_ROOM {code} {nick}")