from flask import Flask, request, render_template_string
import mysql.connector
import os

app = Flask(__name__)

HTML = '''
    <h1>Mesaje</h1>
    <form method="POST">
        <input name="message" placeholder="Scrie un mesaj" required>
        <input type="submit">
    </form>
    <ul>
        {% for msg in messages %}
            <li>{{ msg[1] }}</li>
        {% endfor %}
    </ul>
'''

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('MYSQL_USER', 'user'),
        password=os.environ.get('MYSQL_PASSWORD', 'password'),
        database=os.environ.get('MYSQL_DATABASE', 'myapp')
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        msg = request.form['message']
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (msg,))
        conn.commit()
    cur.execute("SELECT * FROM messages")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(HTML, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
