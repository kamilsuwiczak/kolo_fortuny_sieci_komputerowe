import customtkinter as ctk

class EndRoundView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label_title = ctk.CTkLabel(self, text="Koniec Rundy!", font=("Arial", 30, "bold"), text_color="orange")
        self.label_title.pack(pady=(40, 20))

        self.label_result = ctk.CTkLabel(self, text="", font=("Arial", 22, "bold"))
        self.label_result.pack(pady=(0, 20))

        self.ranking_label = ctk.CTkLabel(self, text="Ranking po tej rundzie:", font=("Arial", 20))
        self.ranking_label.pack(pady=10)

        self.ranking_text = ctk.CTkTextbox(self, width=400, height=200, font=("Arial", 16))
        self.ranking_text.pack(pady=10)
        self.ranking_text.configure(state="disabled")

        self.label_timer = ctk.CTkLabel(self, text="Następna runda za: 5s", font=("Arial", 24, "bold"))
        self.label_timer.pack(pady=30)
        
        self.time_left = 5
        self.timer_running = False

    def update_ranking(self, formatted_ranking_text):
        self.ranking_text.configure(state="normal")
        self.ranking_text.delete("0.0", "end")
        self.ranking_text.insert("0.0", formatted_ranking_text)
        self.ranking_text.configure(state="disabled")

    def display_round_result(self, text, color="white"):
        self.label_result.configure(text=text, text_color=color)

    def start_countdown(self):
        self.time_left = 5
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        """Metoda do natychmiastowego przerwania odliczania."""
        self.timer_running = False
        self.label_timer.configure(text="")

    def update_timer(self):
        if not self.timer_running:
            return

        if self.time_left > 0:
            self.label_timer.configure(text=f"Następna runda za: {self.time_left}s")
            self.time_left -= 1
            self.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.controller.show_frame("GameView")