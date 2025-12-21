import customtkinter as ctk

class NickSetHostView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Ustaw swój nick", font=("Arial", 24))
        self.label.pack(pady=(150,10))

        self.entry_nick = ctk.CTkEntry(self, placeholder_text="NICK")
        self.entry_nick.pack(pady=(10,0))

        self.btn_confirm = ctk.CTkButton(self, text="Potwierdź", command=self.confirm_nick)
        self.btn_confirm.pack(pady=10)

    def confirm_nick(self):
        nick = self.entry_nick.get()
        if not nick:
            return

        self.controller.is_host = True
        self.controller.player_nick = nick
        
        self.controller.network_client.send(f"CREATE_ROOM:{nick}")

        if "RoomView" in self.controller.frames:
            self.controller.frames["RoomView"].refresh_view()

        self.controller.show_frame("RoomView")