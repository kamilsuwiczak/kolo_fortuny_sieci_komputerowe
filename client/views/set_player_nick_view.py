import customtkinter as ctk
from dotenv import load_dotenv
import os

load_dotenv()

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

        self.btn_confirm = ctk.CTkButton(self, text="Potwierdź", width=200, height=40, command=self.confirm_nick)
        self.btn_confirm.pack(pady=10)

    def confirm_nick(self):
        nick = self.entry_nick.get()
        code = self.entry_code.get()
        print(f"Nick: {nick}, Kod: {code}")
        self.controller.show_frame("RoomView")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry(os.getenv("WINDOW_SIZE", "1000x600"))
    nick_view = NickSetPlayerView(parent=app, controller=app)
    nick_view.pack(fill="both", expand=True)
    app.mainloop()