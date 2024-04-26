import mysql.connector
from conection_File import conexao
from flask import *
from tkinter import *

class unidade:
    def listar_unidades():
        conn = conexao.conection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM unidade")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return render_template('lista_unidades.html', unidades=rows)

    def cadastrar_unidade():
        if request.method == 'POST':
            conn = conexao.conection()
            cursor = conn.cursor()

            nome = request.form['nome']
            endereco = request.form['endereco']
            telefone = request.form['telefone']
            sql = "INSERT INTO unidade (nome, endereco, telefone) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, endereco, telefone))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return unidade.listar_unidades()
        return render_template('cadastrar_unidade.html')

    def editar_unidade(unidade_id):
        conn = conexao.conection()
        cursor = conn.cursor()
        if request.method == 'POST':
            # Obter os dados do formulário

            nome = request.form['nome']
            endereco = request.form['endereco']
            telefone = request.form['telefone']

            sql = "UPDATE unidade SET nome = %s, endereco = %s, telefone = %s WHERE id = %s"
            cursor.execute(sql, (nome, endereco, telefone, unidade_id))
            conn.commit()

            return unidade.listar_unidades()

        # Se for uma requisição GET, exibir o formulário de edição
        cursor.execute("SELECT * FROM unidade WHERE id = %s", (unidade_id,))        
        unidadeEdit = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('editar_unidade.html', unidade=unidadeEdit)

    def excluir_unidade(unidade_id):
        # Excluir a unidade do banco de dados
        conn = conexao.conection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cliente WHERE unidadeCliente_id =%s", (unidade_id,))
        clientes = cursor.fetchall()
        if clientes == []:
            cursor.execute("DELETE FROM unidade WHERE id = %s", (unidade_id,))
            conn.commit()   
            cursor.close()
            conn.close()
            return unidade.listar_unidades()
        else:
            cursor.close()
            conn.close()
            return unidade.listar_unidades()