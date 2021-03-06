from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, food

# put in routes
@app.route('/')
def index():
    return render_template('index.html')

#Create 
@app.route('/register/user', methods = ['POST'])
def register():
    if user.User.create_user(request.form):
        return redirect('/user/profile')
    return redirect('/')

#Read 
@app.route('/user/profile')
def view_profile():
    if 'user_id' not in session:
        return render_template('index.html')
    this_user = user.User.get_user_by_id(session['user_id'])
    all_foods = food.Food.view_all_foods()
    return render_template('profile.html', this_user = this_user, all_foods = all_foods)

@app.route('/login', methods = ['POST'])
def login_user():
    if user.User.login(request.form):
        return redirect('/user/profile')
    return redirect('/')

#Update 


#Delete 
@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')