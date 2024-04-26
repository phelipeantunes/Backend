import mysql.connector

# Conectando ao banco de dados
class conexao:
    def conection():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin",
                database="app_sust"
            )
            return conn
        except:
            print("Connection error")
