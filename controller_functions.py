from flask import Flask, render_template, redirect, flash, request, session
from config import app, db, func, IntegrityError, bcrypt, re
from models import User, Quote, Like

def home():
    return render_template("login.html")

def register():
    validation_check = User.validate_user(request.form)
    if "_flashes" in session.keys() or not validation_check:
        flash("Registration unsuccessful. Please Try Again!")
        return redirect("/")
    else:
        try:
            new_user = User.add_new_user(request.form)
            return redirect("/")
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. This email already exists! Please Try Again!")
            return redirect("/")

def login():
    login_user = User.query.filter_by(email = request.form["email"]).all()

    if login_user:
        session["login_id"] = login_user[0].id
        session["first_name"] = login_user[0].first_name
        session["last_name"] = login_user[0].last_name
        session["email"] = login_user[0].email
        hashed_password = login_user[0].password
        if bcrypt.check_password_hash(hashed_password, request.form["password"]):
            session["logged_in"] = True
            session["user_id"] = login_user[0].id
            flash("You are logged in!")
            return redirect("/dashboard")
        else:
            session["logged_in"] = False
            flash("You could not be logged in. Try again or register")
        return redirect("/")
    else:
        flash("Email was not found. Please try again.")
        return redirect("/")
    return redirect("/")

def dashboard():
    try:
        login_name = session["first_name"]
    except:
        flash("Please login or register to continue.")
        return redirect("/")

    first_name = session["first_name"]
    last_name = session["last_name"]
    login_id = session["user_id"]
    all_quotes = db.session.query(Quote, User).filter(Quote.user_id == User.id).all()
    count_likes = Like.query.all()
    return render_template("dashboard.html", login_name = login_name, login_id = login_id, all_quotes = all_quotes, first_name = first_name, last_name = last_name, count_likes = count_likes)

def view_edit_account(id):
    login_id = session["login_id"]
    user_instance_to_update = User.query.get(request.form["login_id"])
    first_name = user_instance_to_update.first_name
    last_name = user_instance_to_update.last_name
    email = user_instance_to_update.email
    return render_template("editaccount.html", first_name = first_name, last_name = last_name, email = email, login_id = login_id)

def update_account():
    user_instance_to_update = User.query.get(request.form["login_id"])
    first_name = user_instance_to_update.first_name
    last_name = user_instance_to_update.last_name
    email = user_instance_to_update.email

    validation_check = User.validate_edit_user(request.form)
    if "_flashes" in session.keys() or not validation_check:
        flash("Updating unsuccessful because email account already exists! Please Try Again!")
        return render_template("editaccount.html", first_name = first_name, last_name = last_name, email = email)
    else:
        try:
            edit_user = User.edit_user(request.form)
            return redirect("/dashboard")
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. This email already exists! Please try a different email address!")
            return render_template("editaccount.html", first_name = first_name, last_name = last_name, email = email)

def add_quote():
    validation_check = Quote.validate_quote(request.form)
    if "_flashes" in session.keys() or not validation_check:
        flash("Adding quote to database was unsuccessful. Try again")
        return redirect("/dashboard")
    else:
        new_quote = Quote.add_new_quote(request.form)
        return redirect("/dashboard")

def like_quote():
    login_id = session["user_id"]
    cant_like_more_than_once = Like.query.filter(Like.user_id == login_id).filter(Like.quote_id == request.form["liked_quote_value"]).count()
    if int(cant_like_more_than_once) > 0:
        flash("You already liked quote!")
        return redirect("/dashboard")
    else:
        like_quote = Like.like_quote(request.form)
        return redirect("/dashboard")

def delete_quote():
    delete_quote = Quote.delete_quote(request.form)
    return redirect("/dashboard")

def view_quotes_added_by_one_user(id):
    one_user_quotes = all_quotes = db.session.query(Quote, User).filter(Quote.user_id == User.id).filter(User.id == id).all()
    print(one_user_quotes)
    return render_template("view_quotes_added_by_one_user.html", one_user_quotes = one_user_quotes)

def logout():
    session['logged_in'] = False
    session.clear()
    flash("You have been logged out. Thank you for visiting Quotes Dash!")
    return redirect("/")