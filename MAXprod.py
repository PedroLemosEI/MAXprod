import tkinter as tk
from tkinter import messagebox
import winsound
import time

class ContadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App de Foco - 90/20/20")
        self.root.geometry("300x250")
        self.root.configure(bg="#2c3e50")

        self.tempo_restante = 90 * 60
        self.modo = "ESTUDO" # Modos: ESTUDO, PAUSA, MICRO
        self.rodando = False
        self.tempo_estudo_pausado = 0

        # Interface
        self.label_status = tk.Label(root, text="ESTUDO", font=("Arial", 14, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.label_status.pack(pady=10)

        self.label_timer = tk.Label(root, text="90:00", font=("Arial", 40), bg="#2c3e50", fg="#e74c3c")
        self.label_timer.pack(pady=10)

        self.btn_start = tk.Button(root, text="Iniciar", command=self.toggle_timer, width=10)
        self.btn_start.pack(side=tk.LEFT, padx=20)

        self.btn_break = tk.Button(root, text="BREAK (20s)", command=self.trigger_micro_break, state=tk.DISABLED, width=12)
        self.btn_break.pack(side=tk.RIGHT, padx=20)

        self.update_clock()

    def play_alarm(self):
        # Som de sistema do Windows
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

    def toggle_timer(self):
        self.rodando = not self.rodando
        self.btn_start.config(text="Pausar" if self.rodando else "Retomar")
        if self.modo == "ESTUDO":
            self.btn_break.config(state=tk.NORMAL if self.rodando else tk.DISABLED)

    def trigger_micro_break(self):
        if self.modo == "ESTUDO":
            self.tempo_estudo_pausado = self.tempo_restante
            self.modo = "MICRO"
            self.tempo_restante = 20
            self.label_status.config(text="MICRO BREAK", fg="#f1c40f")
            self.label_timer.config(fg="#f1c40f")
            self.play_alarm()

    def update_clock(self):
        if self.rodando and self.tempo_restante > 0:
            self.tempo_restante -= 1
        elif self.rodando and self.tempo_restante <= 0:
            self.play_alarm()
            self.handle_transition()

        minutos, segundos = divmod(self.tempo_restante, 60)
        self.label_timer.config(text=f"{minutos:02d}:{segundos:02d}")
        self.root.after(1000, self.update_clock)

    def handle_transition(self):
        if self.modo == "ESTUDO":
            self.modo = "PAUSA"
            self.tempo_restante = 20 * 60
            self.label_status.config(text="PAUSA LONGA", fg="#2ecc71")
            self.label_timer.config(fg="#2ecc71")
            self.btn_break.config(state=tk.DISABLED)
            messagebox.showinfo("Fim de Ciclo", "Hora da pausa de 20 minutos!")
        
        elif self.modo == "PAUSA":
            self.modo = "ESTUDO"
            self.tempo_restante = 90 * 60
            self.label_status.config(text="ESTUDO", fg="#ecf0f1")
            self.label_timer.config(fg="#e74c3c")
            messagebox.showinfo("Foco!", "De volta ao estudo (90 min)!")

        elif self.modo == "MICRO":
            self.modo = "ESTUDO"
            self.tempo_restante = self.tempo_estudo_pausado
            self.label_status.config(text="ESTUDO (Retomado)", fg="#ecf0f1")
            self.label_timer.config(fg="#e74c3c")
            messagebox.showinfo("Fim do Micro Break", "A retomar o contador de estudo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorApp(root)
    root.mainloop()