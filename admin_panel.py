import tkinter as tk
from tkinter import messagebox
from db import connect_db

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel do Administrador")
        self.root.geometry("500x400")

        self.login_screen()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login do Administrador", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Usuário:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Entrar", command=self.check_login).pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.load_question_form()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def load_question_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Cadastrar Nova Pergunta", font=("Arial", 16)).pack(pady=10)

        self.q_entry = tk.Entry(self.root, width=60)
        self.q_entry.insert(0, "Digite a pergunta")
        self.q_entry.pack(pady=5)

        self.options = {}
        for opt in ['A', 'B', 'C', 'D']:
            tk.Label(self.root, text=f"Opção {opt}:").pack()
            entry = tk.Entry(self.root, width=50)
            entry.pack()
            self.options[opt] = entry

        tk.Label(self.root, text="Alternativa correta (A/B/C/D):").pack()
        self.correct_entry = tk.Entry(self.root)
        self.correct_entry.pack()

        tk.Button(self.root, text="Salvar pergunta", command=self.save_question).pack(pady=10)
        tk.Button(self.root, text="Gerenciar Perguntas", command=self.manage_questions).pack(pady=5)
        tk.Button(self.root, text="Sair", command=self.login_screen).pack(pady=5)


    def save_question(self):
        question = self.q_entry.get().strip()
        correct = self.correct_entry.get().strip().upper()

        if not question or correct not in ['A', 'B', 'C', 'D']:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        options = {k: self.options[k].get().strip() for k in self.options}
        if any(not v for v in options.values()):
            messagebox.showerror("Erro", "Todas as opções devem ser preenchidas.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            question,
            options['A'],
            options['B'],
            options['C'],
            options['D'],
            correct
        ))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Pergunta adicionada com sucesso!")
        self.load_question_form()

    def manage_questions(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Perguntas Cadastradas", font=("Arial", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=80)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, question FROM questions ORDER BY id")
        questions = cursor.fetchall()
        conn.close()

        for q in questions:
            listbox.insert(tk.END, f"ID {q[0]}: {q[1]}")

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Campo para deletar
        tk.Label(self.root, text="Digite o ID da pergunta para deletar:").pack(pady=5)
        self.delete_entry = tk.Entry(self.root)
        self.delete_entry.pack()

        tk.Button(self.root, text="Deletar", command=self.delete_question).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.load_question_form).pack(pady=5)

    def delete_question(self):
        try:
            qid = int(self.delete_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id = %s", (qid,))
        if cursor.fetchone() is None:
            conn.close()
            messagebox.showerror("Erro", "Pergunta não encontrada.")
            return

        cursor.execute("DELETE FROM questions WHERE id = %s", (qid,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Pergunta ID {qid} deletada.")
        self.manage_questions()  # Recarrega a lista



if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()
