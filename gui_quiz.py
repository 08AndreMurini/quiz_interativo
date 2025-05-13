import tkinter as tk
from tkinter import messagebox
from questions import get_all_questions
from db import create_tables
import subprocess

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Interativo")
        self.root.geometry("500x400")
        
        self.username = ""
        self.questions = get_all_questions()
        self.current_question = 0
        self.score = 0
        self.selected_option = tk.StringVar()

        self.create_login_screen()

    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Digite seu nome:", font=("Arial", 14)).pack(pady=20)
        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.name_entry.pack()

        tk.Button(self.root, text="Iniciar Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.root, text="Painel do Administrador", command=self.open_admin_panel).pack(pady=5)


    def start_quiz(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Aviso", "Digite seu nome antes de começar.")
            return

        self.username = name
        self.current_question = 0
        self.score = 0
        self.questions = get_all_questions()
        self.load_question()


    def load_question(self):
        if self.current_question >= len(self.questions):
            self.show_result()
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        q = self.questions[self.current_question]

        tk.Label(self.root, text=f"Pergunta {self.current_question + 1}", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text=q['question'], font=("Arial", 12), wraplength=450).pack(pady=10)

        self.selected_option.set(None)
        options = ['A', 'B', 'C', 'D']
        for opt in options:
            text = q[f'option_{opt.lower()}']
            tk.Radiobutton(
                self.root, text=text, variable=self.selected_option, value=opt,
                font=("Arial", 12)
            ).pack(anchor="w", padx=50)

        tk.Button(self.root, text="Próxima", command=self.next_question).pack(pady=20)

    def next_question(self):
        selected = self.selected_option.get()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione uma alternativa.")
            return

        correct = self.questions[self.current_question]['correct_option']
        if selected == correct:
            self.score += 1

        self.current_question += 1
        self.load_question()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=f"Parabéns, {self.username}!", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Sua pontuação: {self.score}/{len(self.questions)}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Sair", command=self.root.quit).pack(pady=20)

    def open_admin_panel(self):
        try:
            subprocess.Popen(["python", "admin_panel.py"])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o painel: {e}")


if __name__ == "__main__":
    from questions import insert_sample_questions

    create_tables()
    insert_sample_questions()  # Você pode comentar esta linha após inserir uma vez

    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
