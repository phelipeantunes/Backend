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
@app.route('/lista_clientes')
def listar_clientes():
    cursor.execute("SELECT * FROM cliente")
    rows = cursor.fetchall()
    return render_template('lista_clientes.html', clientes=rows)

@app.route('/')
def home():
    cursor.execute("SELECT * FROM cliente")
    rows = cursor.fetchall()
    return render_template('index.html', clientes=rows)

@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')

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

    return redirect(url_for('lista_clientes'))

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

        return redirect(url_for('lista_clientes'))

    # Se for uma requisição GET, exibir o formulário de edição
    sql = "SELECT * FROM cliente WHERE id = %s"
    cursor.execute(sql, (cliente_id,))
    cliente = cursor.fetchone()
    return render_template('editar_cliente.html', cliente=cliente)

# Rota para cadastrar venda
@app.route('/cadastrar_venda', methods=['GET', 'POST'])
def cadastrar_venda():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        cliente_id = request.form['cliente_id']
        quantidade = request.form['quantidade']
        total = request.form['total']

        # Insira aqui o código para inserir a venda no banco de dados

        return redirect(url_for('lista_clientes'))

    # Consulta para obter a lista de produtos
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = cursor.fetchall()

    # Consulta para obter a lista de clientes
    cursor.execute("SELECT id, nome FROM cliente")
    clientes = cursor.fetchall()

    return render_template('cadastrar_venda.html', produtos=produtos, clientes=clientes)

# Página para editar uma venda
@app.route('/editar_venda/<int:venda_id>', methods=['GET', 'POST'])
def editar_venda(venda_id):
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        cliente_id = request.form['cliente_id']
        quantidade = request.form['quantidade']
        total = request.form['total']

        cursor.execute("UPDATE vendas SET produto_id=%s, cliente_id=%s, quantidade=%s, total=%s WHERE id=%s",
                       (produto_id, cliente_id, quantidade, total, venda_id))
        conn.commit()

        return redirect(url_for('listar_vendas'))

    cursor.execute("SELECT * FROM vendas WHERE id=%s", (venda_id,))
    venda = cursor.fetchone()
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM cliente")
    clientes = cursor.fetchall()

    return render_template('editar_venda.html', venda=venda, produtos=produtos, clientes=clientes)

# Rota para excluir uma venda
@app.route('/excluir_venda/<int:venda_id>', methods=['GET'])
def excluir_venda(venda_id):
    cursor.execute("DELETE FROM vendas WHERE id=%s", (venda_id,))
    conn.commit()
    return redirect(url_for('listar_vendas'))

# Página para listar todas as vendas
@app.route('/lista_vendas')
def listar_vendas():
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()
    return render_template('lista_vendas.html', vendas=vendas)

# Página inicial - Lista de produtos
@app.route('/lista_produtos')
def listar_produtos():
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    return render_template('lista_produtos.html', produtos=rows)

# Rota para cadastrar um novo produto
@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']

        sql = "INSERT INTO produtos (nome, descricao, preco) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, descricao, preco))
        conn.commit()

        return redirect(url_for('listar_produtos'))
    return render_template('cadastrar_produto.html')

# Rota para editar um produto
@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']

        sql = "UPDATE produtos SET nome = %s, descricao = %s, preco = %s WHERE id = %s"
        cursor.execute(sql, (nome, descricao, preco, id))
        conn.commit()

        return redirect(url_for('listar_produtos'))

    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    produto = cursor.fetchone()
    return render_template('editar_produto.html', produto=produto)

# Rota para excluir um produto
@app.route('/excluir_produto/<int:id>', methods=['GET'])
def excluir_produto(id):
    cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
    conn.commit()

    return redirect(url_for('listar_produtos'))

# Rota para listagem de unidades
@app.route('/lista_unidades')
def lista_unidades():
    cursor.execute("SELECT * FROM unidade")
    rows = cursor.fetchall()
    return render_template('lista_unidades.html', unidades=rows)


# Rota para cadastrar uma Unidade
@app.route('/cadastrar_unidade', methods=['GET', 'POST'])
def cadastrar_unidade():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        sql = "INSERT INTO unidade (nome, endereco, telefone) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, endereco, telefone))
        conn.commit()

        return redirect(url_for('listar_unidades'))
    return render_template('cadastrar_unidade.html')


# Rota para editar uma unidade
@app.route('/editar_unidade/<int:unidade_id>', methods=['GET', 'POST'])
def editar_unidade(unidade_id):
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        sql = "UPDATE unidade SET nome = %s, endereco = %s, telefone = %s WHERE id = %s"
        cursor.execute(sql, (nome, endereco, telefone, unidade_id))
        conn.commit()

        return redirect(url_for('lista_unidades'))

    cursor.execute("SELECT * FROM unidade WHERE id = %s", (unidade_id,))
    unidade = cursor.fetchone()
    return render_template('editar_unidade.html', unidade=unidade)

# Rota para excluir uma unidade
@app.route('/excluir_unidade/<int:unidade_id>', methods=['GET'])
def excluir_unidade(unidade_id):
    cursor.execute("DELETE FROM unidade WHERE id = %s", (unidade_id,))
    conn.commit()

    return redirect(url_for('lista_unidade'))


if __name__ == '__main__':
    app.run(debug=True)