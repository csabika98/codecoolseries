from flask import Flask, render_template, url_for, request, redirect, session, flash, jsonify
from data import queries
import datetime
import bcrypt
from data import validation as validate


app = Flask(__name__)
app.secret_key = "derank123"



@app.route("/search", methods=["GET"])
def search():
    all_shows = queries.get_shows()
    search_result = request.args.get("find")
    if request.method == "GET":
        result = queries.search_shows(search_result)
        print(result)
    return render_template("search.html", result=result, all_shows=all_shows)
   


#CREATE API ROUTE TO MAKE POSSIBLE THE PAGINATION!
@app.route('/api/most-rated/<int:page>')
def api_route(page):
    page_number = page
    if page == None:
        page = 1
    top_shows = queries.most_rated_show(page_number)
    return jsonify(top_shows)


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
    return render_template('most-rated.html')


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
    emails = validate.check_for_email()
    user = validate.check_for_username()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        created_on = datetime.datetime.today().strftime("%d-%B-%Y %H:%M:%S") # getting back today's date with this format YYYY-MM-DD
        has_password = hash_password(password)
        if username in user:
            flash("This username has been taken Please choose another!")
            return redirect("/register")
        elif email in emails:
            flash("This email has been taken Please choose another!")
            return redirect("/register")
        else:
            flash("Registration completed! You can log in now!")
            queries.register(username, email, has_password, created_on)
            return redirect("/")

    return render_template("register.html")


@app.route('/shows/<int:id>')
def showinfos(id):
    show_details = queries.overview(id)
    show_seasons = queries.seasonoverview(id)
    return render_template('tv-shows.html', show_details=show_details, show_seasons=show_seasons)

@app.route('/design')
def design():
    return render_template('design.html')
    


if __name__ == '__main__':
    app.run(debug=True)
