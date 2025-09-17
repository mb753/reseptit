from flask import Flask
from flask import abort, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import config, db

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    sql = """SELECT r.title, r.id, u.username
             FROM recipes r, users u
             WHERE r.user_id = u.id"""
    recipes = db.query(sql)
    return render_template("index.html", recipes=recipes)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    try:
        sql = """SELECT r.title, r.id, u.username
                 FROM recipes r, users u
                 WHERE r.id = ? AND r.user_id = u.id"""
        recipe = db.query(sql, [recipe_id])[0]
    except:
        abort(404)

    if request.method == "POST":
        if "user_id" not in session:
            abort(403)
        comment = request.form["comment"]
        sql = "INSERT INTO comments (comment, recipe_id, user_id) VALUES (?, ?, ?)"
        db.execute(sql, [comment, recipe_id, session["user_id"]])
        return redirect("/recipe/" + str(recipe_id))

    sql = "SELECT ingredient FROM ingredients WHERE recipe_id = ?"
    ingredients = db.query(sql, [recipe_id])

    sql = "SELECT instruction FROM instructions WHERE recipe_id = ?"
    instructions = db.query(sql, [recipe_id])

    sql = """SELECT c.comment, c.user_id, u.username
             FROM comments c, users u
             WHERE c.recipe_id = ? AND u.id = c.user_id"""
    comments = db.query(sql, [recipe_id])

    return render_template("recipe.html", recipe=recipe, ingredients=ingredients, instructions=instructions, comments=comments)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        if "user_id" not in session:
            abort(403)

        recipe_creator = session["user_id"]
        recipe_name = request.form["recipe_name"]
        ingredients = request.form["ingredients"].split("\n")
        instructions = request.form["instructions"].split("\n")

        if recipe_name == "":
            recipe_name = "Nimetön resepti"

        sql = "INSERT INTO recipes (title, user_id) VALUES (?, ?)"
        db.execute(sql, [recipe_name, recipe_creator])
        recipe_id = db.last_insert_id()

        sql = "INSERT INTO ingredients (ingredient, recipe_id) VALUES (?, ?)"
        parameters = [(ingredient.strip(), recipe_id) for ingredient in ingredients]
        db.executemany(sql, parameters)

        sql = "INSERT INTO instructions (instruction, recipe_id) VALUES (?, ?)"
        parameters = [(instruction.strip(), recipe_id) for instruction in instructions]
        db.executemany(sql, parameters)

        return redirect("/")

    return render_template("add_recipe.html")


# add_recipe and edit_recipe probably should be combined somehow,
# as they have a lot in common

@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    try:
        sql = "SELECT title, user_id FROM recipes WHERE id = ?"
        recipe_name, recipe_creator = db.query(sql, [recipe_id])[0]
    except:
        abort(404)

    if "user_id" not in session:
        abort(403)
    if session["user_id"] != recipe_creator:
        abort(403)

    if request.method == "POST":
        recipe_name = request.form["recipe_name"]
        ingredients = request.form["ingredients"].split("\n")
        instructions = request.form["instructions"].split("\n")

        if recipe_name == "":
            recipe_name = "Nimetön resepti"

        sql = "UPDATE recipes SET title = ? WHERE id = ?"
        db.execute(sql, [recipe_name, recipe_id])

        sql = "DELETE FROM ingredients WHERE recipe_id = ?"
        db.execute(sql, [recipe_id])
        sql = "INSERT INTO ingredients (ingredient, recipe_id) VALUES (?, ?)"
        parameters = [(ingredient.strip(), recipe_id) for ingredient in ingredients]
        db.executemany(sql, parameters)

        sql = "DELETE FROM instructions WHERE recipe_id = ?"
        db.execute(sql, [recipe_id])
        sql = "INSERT INTO instructions (instruction, recipe_id) VALUES (?, ?)"
        parameters = [(instruction.strip(), recipe_id) for instruction in instructions]
        db.executemany(sql, parameters)

        return redirect("/recipe/" + str(recipe_id))

    sql = "SELECT ingredient FROM ingredients WHERE recipe_id = ?"
    ingredients = db.query(sql, [recipe_id])
    ingredients = "\n".join(ingredient[0] for ingredient in ingredients)

    sql = "SELECT instruction FROM instructions WHERE recipe_id = ?"
    instructions = db.query(sql, [recipe_id])
    instructions = "\n".join(instruction[0] for instruction in instructions)

    return render_template("edit_recipe.html", recipe_id=recipe_id, recipe_name=recipe_name, ingredients=ingredients, instructions=instructions)


