import flask
import json
import psycopg2
from flask_cors import CORS, cross_origin
import signal
import sys

import time




time.sleep(10)
try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="todo",
        user="user",
        password="user")
    cur = conn.cursor()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/todos/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def hello():
    return "Hello"

@app.route('/todos/user/<user_id>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_user_todos(user_id):
    postgreSQL_select_Query = "select * from todos where user_id = %s"
    try:
        cur.execute(postgreSQL_select_Query, (user_id))
        records = cur.fetchall()
        records_with_keys = []
        for record in records:
            records_with_keys.append({
                'user_id': record[0],
                'task': record[1],
                'task_id': record[2],
                'is_completed': record[3],
                'priority': record[4]
            })
        return json.dumps(records_with_keys)
    except Exception as e:
        return f"Error collecting data for {user_id}: {e}"

@app.route('/todos/create', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def create_todo():
    data = flask.request.json
    print(data)
    try:
        cur.execute("""INSERT INTO todos (user_id, task, is_completed, priority) VALUES (%(user_id)s, %(task)s, %(is_completed)s, %(priority)s) RETURNING task_id""", data)
        task_id = cur.fetchone()[0]
        conn.commit()
        return str(task_id)
    except Exception as e:
        return f"Error creating To Do: {e}"

@app.route('/todos/delete/<task_id>', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def delete_todo(task_id):
    try:
        cur.execute("DELETE FROM todos WHERE task_id = %s", (task_id,))
        conn.commit()
        return f"Successfully Deleted {task_id}"
    except Exception as e:
        return f"Error Deleting {task_id}: {e}"

@app.route('/todos/update/task/<task_id>',  methods=['POST'])
@cross_origin()
def update_todo(task_id):
    data = flask.request.json
    print(data)
    data['task_id'] = task_id
    try:
        cur.execute(f"UPDATE todos set user_id=%(user_id)s, task=%(task)s, is_completed=%(is_completed)s, priority=%(priority)s where task_id={task_id}", data)
        conn.commit()
        return f"Successfully updated record {task_id}"
    except Exception as e:
        return f"Error updating record {task_id}: {e}"

@app.route('/create_db', methods=['GET'])
@cross_origin()
def create_db():
    command = (
        """
        CREATE TABLE IF NOT EXISTS todos (
            user_id INTEGER NOT NULL,
            task TEXT,
            task_id SERIAL,
            is_completed BOOLEAN,
            priority TEXT
        )
        """
    )
    cur.execute(command)
    conn.commit()
    return f"Table Created"

@app.route('/create_fake_data', methods=['GET'])
@cross_origin()
def create_fake_data():
    try:
        cur.execute("INSERT INTO todos (user_id, task, is_completed, priority) VALUES(%s, %s, %s, %s)", (1, "Jackie", False, "HIGH"))
        conn.commit()
        return f"Successfully Inserted Fake Data"
    except Exception as e:
        return f"Error Inserting Fake data: {e}"

@app.route('/inspect', methods=['GET'])
@cross_origin()
def inspect():
    command = (
        """
        SELECT 
            table_name, 
            column_name, 
            data_type 
        FROM 
            information_schema.columns
        WHERE 
            table_name = 'todos';
        """
    )
    cur.execute(command)
    vals = cur.fetchall()
    return str(vals)

app.run()