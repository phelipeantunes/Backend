from flask import Flask, request
from flask_cors import CORS
import psycopg2
import json
import datetime


app = Flask(__name__)

CORS(app)

def postgres_connection():
    # Connection details
    hostname = 'postgres'
    database = 'postgres'
    username = 'postgres'
    password = 'pish1234'

    try:
        # Establish a connection
        connection = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password
        )

        # Create a cursor
        return connection

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/get/<entity>',methods=['GET'])
def get(entity):
    connection = postgres_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "quizz-project".' + entity)
    
    # Fetch the results
    rows = cursor.fetchall()

    # Get the column names
    columns = [desc[0] for desc in cursor.description]

    # Convert rows to a list of dictionaries
    results = []
    for row in rows:
        result_dict = {}
        for i, value in enumerate(row):
            if isinstance(value, datetime.datetime):
                value = value.isoformat()  # Converter o datetime em string
            result_dict[columns[i]] = value
        results.append(result_dict)

    # Convert results to JSON
    json_data = json.dumps(results)

    # Print JSON data
    print(json_data)


    # Close the cursor and connection
    cursor.close()
    connection.close()
    return json_data

@app.route('/create/<entity>',methods=['POST'])
def create(entity):
    data = json.loads(request.get_data())
    connection = postgres_connection()
    cursor = connection.cursor()
       
    if isinstance(data, list):
        for item in data:
            columns = list(item.keys())
            values = list(item.values())

            # Construct the SQL query
            insert_query = 'INSERT INTO "quizz-project".'+ entity + '({}) VALUES ({}) RETURNING id'.format(
                ", ".join(columns),
                ", ".join(['%s'] * len(columns))
            )
            cursor.execute(insert_query, values)
            
            # Recuperar o novo ID gerado
            
            item['id'] = cursor.fetchone()[0]
    else:
        columns = list(data.keys())
        values = list(data.values())

            # Construct the SQL query
        insert_query = 'INSERT INTO "quizz-project".'+ entity + '({}) VALUES ({}) RETURNING id'.format(
            ", ".join(columns),
            ", ".join(['%s'] * len(columns))
        )
        cursor.execute(insert_query, values)
        # Recuperar o novo ID gerado
        
        data['id'] = cursor.fetchone()[0]
    
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    
    return data

@app.route('/delete/<entity>/<fk>',methods=['DELETE'])
@app.route('/delete/<entity>',methods=['DELETE'])
def delete(entity, fk = 'id'):
    data = json.loads(request.get_data())
    connection = postgres_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM "quizz-project".' + entity + ' WHERE ' + fk + ' = ' + "'" + str(data[fk]) + "'")
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return data

@app.route('/edit/<entity>',methods=['PUT'])
def edit(entity):
    data = json.loads(request.get_data())
    connection = postgres_connection()
    cursor = connection.cursor()
    
    columns = list(data.keys())
    values = list(data.values())    
    update_query = 'UPDATE "quizz-project".' + entity + " SET {} ".format(
        ", ".join(["{}=%s".format(column) for column in columns]) + " WHERE id = '" + str(data['id']) + "'"
    )
    
    cursor.execute(update_query, values)
        
    connection.commit()
    
    cursor.close()
    connection.close()
    return data

@app.route('/getResult/<quiz_id>',methods=['GET'])
def getResult(quiz_id):
    connection = postgres_connection()
    cursor = connection.cursor()
    cursor.execute(f"""select id_dispositivo ,nome_dispositivo , count(id_dispositivo) as pontuacao from (
        select  t.id_dispositivo, d.nome_dispositivo , p.id, t.resposta_tentativa ,p.opcao_correta from "quizz-project".tentativas t 
        inner join "quizz-project".perguntas p 
        on p.id =t.id_pergunta 
        inner join (
        select id_dispositivo,id_pergunta , max(created_at) as last_try from  "quizz-project".tentativas t 
        where t.id_quiz = {quiz_id}
        group by id_dispositivo,id_pergunta 
        ) rm_duplicate
        on rm_duplicate.last_try = t.created_at
        inner join "quizz-project".dispositivos d 
        on t.id_dispositivo = d.id 
        where t.id_quiz = {quiz_id}
        and t.resposta_tentativa = p.opcao_correta
        ) as results
        group by id_dispositivo, nome_dispositivo 
        order by count(id_dispositivo) desc
        """
    )
    # Fetch the results
    rows = cursor.fetchall()

    # Get the column names
    columns = [desc[0] for desc in cursor.description]

    # Convert rows to a list of dictionaries
    results = []
    for row in rows:
        result_dict = {}
        for i, value in enumerate(row):
            if isinstance(value, datetime.datetime):
                value = value.isoformat()  # Converter o datetime em string
            result_dict[columns[i]] = value
        results.append(result_dict)

    # Convert results to JSON
    json_data = json.dumps(results)

    # Print JSON data
    print(json_data)


    # Close the cursor and connection
    cursor.close()
    connection.close()
    return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0')
