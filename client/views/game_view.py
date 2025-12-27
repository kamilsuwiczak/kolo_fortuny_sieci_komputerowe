import customtkinter as ctk
from dotenv import load_dotenv

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
        
        self.lbl_nick = ctk.CTkLabel(self.score_frame, text="Gracz: ---", font=("Arial", 16, "bold"))
        self.lbl_nick.pack(anchor="e")

        self.lbl_score = ctk.CTkLabel(self.score_frame, text="Twoje Punkty: 0", font=("Arial", 20, "bold"))
        self.lbl_score.pack(anchor="e")

        self.lbl_code = ctk.CTkLabel(self.score_frame, text="Kod pokoju: ---", font=("Arial", 16, "bold"))
        self.lbl_code.pack(anchor="e")

        self.lbl_timer = ctk.CTkLabel(self.score_frame, text="Czas: 60s", font=("Arial", 20, "bold"), text_color="orange")
        self.lbl_timer.pack(anchor="e", pady=(5, 0))

        self.time_left = 60
        self.timer_running = False

        self.game_content = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.game_content.place(relx=0.5, rely=0.5, anchor="center")

        self.label_word = ctk.CTkLabel(self.game_content, text="", font=("Courier", 60, "bold"))
        self.label_word.pack(pady=(0, 40))

        self.input_frame = ctk.CTkFrame(self.game_content, fg_color="transparent")
        self.input_frame.pack()

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Zgadnij...", width=200, height=40, font=("Arial", 16))
        self.entry.pack(side="left", padx=10)
        
        self.entry.bind('<Return>', self.send_guess)

        self.btn_submit = ctk.CTkButton(self.input_frame, text="Zatwierdź", command=self.send_guess, height=40, fg_color="green", hover_color="darkgreen")
        self.btn_submit.pack(side="left")

        self.lbl_feedback = ctk.CTkLabel(self.game_content, text="", font=("Arial", 18, "bold"))
        self.lbl_feedback.pack(pady=10)

    def update_room_info(self, code, nick):
        self.lbl_code.configure(text=f"Kod pokoju: {code}")
        self.lbl_nick.configure(text=f"Gracz: {nick}")

    def start_new_round(self):
        self.entry.configure(state="normal")
        self.btn_submit.configure(state="normal")
        self.entry.delete(0, 'end')
        self.lbl_feedback.configure(text="")

        self.history_text.configure(state="normal")
        self.history_text.delete("0.0", "end")
        self.history_text.configure(state="disabled")

        self.stop_timer()
        self.start_timer()

    def send_guess(self, event=None):
        guess = self.entry.get()
        if not guess: return

        self.lbl_feedback.configure(text="")
        
        self.controller.network_client.send(f"GUESS {guess.upper()}")
    
        self.history_text.configure(state="normal")
        self.history_text.insert("0.0", f"{guess}\n")
        self.history_text.configure(state="disabled")

        self.entry.delete(0, 'end')
        self.entry.focus() 

    def show_guess_result(self, result):
        if result == "WRONG":
            self.lbl_feedback.configure(text="Złe hasło", text_color="red")
        elif result == "CORRECT":
            self.lbl_feedback.configure(text="Zgadłeś!", text_color="green")

    def update_word(self, new_word):
        word=""
        for i in range(len(new_word)):
            word+=new_word[i]+" "
            if i>=len(new_word)-1:
                break
        self.label_word.configure(text=word)
    
    def update_ranking(self, formatted_ranking_text):
        self.ranking_text.configure(state="normal")
        self.ranking_text.delete("0.0", "end")
        self.ranking_text.insert("0.0", formatted_ranking_text)
        self.ranking_text.configure(state="disabled")
    
    def update_score(self, score):
        self.lbl_score.configure(text=f"Twoje Punkty: {score}")

    def go_back(self):
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
        elif self.time_left == 0 and self.timer_running:
            self.lbl_timer.configure(text="KONIEC CZASU!", text_color="red")
            self.timer_running = False
            self.entry.configure(state="disabled")
            self.btn_submit.configure(state="disabled")