@app.route("/delete_recipe/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    try:
        sql = "SELECT title, user_id FROM recipes WHERE id = ?"
        recipe_name, recipe_creator = db.query(sql, [recipe_id])[0]
    except:
        abort(404)

    if "user_id" not in session:
        abort(403)
    if session["user_id"] != recipe_creator:
        abort(403)

    if request.method == "POST":
        db.execute("DELETE FROM ingredients WHERE recipe_id = ?", [recipe_id])
        db.execute("DELETE FROM instructions WHERE recipe_id = ?", [recipe_id])
        db.execute("DELETE FROM comments WHERE recipe_id = ?", [recipe_id])
        db.execute("DELETE FROM recipes WHERE id = ?", [recipe_id])

        return redirect("/")

    return render_template("/delete_recipe.html", recipe_name=recipe_name, recipe_id=recipe_id)


@app.route("/search", methods=["GET", "POST"])
def search():
    recipes = None

    if request.method == "POST":
        search_string = request.form["search_string"]
        if search_string != "":
            sql = """SELECT r.id, r.title, u.username
                     FROM recipes r, users u
                     WHERE r.title LIKE '%' || ? || '%' AND r.user_id = u.id
                     UNION
                     SELECT r.id, r.title, u.username
                     FROM recipes r, users u, ingredients i
                     WHERE i.ingredient LIKE '%' || ? || '%' AND i.recipe_id = r.id AND r.user_id = u.id
                     UNION                    
                     SELECT r.id, r.title, u.username
                     FROM recipes r, users u, instructions i
                     WHERE i.instruction LIKE '%' || ? || '%' AND i.recipe_id = r.id AND r.user_id = u.id
                     UNION
                     SELECT r.id, r.title, u.username
                     FROM recipes r, users u, comments c
                     WHERE c.comment LIKE '%' || ? || '%' AND c.recipe_id = r.id AND r.user_id = u.id"""
            parameters = [search_string for i in range(4)]
            recipes = db.query(sql, parameters)

    return render_template("search.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if username == "":
            result = "VIRHE: anna käyttäjätunnus"
            return render_template("register.html", result=result)
        if password1 != password2:
            result = "VIRHE: salasanat eivät ole samat"
            return render_template("register.html", result=result, username=username)
        if password1 == "":
            result = "VIRHE: salasana on pakollinen"
            return render_template("register.html", result=result, username=username)
        
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except:
        # except sqlite3.IntegrityError:
            result = "VIRHE: tunnus on jo varattu"
            return render_template("register.html", result=result, username=username)

        return render_template("register.html", result=f"Tunnus {username} luotu")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            sql = "SELECT password_hash FROM users WHERE username = ?"
            password_hash = db.query(sql, [username])[0][0]
        except:
            result = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", result=result, username=username)

        # deal with test users from init.sql for which no password hash is stored
        if password_hash == None:
            result = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", result=result, username=username)

        if check_password_hash(password_hash, password):
            session["username"] = username
            user_id = db.query("SELECT id FROM users WHERE username = ?", [username])[0][0]
            session["user_id"] = user_id
            return redirect("/")
        else:
            result = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", result=result, username=username)

    return render_template("login.html")


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    
    return redirect("/")
