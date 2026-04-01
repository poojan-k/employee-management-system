from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pooja@2003",
    database="employee_db"
)

cursor = db.cursor()

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid username or password"

    return render_template('login.html')


# 🔓 LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# 🏠 HOME + SEARCH
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        search = request.form['search']
        cursor.execute(
            "SELECT * FROM employees WHERE name LIKE %s",
            ('%' + search + '%',)
        )
    else:
        cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()
    return render_template('index.html', employees=employees)


# ➕ ADD EMPLOYEE
@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session:
        return redirect('/login')

    name = request.form['name']
    role = request.form['role']
    salary = request.form['salary']

    cursor.execute(
        "INSERT INTO employees (name, role, salary) VALUES (%s, %s, %s)",
        (name, role, salary)
    )
    db.commit()
    return redirect('/')


# ❌ DELETE
@app.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    db.commit()
    return redirect('/')


# ✏️ EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        salary = request.form['salary']

        cursor.execute(
            "UPDATE employees SET name=%s, role=%s, salary=%s WHERE id=%s",
            (name, role, salary, id)
        )
        db.commit()
        return redirect('/')

    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    emp = cursor.fetchone()
    return render_template('edit.html', emp=emp)


if __name__ == '__main__':
    app.run(debug=True)