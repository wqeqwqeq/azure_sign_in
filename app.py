from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# In-memory database to store user credentials and login info
users = {}
login_info = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            # Update login info
            if username not in login_info:
                login_info[username] = {
                    'logins': 0,
                    'last_login': None
                }
            login_info[username]['logins'] += 1
            login_info[username]['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return redirect(url_for('dashboard'))
        else:
            return "Incorrect Username or Password"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            if username in users:
                return "User already exists!"
            else:
                users[username] = {'password': password}
                return redirect(url_for('login'))
        else:
            return "Passwords do not match!"
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        user_login_info = login_info.get(username, {})
        return render_template('dashboard.html', username=username, login_info=user_login_info)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

