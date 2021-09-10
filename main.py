from flask import Flask, request, render_template, escape, redirect, url_for, send_from_directory, flash
import os


# import my_data or my_data_safe
import my_data_safe as data


app = Flask(__name__)
app.secret_key = "my_secret_key"


# Main Route
@app.route('/')
def main():
    return redirect(url_for('login'))


# Login Route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'login' in request.form:
        username = (request.form['username'])
        password = (request.form['password'])
        if data.login_checker(username, password):
            return render_template('index.html', name=escape(username), passw=escape(password))
        else:
            flash("Login failed!")
            return redirect(url_for('login'))
    elif 'register_instead' in request.form:
        return redirect(url_for('register'))
    elif 'truncate_users_table' in request.form:
        data.truncate_users_table()
        flash("Table truncated!")
        return redirect(url_for('login'))
    else:
        return render_template('login.html')


# Register Route
@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'register' in request.form:
        username = (request.form['username'])
        password = (request.form['password'])
        if data.register_checker(username, password):
            flash("Register succesful!")
            return redirect(url_for('login'))
        else:
            flash("Register failed!")
            return redirect(url_for('register'))
    elif 'login_instead' in request.form:
        return redirect(url_for('login'))
    elif 'truncate_users_table' in request.form:
        data.truncate_users_table()
        flash("Table truncated!")
        return redirect(url_for('register'))
    else:
        return render_template('register.html')


# Route to favicon
@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'img'),'favicon.ico')
