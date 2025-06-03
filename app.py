from flask import Flask, render_template, request, redirect, url_for, session, abort, get_flashed_messages
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
import bcrypt
import os
from flask import flash


app = Flask(__name__)
app.secret_key = "your-secret-key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'car3'
mysql = MySQL(app)

@app.route('/home')
def home():
    purchase_status = request.args.get('purchase')
    return render_template('home.html', purchase_status=purchase_status)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from ecom where username = '{username}'")
        user = cur.fetchone()
        cur.close()

        if user and pwd == user[1]:
                session['username'] = user[0]
                return redirect(url_for('home'))
        else:
             return render_template('login.html', error='Invalid username or password')
    return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ecom (username, password) VALUES (%s, %s)", (username, pwd))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/car<int:car_id>')
def car_page(car_id):
    if 1 <= car_id <= 16:
        template_name = f"car{car_id}.html"
        if os.path.exists(os.path.join('templates', template_name)):
            return render_template(template_name)
        else:
            abort(404)
    else:
        return "Car not found", 404

@app.route('/purchase1')
def purchase1():
    return render_template('purchase1.html')

@app.route('/purchase2')
def purchase2():
    return render_template('purchase2.html')

@app.route('/purchase3')
def purchase3():
    return render_template('purchase3.html')

@app.route('/purchase4')
def purchase4():
    return render_template('purchase4.html')

@app.route('/purchase5')
def purchase5():
    return render_template('purchase5.html')


@app.route('/balance1', methods=['GET', 'POST'])
def balance1():
    if request.method == 'POST':
        selected_method = request.form.get('payment_method')
        balances = {
            "paypal": 0,
            "google_pay": 1_200_000,
            "credit_card": 0,
        }
        if selected_method not in balances:
            return render_template('balance1.html', message="Please select a payment method.")
        elif balances[selected_method] <= 0:
            return render_template('balance1.html', message="You don't have enough money.")
        else:
            flash("Successfully purchased!") 
            return redirect(url_for('home'))  
    return render_template('balance1.html')


@app.route('/balance2', methods=['GET', 'POST'])
def balance2():
    message = None
    if request.method == 'POST':
        selected_method = request.form.get('payment_method')
        balances = {
            "paypal": 0,
            "google_pay": 0,
            "apple_pay": 0,
        }
        if selected_method not in balances:
            message = "Please select a payment method."
        elif balances[selected_method] <= 0:
            message = "You don't have enough money to purchase this."

    return render_template('balance2.html', message=message)

@app.route('/balance3')
def balance3():
    return render_template('balance3.html')

@app.route('/setting1')
def setting1():
    return render_template('setting1.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/yourpin')
def yourpin():
    return render_template('yourpin.html')

@app.route('/password')
def password():
    return render_template('password.html')

@app.route('/profil1')
def profil1():
    return render_template('profil1.html')

@app.route('/location')
def location():
    return render_template('location.html')
if __name__ == '__main__':
    with app.app_context():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT 1")
            print("✅ MySQL connection successful.")
        except Exception as e:
            print(f"❌ MySQL connection failed: {e}")

    app.run(debug=True)
