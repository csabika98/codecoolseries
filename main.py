from flask import Flask, render_template, url_for, request, redirect, session, flash
from data import queries
import datetime
import bcrypt


app = Flask('codecool_series')
app.secret_key = "derank123"

# TOOL TO HASH PLAIN TEXT PASSWORD THANK TO THE BCRYPT!

def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

    return hashed_bytes.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)

@app.route('/shows/most-rated')
def most_rated_shows():
    most_rated = queries.most_rated_show()
    return render_template('most-rated.html', most_rated=most_rated)


@app.route('/login', methods=["GET","POST"])
def login_new_user():
    if request.method == "POST":
        user = queries.login_user(request.form["email"])
        if user:
            for i in user:
                if(verify_password(request.form["password"],i["password"])):
                    session["email"] = i["email"]
                    session["password"] = i["password"]
                    return redirect("/")
                else:
                    flash("Wrong password")
                    return redirect("/")
        else:
            flash("Login Failed: Wrong email or password", "red")
        return redirect("/")


@app.route('/logout', methods=["GET","POST"])
def logout():
    session.pop('email',None)
    session.pop("password", None)
    flash("You have been successfully logged out!","green")
    return redirect("/")


@app.route('/register', methods=["GET","POST"])
def register_new_user():
    users = queries.list_emails()
    nameuser = queries.list_usernames()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        created_on = datetime.datetime.today().strftime("%d-%B-%Y %H:%M:%S") # getting back today's date with this format YYYY-MM-DD
        has_password = hash_password(password)
        if nameuser:
            for nameus in nameuser:
                if request.form["username"] == nameus["username"]:
                    error_msg_1 = "This username is already taken"
                    flash(error_msg_1)
                    return redirect("/register")
                else:
                    queries.register(username, email, has_password, created_on)
        if users:
            for user in users:
                if email == user['email']:
                    error_msg_2 = 'This email is already taken!'
                    flash(error_msg_2)
                    return redirect("/register")
                else:
                    queries.register(username, email, has_password, created_on)
                    return redirect("/")
        else:
        #new_pass = queries.rewrite_password(has_password, email) 
            queries.register(username, email, has_password, created_on)
            return redirect("/")
    return render_template("register.html")


@app.route('/tv-show/<int:id>')
def showinfos(id):
    show_details = queries.overview(id)
    show_seasons = queries.seasonoverview(id)
    return render_template('tv-shows.html', show_details=show_details, show_seasons=show_seasons)

@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
