from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask_app.models.user import User

# -------------------------------------------------------------------------------------------------
# HOME ROUTE
# -------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------------------------------------------------------------------------------
# ABOUT ROUTE
# -------------------------------------------------------------------------------------------------
@app.route('/about')
def about():
    return render_template('about.html')

# -------------------------------------------------------------------------------------------------
# SET ALERT ROUTE
# -------------------------------------------------------------------------------------------------
@app.route('/set/alert', methods = ['POST'])
def set_alert():
    User.set_alert(request.form)
    return redirect('/dashboard')

# -------------------------------------------------------------------------------------------------
# DASHBOARD ROUTE
# -------------------------------------------------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': session['user_id']}
    user = User.get_one(data)
    return render_template('dashboard.html', user = user)

# -------------------------------------------------------------------------------------------------
# REGISTER ROUTES
# -------------------------------------------------------------------------------------------------
@app.route('/register')
def render_register():
    return render_template('register.html')                                        # RENDER REGISTRATION PAGE

@app.route('/register/user', methods = ['POST'])
def register_user():
    print(request.form)
    data = {'email':request.form['email']}
    user_in_db = User.get_one_with_email(data)
    if user_in_db:
        flash("Email already in use.")
        return redirect('/')
    if not User.validate_user(request.form):                                # VALIDATE USERS INPUTS
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])     # HASH PW WITH BCRYPT
    print(hashed_pw)
    data = {                                                                # MAKE SURE DATA MATCHES COLUMN NAMES
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    print(data)
    user_id = User.save(data)                                               # SAVE USER INTO DB
    session['user_id'] = user_id                                            # LOG USER IN VIA SESSION
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')

# # -------------------------------------------------------------------------------------------------
# # LOGIN ROUTES
# # -------------------------------------------------------------------------------------------------
@app.route('/login')
def render_login():
    return render_template('login.html')                                           # RENDER LOGIN PAGE

@app.route('/login/user', methods = ['POST'])
def login_user():
    data = {'email': request.form['log_email']}                             # VERIFY EMAIL INPUT
    user_in_db = User.get_one_with_email(data)                              # INVALID? FLASH MESSAGE
    if not user_in_db:
        flash("Invalid credentials.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash("Invalid credentials.")                                       # VERIFY PW INPUT
        return redirect('/')                                           # INVALID? FLASH MESSAGE
    session['user_id'] = user_in_db.id                                      # LOG USER IN VIA SESSION
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')                                           # REDIRECT USER TO DASHBOARD

# @app.route('/dashboard')
# def login_redirect():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {'id': session['user_id']}
#     user = User.get_one(data)
#     return render_template('dashboard.html', user = user)

# ! LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# # -------------------------------------------------------------------------------------------------
# # UPDATE AND DELETE ROUTES
# # -------------------------------------------------------------------------------------------------
# ! UPDATE
@app.route('/update/user', methods = ['POST'])
def update_user():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/dashboard')
    User.edit_user(request.form)
    return redirect("/dashboard")

# ! DELETE
@app.route('/delete/<int:id>')
def delete_user(id):
    User.delete_user({'id': id})
    return redirect('/')

# # -------------------------------------------------------------------------------------------------
# # DISPLAY ALERTS
# # -------------------------------------------------------------------------------------------------
# # ! READ ONE
# @app.route('/subscribed/magazines')
# def show_subscribes():
#     data = {'id': session['user_id']}
#     user = User.magazines_subscribed(data)
#     this_user_subscribed = []
#     for magazine in user.magazines_subscribed:
#         this_user_subscribed.append(magazine.name)
#     print(this_user_subscribed)
#     return render_template('subscribes.html', user = user, this_user_subscribed = this_user_subscribed)