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
    return render_template("index.html", recipes=recipes)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    recipe = db.query("""SELECT r.title, r.id, u.username
                      FROM recipes r, users u
                      WHERE r.id = ? AND r.user_id = u.id
                      """, [recipe_id])
    recipe = recipe[0] if recipe else abort(404)

    if request.method == "POST":
        if not session["username"]:
            abort(403)
        comment = request.form["comment"]
        db.execute("INSERT INTO comments (comment, recipe_id, user_id) VALUES (?, ?, ?)", [comment, recipe_id, session["user_id"]])
        return redirect("/recipe/" + str(recipe_id))

    ingredients = db.query("SELECT ingredient FROM ingredients WHERE recipe_id = ?", [recipe_id])
    instructions = db.query("SELECT instruction FROM instructions WHERE recipe_id = ?", [recipe_id])
    comments = db.query("SELECT c.comment, c.user_id, u.username FROM comments c, users u WHERE c.recipe_id = ? AND u.id = c.user_id", [recipe_id])

    return render_template("recipe.html", recipe=recipe, ingredients=ingredients, instructions=instructions, comments=comments)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        if not session["username"]:
            abort(403)

        recipe_name = request.form["recipe_name"]
        ingredients = request.form["ingredients"].split("\n")
        instructions = request.form["instructions"].split("\n")

        if recipe_name == "":
            recipe_name = "Nimetön resepti"

        db.execute("INSERT INTO recipes (title, user_id) VALUES (?, ?)", [recipe_name, session["user_id"]])
        recipe_id = db.last_insert_id()

        parameters = [(ingredient.strip(), recipe_id) for ingredient in ingredients]
        db.executemany("INSERT INTO ingredients (ingredient, recipe_id) VALUES (?, ?)", parameters)

        parameters = [(instruction.strip(), recipe_id) for instruction in instructions]
        db.executemany("INSERT INTO instructions (instruction, recipe_id) VALUES (?, ?)", parameters)

        return redirect("/")
    
    return render_template("add_recipe.html")


@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    return "Toiminto tulossa"


@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    try:
        recipe_creator = db.query("SELECT user_id FROM recipes WHERE id = ?", [recipe_id])[0][0]
    except:
        abort(404)

    if not session["user_id"]:
        abort(403)
    if session["user_id"] != recipe_creator:
        abort(403)

    db.execute("DELETE FROM ingredients WHERE recipe_id = ?", [recipe_id])
    db.execute("DELETE FROM instructions WHERE recipe_id = ?", [recipe_id])
    db.execute("DELETE FROM comments WHERE recipe_id = ?", [recipe_id])
    db.execute("DELETE FROM recipes WHERE id = ?", [recipe_id])

    return redirect("/")


@app.route("/search")
def search():
    return "Toiminto tulossa"


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
            session["user_id"] = db.query("SELECT id FROM users WHERE username = ?", [username])[0][0]
            return redirect("/")
        else:
            return render_template("login.html", result="VIRHE: väärä tunnus tai salasana")

    return render_template("login.html")


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")
