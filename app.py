from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexão com o banco de dados
def init_db():
    with sqlite3.connect('database/financas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS gastos (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           descricao TEXT NOT NULL,
                           valor REAL NOT NULL,
                           categoria TEXT NOT NULL,
                           data TEXT NOT NULL
                       )
                       ''')
    print("Banco de dados inicializando.")
    
init_db()

# Página inicial
@app.route("/")
def index():
    with sqlite3.connect('database/financas.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos")
        registros = cursor.fetchall()
    return render_template("index.html", registros=registros)

# Adicionar para adicionar um gasto
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        categoria = request.form['categoria']
        data = request.form['data']
        
        with sqlite3.connect('database/financas.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO gastos (descricao, valor, categoria, data)
                           VALUES (?, ?, ?, ?)
                           ''', (descricao, valor, categoria, data))
            conn.commit()
        return redirect(url_for('index'))
                       
    return render_template('adicionar.html')

if __name__ == "__main__":
    app.run(debug=True)
