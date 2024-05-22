# import mysql.connector
# from clientes import cliente
# from unidades import unidade
# from produtos import produto
# from flask import *
# from tkinter import *

# app = Flask(__name__)
# app.secret_key = "super secret key"

# # Rotas de cliente, referenciam o módulo clientes.
# @app.route('/lista_clientes')
# def listar():
#     return cliente.listar_clientes()

# @app.route('/cadastrar_clientes', methods=['GET', 'POST'])
# def cadastrar_cliente():
#     return cliente.cadastrar_cliente()

# @app.route('/editar_clientes/<int:cliente_id>', methods=['GET', 'POST'])
# def editar_cliente(cliente_id):
#     return cliente.editar_cliente(cliente_id)

# @app.route('/excluir_clientes/<int:cliente_id>', methods=['GET'])
# def excluir_cliente(cliente_id):
#     return cliente.excluir_cliente(cliente_id)



# # Rotas de unidade, referenciam o módulo unidades.
# @app.route('/lista_unidades')
# def lista_unidades():
#     return unidade.listar_unidades()

# # Rota para cadastrar uma Unidade
# @app.route('/cadastrar_unidade', methods=['GET', 'POST'])
# def cadastrar_unidade():
#     return unidade.cadastrar_unidade()

# # Rota para editar uma unidade
# @app.route('/editar_unidade/<int:unidade_id>', methods=['GET', 'POST'])
# def editar_unidade(unidade_id):
#     return unidade.editar_unidade(unidade_id)

# # Rota para excluir uma unidade
# @app.route('/excluir_unidade/<int:unidade_id>', methods=['GET'])
# def excluir_unidade(unidade_id):
#     return unidade.excluir_unidade(unidade_id)




# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')



# # Rota para cadastrar venda
# @app.route('/cadastrar_venda', methods=['GET', 'POST'])
# def cadastrar_venda():
#     if request.method == 'POST':
#         produto_id = request.form['produto_id']
#         cliente_id = request.form['cliente_id']
#         quantidade = request.form['quantidade']
#         total = request.form['total']

#         # Insira aqui o código para inserir a venda no banco de dados

#         return redirect(url_for('lista_clientes'))

#     # Consulta para obter a lista de produtos
#     cursor.execute("SELECT id, nome FROM produtos")
#     produtos = cursor.fetchall()

#     # Consulta para obter a lista de clientes
#     cursor.execute("SELECT id, nome FROM cliente")
#     clientes = cursor.fetchall()

#     return render_template('cadastrar_venda.html', produtos=produtos, clientes=clientes)

# # Página para editar uma venda
# @app.route('/editar_venda/<int:venda_id>', methods=['GET', 'POST'])
# def editar_venda(venda_id):
#     if request.method == 'POST':
#         produto_id = request.form['produto_id']
#         cliente_id = request.form['cliente_id']
#         quantidade = request.form['quantidade']
#         total = request.form['total']

#         cursor.execute("UPDATE vendas SET produto_id=%s, cliente_id=%s, quantidade=%s, total=%s WHERE id=%s",
#                        (produto_id, cliente_id, quantidade, total, venda_id))
#         conn.commit()

#         return redirect(url_for('listar_vendas'))

#     cursor.execute("SELECT * FROM vendas WHERE id=%s", (venda_id,))
#     venda = cursor.fetchone()
#     cursor.execute("SELECT id, nome FROM produtos")
#     produtos = cursor.fetchall()
#     cursor.execute("SELECT id, nome FROM cliente")
#     clientes = cursor.fetchall()

#     return render_template('editar_venda.html', venda=venda, produtos=produtos, clientes=clientes)

# # Rota para excluir uma venda
# @app.route('/excluir_venda/<int:venda_id>', methods=['GET'])
# def excluir_venda(venda_id):
#     cursor.execute("DELETE FROM vendas WHERE id=%s", (venda_id,))
#     conn.commit()
#     return redirect(url_for('listar_vendas'))

# # Página para listar todas as vendas
# @app.route('/lista_vendas')
# def listar_vendas():
#     cursor.execute("SELECT * FROM vendas")
#     vendas = cursor.fetchall()
#     return render_template('lista_vendas.html', vendas=vendas)

# # Página inicial - Lista de produtos
# @app.route('/lista_produtos')
# def lista_produtos():
#     return produto.listar_produtos()

# # Rota para cadastrar um novo produto
# @app.route('/cadastrar_produto', methods=['GET', 'POST'])
# def cadastrar_produto():
#     return produto.cadastrar_produto()

# # Rota para editar um produto
# @app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
# def editar_produto(id):
#     return produto.editar_produto(id)

# # Rota para excluir um produto
# @app.route('/excluir_produto/<int:id>', methods=['GET'])
# def excluir_produto(id):
#     return produto.excluir_produto(id)


# if __name__ == '__main__':
#     app.run(debug=True)


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "16C0z2ITZdZOAW5Ofs2CncP4NbrJenCqvBCqXDigKSmI"
SAMPLE_RANGE_NAME = "Pagina1!A1:B5"


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "secrete2.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

#   try:
#     service = build("sheets", "v4", credentials=creds)

#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result = (
#         sheet.values()
#         .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
#         .execute()
#     )
#     values = result.get("values", [])

#     if not values:
#       print("No data found.")
#       return

#     print("Name, Major:")
#     for row in values:
#       # Print columns A and E, which correspond to indices 0 and 4.
#       print(f"{row[0]}, {row[4]}")
#   except HttpError as err:
#     print(err)


if __name__ == "__main__":
  main()