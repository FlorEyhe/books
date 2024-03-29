from flask import Flask, g, jsonify
import psycopg2

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = psycopg2.connect(
                                user="postgres",
                                password="PIKqPhxx35Ymhm3MIgdR",
                                host="containers-us-west-17.railway.app",
                                port="5679",
                                database="railway"
                                )
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Ruta para la página de inicio
@app.route('/', methods=['GET'])
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books_table")
    totalRows = cursor.fetchall()

    num_libros = len(totalRows)

    cursor.close()

    home_display = f"""
    <h1>API Libros</h1>
    <p>Esta es una API que contiene {num_libros} libros.</p>"""

    return home_display


# 1.Ruta para obtener todos los libros
@app.route('/books', methods=['GET  '])
def get_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books_table")
    books = cursor.fetchall()

    cursor.close()

    return jsonify(books)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)