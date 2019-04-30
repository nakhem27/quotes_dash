from config import db, re, func, flash, bcrypt, datetime, timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_user(cls, new_user_data):
        is_valid = True
        if len(new_user_data["first_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_user_data["first_name"]):
            is_valid = False
            flash("Please enter a valid first name.")
        if len(new_user_data["last_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_user_data["last_name"]):
            is_valid = False
            flash("Please enter a valid last name. Must be between 3-20 characters in length and contain no numbers or special characters.")
        if len(new_user_data["email"]) < 1 or not re.search("[^@]+@[^@]+\.[^@]+", new_user_data["email"]):
            is_valid = False
            flash("Please enter a valid email address containing @ AND . followed by com/org/etc.")
        if len(new_user_data["password"]) < 8:
            is_valid = False
            flash("Password should be at least 8 characters and contain one number and uppercase letter")
        if new_user_data["confirm_password"] != new_user_data["password"]:
            is_valid = False
            flash("Passwords do not match!")
        return is_valid

    @classmethod
    def add_new_user(cls, new_user_data):
        add_user = cls(
            first_name = new_user_data["first_name"],
            last_name = new_user_data["last_name"],
            email = new_user_data["email"],
            password = bcrypt.generate_password_hash(new_user_data["password"])
        )
        db.session.add(add_user)
        db.session.commit()
        flash("User successfully added! Login to view the Quote Dash Dashboard!")
        return add_user

    @classmethod
    def validate_edit_user(cls, edit_user_data):
        is_valid = True
        if len(new_user_data["first_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", edit_user_data["first_name"]):
            is_valid = False
            flash("Please enter a valid first name.")
        if len(new_user_data["last_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", edit_user_data["last_name"]):
            is_valid = False
            flash("Please enter a valid last name. Must be between 3-20 characters in length and contain no numbers or special characters.")
        if len(new_user_data["email"]) < 1 or not re.search("[^@]+@[^@]+\.[^@]+", edit_user_data["email"]):
            is_valid = False
        return is_valid

    @classmethod
    def edit_new_user(cls, new_user_data):
        edit_user = cls(
            edit_first_name = new_user_data["first_name"],
            edit_last_name = new_user_data["last_name"],
            edit_email = new_user_data["email"],
        )
        db.session.add(edit_user)
        db.session.commit()
        flash("You successfully updated your account!")
        return edit_user

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posted_by = db.relationship('User', foreign_keys=[user_id], backref='user_quotes', cascade='all')
    author_of_quote = db.Column(db.String(255))
    quote_content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def add_new_quote(cls, new_quote_data):
        add_quote = cls(
            user_id = new_quote_data["login_id"],
            posted_by = new_quote_data["posted_by"],
            author_of_quote = new_quote_data["author_of_quote"],
            quote_content = new_quote_data["quote_content"]
        )
        db.session.add(add_user)
        db.session.commit()
        flash("Quote successfully added!!")
        return add_quote

    @classmethod
    def delete_a_quote(cls, delete_quote_data):
        quote_instance_to_delete = Quote.query.filter(Quote.id == delete_quote_data['deleted_quote_value']).delete()
        db.session.commit()
        flash("You deleted this quote!")
        return quote_instance_to_delete
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_who_liked_quote = db.relationship('User', foreign_keys=[user_id], backref='user_liked', cascade='all')
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'))
    quote_liked_by_user = db.relationship('Quote', foreign_keys=[quote_id],backref='liked_quote', cascade='all')
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())