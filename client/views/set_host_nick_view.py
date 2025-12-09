import customtkinter as ctk
from dotenv import load_dotenv
import os
load_dotenv()

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
        print(f"Nick hosta ustawiony na: {nick}")
        # Tutaj możesz wysłać nick do serwera lub przejść do innego widoku
        self.controller.show_frame("GameView")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry(os.getenv("WINDOW_SIZE", "1000x600"))
    nick_view = NickSetHostView(parent=app, controller=app)
    nick_view.pack(fill="both", expand=True)
    app.mainloop()