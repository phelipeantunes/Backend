import mysql.connector
from clientes import cliente
from unidades import unidade
from produtos import produto
from flask import *
from tkinter import *

app = Flask(__name__)
app.secret_key = "super secret key"

# Rotas de cliente, referenciam o módulo clientes.
@app.route('/lista_clientes')
def listar():
    return cliente.listar_clientes()

@app.route('/cadastrar_clientes', methods=['GET', 'POST'])
def cadastrar_cliente():
    return cliente.cadastrar_cliente()

@app.route('/editar_clientes/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    return cliente.editar_cliente(cliente_id)

@app.route('/excluir_clientes/<int:cliente_id>', methods=['GET'])
def excluir_cliente(cliente_id):
    return cliente.excluir_cliente(cliente_id)



# Rotas de unidade, referenciam o módulo unidades.
@app.route('/lista_unidades')
def lista_unidades():
    return unidade.listar_unidades()

# Rota para cadastrar uma Unidade
@app.route('/cadastrar_unidade', methods=['GET', 'POST'])
def cadastrar_unidade():
    return unidade.cadastrar_unidade()

# Rota para editar uma unidade
@app.route('/editar_unidade/<int:unidade_id>', methods=['GET', 'POST'])
def editar_unidade(unidade_id):
    return unidade.editar_unidade(unidade_id)

# Rota para excluir uma unidade
@app.route('/excluir_unidade/<int:unidade_id>', methods=['GET'])
def excluir_unidade(unidade_id):
    return unidade.excluir_unidade(unidade_id)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



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
def lista_produtos():
    return produto.listar_produtos()

# Rota para cadastrar um novo produto
@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    return produto.cadastrar_produto()

# Rota para editar um produto
@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    return produto.editar_produto(id)

# Rota para excluir um produto
@app.route('/excluir_produto/<int:id>', methods=['GET'])
def excluir_produto(id):
    return produto.excluir_produto(id)


if __name__ == '__main__':
    app.run(debug=True)