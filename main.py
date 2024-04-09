import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from tkinter import *

app = Flask(__name__)

# Conectando ao banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="app_sust"
)
cursor = conn.cursor()
# Página inicial - Lista de clientes
@app.route('/')
def listar_clientes():
    cursor.execute("SELECT * FROM cliente")
    rows = cursor.fetchall()
    return render_template('lista_clientes.html', clientes=rows)

# Página para cadastrar um novo cliente
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        sql = "INSERT INTO cliente (nome, email, telefone) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, telefone))
        conn.commit()

        return redirect(url_for('listar_clientes'))
    return render_template('cadastrar_cliente.html')



@app.route('/excluir/<int:cliente_id>', methods=['GET'])
def excluir_cliente(cliente_id):
    # Excluir o cliente do banco de dados
    cursor.execute("DELETE FROM cliente WHERE id = %s", (cliente_id,))
    conn.commit()

    return redirect(url_for('listar_clientes'))

@app.route('/editar/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    if request.method == 'POST':
        # Obter os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        # Atualizar os dados do cliente no banco de dados
        sql = "UPDATE cliente SET nome = %s, email = %s, telefone = %s WHERE id = %s"
        cursor.execute(sql, (nome, email, telefone, cliente_id))
        conn.commit()

        return redirect(url_for('listar_clientes'))

    # Se for uma requisição GET, exibir o formulário de edição
    sql = "SELECT * FROM cliente WHERE id = %s"
    cursor.execute(sql, (cliente_id,))
    cliente = cursor.fetchone()
    return render_template('editar_cliente.html', cliente=cliente)




if __name__ == '__main__':
    app.run(debug=True)