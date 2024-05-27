from flask import Flask, render_template, jsonify
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import traceback

import pyrebase
import pandas as pd

app = Flask(__name__, static_folder='assests')

# Configuração do Firebase
firebaseConfig = {
  "apiKey": "AIzaSyAtOpaz1bzClErSlBWZROF53fX5AQprWlc",
  "authDomain": "projetosust-a925b.firebaseapp.com",
  "projectId": "projetosust-a925b",
  "storageBucket": "projetosust-a925b.appspot.com",
  "messagingSenderId": "1085249179216",
  "appId": "1:1085249179216:web:902fce98827d3f650dcb55",
  "measurementId": "G-DNDSE984B2",
  "databaseURL": "https://projetosust-a925b-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


def getSession():
    try:
        session['user']
        return True
    except:
        return False

# Rota inicial
@app.route('/')
def index():
    if(getSession()):
        if 'user' in session:
            # Obter a lista de usuários do Firebase
            usuarios = db.child("users").get().val()
            return render_template('index.html', usuarios=usuarios)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            return redirect(url_for('index'))
        except:
            error = 'Credenciais inválidas. Por favor, tente novamente.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Rota de registro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['userName']
        email = request.form['email']
        password = request.form['password']

        # Verifica se o email já está cadastrado
        # users = db.child("users").order_by_child("email").equal_to(email).get()
        # if users.each():
        #     error = 'Email já está em uso. Por favor, use outro email.'
        #     return render_template('register.html', error=error)
        
        try:
            auth.create_user_with_email_and_password(email, password)
            user = {"email": email, "name": name}
            db.child("users").push(user)
            return redirect(url_for('login'))
        except:
            error = 'Erro ao registrar. Por favor, tente novamente.'
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')

# Rota de lista de produtos
@app.route('/lista_produtos', methods=['GET', 'POST'])
def lista_produtos():
    if request.method == 'GET':
        if getSession():
            produtos = db.child("produtos").get().val()
            unidades = db.child("unidades").get().val()
            categorias = set(produto['categoria'] for produto in produtos.values())  # Extract unique categories from produtos
            return render_template('lista_produtos.html', produtos=produtos, unidades=unidades, categorias=categorias)
        else:
            return redirect(url_for('login'))
    elif request.method == 'POST':
        id_produto_deletar = request.form.get('id_produto_deletar')
        try:
            db.child("produtos").child(id_produto_deletar).remove()
            return redirect(url_for('lista_produtos'))
        except Exception as e:
            traceback.print_exc()  # Imprime a exceção no console para depuração
            return "Ocorreu um erro ao excluir o produto: " + str(e), 500

# Rota para cadastrar produto
@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        categoria = request.form['categoria']
        unidadeProduto = request.form['unidadeProduto']
        nova_categoria = request.form['nova_categoria']

        if categoria == 'nova_categoria' and nova_categoria:
            categorias = db.child("categorias").get().val() or []
            categorias.append(nova_categoria)
            db.child("categorias").set(categorias)
            categoria = nova_categoria

        produto = {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "categoria": categoria,
            "unidadeProduto": unidadeProduto
        }

        db.child("produtos").push(produto)

        return redirect(url_for('lista_produtos'))
    else:
        unidades = db.child("unidades").get().val()
        categorias = db.child("categorias").get().val() or []
        return render_template('cadastrar_produto.html', unidades=unidades, categorias=categorias)

# Rota de edição de produto
@app.route('/editar_produto/<id>', methods=['GET', 'POST'])
def editar_produto(id):
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        categoria = request.form['categoria']
        unidadeProduto = request.form['unidadeProduto']

        db.child("produtos").child(id).update({
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "categoria": categoria,
            "unidadeProduto": unidadeProduto
        })
        return redirect(url_for('lista_produtos'))
    else:
        produto = db.child("produtos").child(id).get().val()
        unidades = db.child("unidades").get().val()
        categorias = db.child("categorias").get().val() or []
        return render_template('editar_produto.html', unidades=unidades, categorias=categorias, produto=produto)

# Rota de deleção de produto
@app.route('/deletar_produto/<id>', methods=['POST'])
def deletar_produto(id):
    db.child("produtos").child(id).remove()
    return redirect(url_for('lista_produtos'))

@app.route('/lista_clientes')
def lista_clientes():
    if(getSession()):
        clientes = db.child("clientes").get().val()
        if clientes is None:
            clientes = {}
        return render_template('lista_clientes.html', clientes=clientes)
    else:
        return redirect(url_for('login'))

# Rota para cadastrar cliente
@app.route('/cadastrar_cliente', methods=['POST'])
def cadastrar_cliente():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    genero_str = request.form['genero']  # Obtém o valor do dropdown como string
    genero_bool = genero_str == 'true'   # Converte para booleano
    estadoCivil = request.form['estadoCivil']
    idade = request.form['idade']
    cpf = request.form['cpf']
    
    cliente = {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'endereco': endereco,
        'genero': genero_bool,  # Armazena o booleano no banco de dados
        'estadoCivil': estadoCivil,
        'idade': idade,
        'cpf': cpf 
    }
    
    db.child("clientes").push(cliente)
    return redirect(url_for('lista_clientes'))


@app.route('/editar_cliente/<id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        genero_str = request.form['genero']  # Obtém o valor do dropdown como string
        genero_bool = genero_str == 'true'   # Converte para booleano
        estadoCivil = request.form['estadoCivil']
        idade = request.form['idade']
        cpf = request.form['cpf']
        
        db.child("clientes").child(id).update({
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "endereco": endereco,
            "genero": genero_bool,  # Armazena o booleano no banco de dados
            "estadoCivil": estadoCivil, 
            "idade": idade,
            'cpf': cpf
        })
        
        return redirect(url_for('lista_clientes'))
    else:
        cliente = db.child("clientes").child(id).get().val()
        # Verifica se o cliente existe antes de tentar acessar seus dados
        if cliente:
            return render_template('editar_cliente.html', cliente=cliente)
        else:
            flash('Cliente não encontrado.', 'error')
            return redirect(url_for('lista_clientes'))

# Rota para deletar cliente
@app.route('/deletar_cliente/<id>', methods=['POST'])
def deletar_cliente(id):
    db.child("clientes").child(id).remove()
    return redirect(url_for('lista_clientes'))


# Rota para cadastrar uma nova unidade
@app.route('/cadastrar_unidade', methods=['POST'])
def cadastrar_unidade():
    if request.method == 'POST':
        nome = request.form['nome']
        localizacao = request.form['localizacao']
        telefone = request.form['telefone']
        unidade = {"nome": nome, "localizacao": localizacao}
        db.child("unidades").push(unidade)
        return redirect(url_for('lista_unidades'))
    else:
        return render_template('lista_unidades.html', unidades=unidades)

# Rota de edição de unidade
@app.route('/editar_unidade/<id>', methods=['GET', 'POST'])
def editar_unidade(id):
    if request.method == 'POST':
        nome = request.form['nome']
        localizacao = request.form['localizacao']
        telefone = request.form['telefone']
        db.child("unidades").child(id).update({
            "nome": nome, 
            "localizacao": localizacao,
            "telefone": telefone})
        return redirect(url_for('lista_unidades'))
    else:
        unidade = db.child("unidades").child(id).get().val()
        return render_template('editar_unidade.html', unidade=unidade)

# Rota de listagem de unidades
@app.route('/lista_unidades')
def lista_unidades():
    if(getSession()):
        unidades = db.child("unidades").get().val()
        if unidades is None:
            unidades = {}
        return render_template('lista_unidades.html', unidades=unidades)
    else:
        return redirect(url_for('login'))

# Rota de deleção de unidade
@app.route('/deletar_unidade/<id>', methods=['POST'])
def deletar_unidade(id):
    db.child("unidades").child(id).remove()
    return redirect(url_for('lista_unidades'))


@app.route('/lista_vendas')
def lista_vendas():
    if(getSession()):
        # Obter as vendas do banco de dados Firebase ou inicializar uma lista vazia
        vendas = db.child("vendas").get().val() or {}

        # Obter os produtos do banco de dados Firebase
        produtos = db.child("produtos").get().val()

        # Calcular o total de cada venda
        for venda_id, venda in vendas.items():
            produto_id = venda['produto_id']
            quantidade = venda['quantidade']
            preco = produtos[produto_id]['preco']
            total = float(preco) * float(quantidade)
            venda['totpedido'] = format(total, '.2f')

        clientes = db.child("clientes").get().val()
        return render_template('lista_vendas.html', vendas=vendas, clientes=clientes, produtos=produtos)
    else:
        return redirect(url_for('login'))
# Rota para cadastrar uma nova venda
@app.route('/cadastrar_venda', methods=['POST'])
def cadastrar_venda():
    # Obter as vendas do banco de dados Firebase ou inicializar uma lista vazia
    vendas = db.child("vendas").get().val() or {}

    # Obter os produtos do banco de dados Firebase
    produtos = db.child("produtos").get().val()
    
    cliente_id = request.form['cliente']
    produto_id = request.form['produto']
    quantidade = int(request.form['quantidade'])
    data = request.form['data']
    
    produto = produtos[produto_id]
    totpedido = produto['preco'] * quantidade
    email = auth.get_account_info(session['user'])['users'][0]['email']
    usuarios = db.child("users").get().val()
    try:
        for key, usuario in usuarios.items():
            if usuario['email'] == email:
                nomeUser = usuario['name']
    except:
        nomeUser = ""
    # Gerar um ID para a nova venda
    venda_id = len(vendas) + 1

    # Adicionar a nova venda à lista de vendas
    nova_venda = {
        "cliente": cliente_id,
        "data": data,
        "produto_id": produto_id,
        "quantidade": quantidade,
        "totpedido": totpedido,
        "emailUser": email,
        "nomeUser": nomeUser
    }

    vendas[f"-NyqERd{venda_id:03d}"] = nova_venda

    # Atualizar os dados de vendas no banco de dados Firebase
    db.child("vendas").set(vendas)

    # Adicionar o total do pedido ao banco de dados Firebase
    db.child("vendas").child(f"-NyqERd{venda_id:03d}").update({"totpedido": totpedido})

    return redirect(url_for('lista_vendas'))

@app.route('/editar_venda/<id>', methods=['POST'])
def editar_venda(id):
    # Obter os produtos do banco de dados Firebase
    produtos = db.child("produtos").get().val()
    
    # Obter a venda específica que está sendo editada
    venda = db.child("vendas").child(id).get().val()
    
    if venda:
        cliente_id = request.form['cliente']
        produto_id = request.form['produto']
        quantidade = int(request.form['quantidade'])
        data = request.form['data']

        # Certifique-se de que o produto existe antes de acessar suas informações
        if produto_id in produtos:
            produto = produtos[produto_id]
            totpedido = produto['preco'] * quantidade

            updated_venda = {
                "cliente": cliente_id,
                "data": data,
                "produto_id": produto_id,
                "quantidade": quantidade,
                "totpedido": totpedido
            }

            db.child("vendas").child(id).update(updated_venda)

    return redirect(url_for('lista_vendas'))

@app.route('/deletar_venda/<id>', methods=['POST'])
def deletar_venda(id):
    if(getSession()):
        # Obter as vendas do banco de dados Firebase
        vendas = db.child("vendas").get().val() or {}
        
        if id in vendas:
            del vendas[id]
            # Atualizar os dados de vendas no banco de dados Firebase
            db.child("vendas").set(vendas)
        
        return redirect(url_for('lista_vendas'))
    else:
        return redirect(url_for('login'))


# # Exemplo de dados para o gráfico de vendas ao longo do tempo
# dados_grafico_vendas = {
#     'data': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
#     'quantidade': [100, 120, 90, 150, 200, 180]
# }

# Função para calcular o faturamento total ao longo do tempo
def calcular_faturamento_tempo():
    vendas = db.child("vendas").get().val() or {}
    produtos = db.child("produtos").get().val()
    
    data = []
    faturamento_total = []
    
    for venda_id, venda in vendas.items():
        data.append(venda['data'])
        produto_id = venda['produto_id']
        quantidade = venda['quantidade']
        preco = produtos[produto_id]['preco']
        total = float(preco) * float(quantidade)
        
        if not faturamento_total:
            faturamento_total.append(total)
        else:
            faturamento_total.append(total + faturamento_total[-1])
    
    return data, faturamento_total

# Rota para fornecer o relatório de faturamento ao longo do tempo via API
@app.route('/api/relatorio_faturamento_tempo', methods=['GET'])
def api_relatorio_faturamento_tempo():
    data, faturamento_total = calcular_faturamento_tempo()
    relatorio = {'data': data, 'faturamento_total': faturamento_total}
    return jsonify(relatorio)

# Rota para renderizar o dashboard de faturamento
@app.route('/dashboard_faturamento')
def dashboard_faturamento():
    return render_template('grafico_vendas.html')

if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)
