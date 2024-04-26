import mysql.connector
from conection_File import conexao
from flask import *
from tkinter import *

class cliente:
    def listar_clientes():
        conn = conexao.conection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cliente")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return render_template('lista_clientes.html', clientes=rows)

    def cadastrar_cliente():
        
        if request.method == 'POST':
            conn = conexao.conection()
            cursor = conn.cursor()

            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']
            genero = request.form['genero']
            cep = request.form['cep']
            endereco = request.form['endereco']
            estado_civil = request.form['estado_civil']
            idade = request.form['idade']
            unidadeCliente_id = request.form['unidade']

            sql = "INSERT INTO cliente (nome, email, telefone, genero, cep, endereco, estado_civil, idade, unidadeCliente_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, email, telefone, genero, cep, endereco, estado_civil, idade, unidadeCliente_id))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return cliente.listar_clientes()
        elif request.method == 'GET':
            conn = conexao.conection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM unidade")
            rows = cursor.fetchall()

            cursor.close()
            conn.close()
            return render_template('cadastrar_cliente.html', unidades=rows)


    def editar_cliente(cliente_id):
        conn = conexao.conection()
        cursor = conn.cursor()
        if request.method == 'POST':
            # Obter os dados do formulário

            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']
            cep = request.form['cep']
            endereco = request.form['endereco']
            genero = request.form['genero']
            estado_civil = request.form['estado_civil']
            idade = request.form['idade']

            # Atualizar os dados do cliente no banco de dados
            sql = "UPDATE cliente SET nome = %s, email = %s, telefone = %s, genero = %s, cep = %s,endereco = %s,estado_civil = %s, idade= %s  WHERE id = %s"
            cursor.execute(sql, (nome, email, telefone, genero, cep, endereco, estado_civil, idade, cliente_id))
            conn.commit()

            return cliente.listar_clientes()

        # Se for uma requisição GET, exibir o formulário de edição
        sql = "SELECT * FROM cliente WHERE id = %s"
        cursor.execute(sql, (cliente_id,))
        clienteEdit = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('editar_cliente.html', cliente=clienteEdit)

    def excluir_cliente(cliente_id):
        # Excluir o cliente do banco de dados
        conn = conexao.conection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE id = %s", (cliente_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return cliente.listar_clientes()