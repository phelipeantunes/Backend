from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

app = Flask(__name__)

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

# Rota inicial
@app.route('/')
def index():
    if 'user' in session:
        # Obter a lista de usuários do Firebase
        usuarios = db.child("users").get().val()
        return render_template('index.html', usuarios=usuarios)
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
        email = request.form['email']
        password = request.form['password']

        # Verifica se o email já está cadastrado
        users = db.child("users").order_by_child("email").equal_to(email).get()
        if users.each():
            error = 'Email já está em uso. Por favor, use outro email.'
            return render_template('register.html', error=error)

        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('login'))
        except:
            error = 'Erro ao registrar. Por favor, tente novamente.'
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')

# Rota de cadastro de produto
@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        categoria = request.form['categoria']
        unidadeProduto = request.form['unidadeProduto']

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
        return render_template('cadastrar_produto.html')


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
        return render_template('editar_produto.html', produto=produto)



# Rota de listagem de produtos
@app.route('/lista_produtos')
def lista_produtos():
    produtos = db.child("produtos").get().val()
    return render_template('lista_produtos.html', produtos=produtos)





# Rota de deleção de produto
@app.route('/deletar_produto/<id>', methods=['POST'])
def deletar_produto(id):
    db.child("produtos").child(id).remove()
    return redirect(url_for('lista_produtos'))

@app.route('/lista_clientes')
def lista_clientes():
    clientes = db.child("clientes").get().val()
    if clientes is None:
        clientes = {}
    return render_template('lista_clientes.html', clientes=clientes)

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
    
    cliente = {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'endereco': endereco,
        'genero': genero_bool,  # Armazena o booleano no banco de dados
        'estadoCivil': estadoCivil,
        'idade': idade 
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
        
        db.child("clientes").child(id).update({
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "endereco": endereco,
            "genero": genero_bool,  # Armazena o booleano no banco de dados
            "estadoCivil": estadoCivil, 
            "idade": idade 
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
        db.child("unidades").child(id).update({"nome": nome, "localizacao": localizacao})
        return redirect(url_for('lista_unidades'))
    else:
        unidade = db.child("unidades").child(id).get().val()
        return render_template('editar_unidade.html', unidade=unidade)

# Rota de listagem de unidades
@app.route('/lista_unidades')
def lista_unidades():
    unidades = db.child("unidades").get().val()
    if unidades is None:
        unidades = {}
    return render_template('lista_unidades.html', unidades=unidades)

# Rota de deleção de unidade
@app.route('/deletar_unidade/<id>', methods=['POST'])
def deletar_unidade(id):
    db.child("unidades").child(id).remove()
    return redirect(url_for('lista_unidades'))


# Rota de listagem de vendas
@app.route('/lista_vendas')
def lista_vendas():
    vendas = db.child("vendas").get().val()
    if vendas is None:
        vendas = {}  # Se não houver vendas, inicializa como um dicionário vazio
    return render_template('lista_vendas.html', vendas=vendas)

# Rota de cadastro de venda
@app.route('/cadastrar_venda', methods=['GET', 'POST'])
def cadastrar_venda():
    if request.method == 'POST':
        cliente = request.form['cliente']
        produto = request.form['produto']
        quantidade = request.form['quantidade']
        data = request.form['data']  # Adicione isso se houver um campo de data no formulário

        venda = {"cliente": cliente, "produto": produto, "quantidade": quantidade, "data": data}  # Adicione "data" ao dicionário
        db.child("vendas").push(venda)
        return redirect(url_for('lista_vendas'))
    else:
        return render_template('cadastrar_venda.html')

# Rota de edição de venda
@app.route('/editar_venda/<id>', methods=['GET', 'POST'])
def editar_venda(id):
    if request.method == 'POST':
        cliente = request.form['cliente']
        produto = request.form['produto']
        quantidade = request.form['quantidade']
        data = request.form['data']

        venda = {"cliente": cliente, "produto": produto, "quantidade": quantidade, "data": data}
        db.child("vendas").child(id).update(venda)
        return redirect(url_for('lista_vendas'))
    else:
        venda = db.child("vendas").child(id).get().val()
        return render_template('editar_venda.html', venda=venda)

# Rota de deleção de venda
@app.route('/deletar_venda/<id>', methods=['POST'])
def deletar_venda(id):
    db.child("vendas").child(id).remove()
    return redirect(url_for('lista_vendas'))


if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)
