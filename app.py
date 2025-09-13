from flask import Flask
from flask import abort, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import config, db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    recipes = db.query("""SELECT r.title, r.id, u.username
                       FROM recipes r, users u
                       WHERE r.user_id = u.id
                       """)
    return render_template("index.html", message="Reseptisovellus on rakenteilla.", recipes=recipes)

@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    recipe = db.query("""SELECT r.title, r.id, u.username
                      FROM recipes r, users u
                      WHERE r.id = ? AND r.user_id = u.id
                      """, [recipe_id])
    recipe = recipe[0] if recipe else abort(404)

    if request.method == "POST":
        comment = request.form["comment"]
        db.execute("INSERT INTO comments (comment, recipe_id, user_id) VALUES (?, ?, ?)", [comment, recipe_id, 3])
        return redirect("/recipe/" + str(recipe_id))

    ingredients = db.query("SELECT ingredient FROM ingredients WHERE recipe_id = ?", [recipe_id])
    instructions = db.query("SELECT instruction FROM instructions WHERE recipe_id = ?", [recipe_id])
    comments = db.query("SELECT c.comment, c.user_id, u.username FROM comments c, users u WHERE c.recipe_id = ? AND u.id = c.user_id", [recipe_id])

    return render_template("recipe.html", message="Reseptisovellus on rakenteilla.", recipe=recipe, ingredients=ingredients, instructions=instructions, comments=comments)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", result="VIRHE: salasanat eivät ole samat")
        if password1 == "":
            return render_template("register.html", result="VIRHE: salasana on pakollinen")
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            return render_template("register.html", result="VIRHE: tunnus on jo varattu")
        return render_template("register.html", result="Tunnus luotu")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", result="VIRHE: väärä tunnus tai salasana")

    return render_template("login.html")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
