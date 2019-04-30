from flask import Flask, render_template, redirect, flash, request, session
from config import app, db, func, IntegrityError, bcrypt, re
from models import User, Quote

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
        session["user_id"] = login_user[0].id
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
    posted_by = "str(first_name) " + "str(last_name)"
    login_id = session["user_id"]
    all_quotes = Quote.query.all()
    return render_template("dashboard.html", login_name = login_name, login_id = login_id, posted_by = posted_by, all_quotes = all_quotes)

def view_edit_account():
    login_id = session["login_id"]
    first_name = session["first_name"]
    last_name = session["last_name"]
    email = session["email"]
    return render_template("editaccount.html", first_name = first_name, last_name = last_name, email = email)

def update_account():
    validation_check = User.validate_edit_user(request.form)
    if "_flashes" in session.keys() or not validation_check:
        flash("Update account information unsuccessful. Please Try Again!")
        return redirect("/dashboard")
    else:
        try:
            edit_user = User.edit_new_user(request.form)
            return redirect("/dashboard")
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. This email already exists for this account! Please try a different email address!")
            return redirect("/view_edit_account")

def add_quote():
    return redirect("/")

def like_quote():
    return redirect("/")

def delete_quote():
    return redirect("/")

def view_quotes_added_by_one_user():
    one_user_quotes = 1
    return render_template("view_quotes_added_by_one_user.html", one_user_quotes = one_user_quotes)

def logout():
    session['logged_in'] = False
    session.clear()
    flash("You have been logged out. Thank you for visiting Quotes Dash!")
    return redirect("/")