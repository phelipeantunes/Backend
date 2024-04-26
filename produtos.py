import mysql.connector
from conection_File import conexao
from flask import *
from tkinter import *

class produto:
    def listar_produtos():
        conn = conexao.conection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produto")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return render_template('lista_produtos.html', produtos=rows)

    def cadastrar_produto():
        if request.method == 'POST':
            conn = conexao.conection()
            cursor = conn.cursor()

            nome = request.form['nome']
            descricao = request.form['descricao']
            preco = request.form['preco']
            unidadeProduto_id = request.form['unidade']


            sql = "INSERT INTO produto (nome, descricao, preco, unidadeProduto_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, descricao, preco, unidadeProduto_id))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return produto.listar_produtos()
        elif request.method == 'GET':
            conn = conexao.conection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM unidade")
            rows = cursor.fetchall()

            cursor.close()
            conn.close()
            return render_template('cadastrar_produto.html', unidades=rows)

    def editar_produto(produto_id):
        conn = conexao.conection()
        cursor = conn.cursor()
        if request.method == 'POST':
            nome = request.form['nome']
            descricao = request.form['descricao']
            preco = request.form['preco']

            sql = "UPDATE produto SET nome = %s, descricao = %s, preco = %s WHERE id = %s"
            cursor.execute(sql, (nome, descricao, preco, produto_id))
            conn.commit()

            cursor.close()
            conn.close()
            return produto.listar_produtos()
        cursor.execute("SELECT * FROM produto WHERE id = %s", (produto_id,))
        produtoEdit = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('editar_produto.html', produto=produtoEdit)

    def excluir_produto(produto_id):
        conn = conexao.conection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produto WHERE id = %s", (produto_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return produto.listar_produtos()