from db import connect_db

def insert_sample_questions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]

    if count == 0:
        questions = [
            ("Qual é o resultado da expressão: 3 * (2 + 1)?", "6", "9", "5", "7", "B"),
            ("Qual estrutura de controle usamos para repetir um bloco de código?", "if", "while", "break", "def", "B"),
            ("Qual desses é um operador lógico?", "=", "==", "or", "%", "C"),
            ("Qual a função do comando 'def' em Python?", "Definir uma condição", "Definir uma função", "Encerrar um loop", "Importar bibliotecas", "B"),
            ("Qual dessas estruturas representa uma lista em Python?", "{}", "()", "[]", "<>", "C")
        ]

        cursor.executemany("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, questions)

        conn.commit()

    conn.close()

def get_all_questions():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return questions
