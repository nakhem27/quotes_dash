from config import app
from controller_functions import home, register, login, dashboard, view_quotes_added_by_one_user, add_quote, like_quote, delete_quote, view_edit_account, update_account, logout

app.add_url_rule("/", view_func=home)
app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/dashboard", view_func=dashboard, methods=["GET", "POST"])
app.add_url_rule("/user/<id>", view_func=view_quotes_added_by_one_user, methods=["POST"])
app.add_url_rule("/add_quote", view_func=add_quote, methods=["POST"])
app.add_url_rule("/like_quote", view_func=like_quote, methods=["POST"])
app.add_url_rule("/delete_quote", view_func=delete_quote, methods=["POST"])
app.add_url_rule("/myaccount/<id>", view_func=view_edit_account, methods=["POST"])
app.add_url_rule("/edit_account", view_func=update_account, methods=["POST"])
app.add_url_rule("/logout", view_func=logout, methods=["POST"])