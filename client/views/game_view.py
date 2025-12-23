import customtkinter as ctk
from dotenv import load_dotenv
import os

load_dotenv()

class GameView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.ranking_frame = ctk.CTkFrame(self, height=150)
        self.ranking_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.lbl_ranking_title = ctk.CTkLabel(self.ranking_frame, text="Ranking Graczy", font=("Arial", 14, "bold"))
        self.lbl_ranking_title.pack(pady=5)
        
        self.ranking_text = ctk.CTkTextbox(self.ranking_frame, height=100)
        self.ranking_text.pack(padx=5, pady=5, fill="both", expand=True)
        self.ranking_text.insert("0.0", "1. GraczA - 500\n2. GraczB - 300\n3. Ty - 100")
        self.ranking_text.configure(state="disabled")

        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10)) 
        
        self.lbl_history_title = ctk.CTkLabel(self.history_frame, text="Użyte hasła", font=("Arial", 14, "bold"))
        self.lbl_history_title.pack(pady=5)

        self.history_text = ctk.CTkTextbox(self.history_frame)
        self.history_text.pack(padx=5, pady=5, fill="both", expand=True)
        self.history_text.configure(state="disabled")

        self.btn_back = ctk.CTkButton(self, text="Wyjdź do menu", command=self.go_back, fg_color="red", hover_color="darkred")
        self.btn_back.grid(row=2, column=0, sticky="sw", padx=20, pady=20)

        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=0, column=1, columnspan=2, rowspan=3, sticky="nsew")

        self.score_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.score_frame.place(relx=0.98, rely=0.02, anchor="ne")
        
        self.lbl_score = ctk.CTkLabel(self.score_frame, text="Twoje Punkty: 120", font=("Arial", 20, "bold"))
        self.lbl_score.pack(anchor="e")

        self.lbl_code = ctk.CTkLabel(self.score_frame, text="Kod pokoju: ABC123", font=("Arial", 20, "bold"))
        self.lbl_code.pack(anchor="e")

        self.lbl_timer = ctk.CTkLabel(self.score_frame, text="Czas: 60s", font=("Arial", 20, "bold"), text_color="orange")
        self.lbl_timer.pack(anchor="e", pady=(5, 0))

        self.game_content = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.game_content.place(relx=0.5, rely=0.5, anchor="center")

        self.label_word = ctk.CTkLabel(self.game_content, text="_ _ _ _ _ _ _ _ ", font=("Courier", 60, "bold"))
        self.label_word.pack(pady=(0, 40))

        self.input_frame = ctk.CTkFrame(self.game_content, fg_color="transparent")
        self.input_frame.pack()

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Zgadnij...", width=200, height=40, font=("Arial", 16))
        self.entry.pack(side="left", padx=10)
        
        self.entry.bind('<Return>', self.send_guess)

        self.btn_submit = ctk.CTkButton(self.input_frame, text="Zatwierdź", command=self.send_guess, height=40, fg_color="green", hover_color="darkgreen")
        self.btn_submit.pack(side="left")

        self.start_timer()

    def send_guess(self, event=None):
        guess = self.entry.get()
        if not guess: return

        print(f"Wysyłam: {guess}")
    
        self.history_text.configure(state="normal")
        self.history_text.insert("0.0", f"{guess}\n")
        self.history_text.configure(state="disabled")

        self.entry.delete(0, 'end')
        self.entry.focus() 

    def go_back(self):
        print("Powrót do menu")
        self.stop_timer()
        self.controller.show_frame("MenuView")

    def start_timer(self):
        self.time_left = 60
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.lbl_timer.configure(text=f"Czas: {self.time_left}s", text_color="orange")
            self.time_left -= 1
            self.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.lbl_timer.configure(text="KONIEC CZASU!", text_color="red")
            self.timer_running = False
            self.entry.configure(state="disabled")
            self.btn_submit.configure(state="disabled")

if __name__ == "__main__":
    app = ctk.CTk()
    window_size = os.getenv("WINDOW_SIZE", "1100x600")
    app.geometry(window_size)
    app.title("Koło Fortuny")
    
    game_view = GameView(parent=app, controller=app)
    game_view.pack(fill="both", expand=True)
    
    app.mainloop()