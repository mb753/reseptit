import math
import secrets
# import sqlite3
import time

from flask import Flask
from flask import abort, g, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash

import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key


# Uncomment the following two functions to measure the duration
# of page requests and print the measurements to the terminal.

# @app.before_request
# def before_request():
#     g.start_time = time.time()

# @app.after_request
# def after_request(response):
#     elapsed_time = round(time.time() - g.start_time, 2)
#     print("elapsed time:", elapsed_time, "s")
#     return response


@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    recipe_count = db.query("SELECT COUNT(*) FROM recipes")[0][0]
    page_count = math.ceil(recipe_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    sql = """SELECT r.title, r.id, u.username, u.id AS user_id
             FROM recipes r, users u
             WHERE r.user_id = u.id
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    recipes = db.query(sql, [limit, offset])

    return render_template("index.html", recipes=recipes, page=page, page_count=page_count)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    try:
        sql = """SELECT r.title, r.id, u.username, u.id AS user_id
                 FROM recipes r, users u
                 WHERE r.id = ? AND r.user_id = u.id"""
        recipe = db.query(sql, [recipe_id])[0]
    except:
        abort(404)

    sql = """SELECT r.grade, r.comment, r.user_id, u.username
             FROM reviews r, users u
             WHERE r.recipe_id = ? AND u.id = r.user_id"""
    reviews = db.query(sql, [recipe_id])
    reviewers = [review["user_id"] for review in reviews]

    allow_review = False
    if "user_id" in session:
        if (session["user_id"] not in reviewers) and (session["user_id"] != recipe["user_id"]):
            allow_review = True

    if request.method == "POST":
        check_csrf()
        if not allow_review:
            return "Et voi arvioida tätä reseptiä, koska olet jo arvioinut sen tai kyse on "\
                "omasta reseptistäsi."

        grade = request.form["grade"]
        comment = request.form["comment"]
        user_id = session["user_id"]
        sql = "INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (?, ?, ?, ?)"
        db.execute(sql, [grade, comment, recipe_id, user_id])
        return redirect("/recipe/" + str(recipe_id))

    grades = [review["grade"] for review in reviews]
    grade_count = len(grades)
    if grade_count > 0:
        mean_grade = f"{round(sum(grades) / grade_count, 1)} / 5"
    else:
        mean_grade = "n/a"

    sql = "SELECT ingredient FROM ingredients WHERE recipe_id = ?"
    ingredients = db.query(sql, [recipe_id])

    sql = "SELECT instruction FROM instructions WHERE recipe_id = ?"
    instructions = db.query(sql, [recipe_id])

    sql = """SELECT cn.category_name
             FROM category_names cn, recipe_categories rc
             WHERE rc.recipe_id = ? AND rc.category_id = cn.id"""
    categories = db.query(sql, [recipe_id])
    categories = " | ".join(category[0] for category in categories)

    return render_template("recipe.html", recipe=recipe, ingredients=ingredients,\
        instructions=instructions, reviews=reviews, reviewers=reviewers,\
        allow_review=allow_review, mean_grade=mean_grade, grade_count=grade_count,\
        categories=categories)


@app.route("/add_recipe", methods=["GET", "POST"])
@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id=None):

    if "user_id" not in session:
        abort(403)

    existing_recipe = recipe_id is not None

    if existing_recipe:
        try:
            sql = "SELECT title, user_id FROM recipes WHERE id = ?"
            recipe_name, recipe_creator = db.query(sql, [recipe_id])[0]
        except:
            abort(404)
        if session["user_id"] != recipe_creator:
            abort(403)

    if request.method == "POST":
        check_csrf()

        recipe_name = request.form["recipe_name"]
        ingredients = request.form["ingredients"].split("\n")
        instructions = request.form["instructions"].split("\n")
        categories = request.form.getlist("category")

        if recipe_name == "":
            recipe_name = "Nimetön resepti"

        # figure out how to do the following in one transaction

        if not existing_recipe:
            recipe_creator = session["user_id"]
            sql = "INSERT INTO recipes (title, user_id) VALUES (?, ?)"
            db.execute(sql, [recipe_name, recipe_creator])
            recipe_id = db.last_insert_id()
        else:
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

        sql = "DELETE FROM recipe_categories WHERE recipe_id = ?"
        db.execute(sql, [recipe_id])
        sql = "INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)"
        parameters = [(recipe_id, category) for category in categories]
        db.executemany(sql, parameters)

        return redirect("/recipe/" + str(recipe_id))

    if request.method == "GET":

        sql = "SELECT id, category_name FROM category_names"
        categories = db.query(sql)

        if not existing_recipe:
            return render_template("edit_recipe.html", categories=categories)

        sql = "SELECT ingredient FROM ingredients WHERE recipe_id = ?"
        ingredients = db.query(sql, [recipe_id])
        ingredients = "\n".join(ingredient[0] for ingredient in ingredients)

        sql = "SELECT instruction FROM instructions WHERE recipe_id = ?"
        instructions = db.query(sql, [recipe_id])
        instructions = "\n".join(instruction[0] for instruction in instructions)

        sql = "SELECT category_id FROM recipe_categories WHERE recipe_id = ?"
        recipe_categories = db.query(sql, [recipe_id])
        recipe_categories = [category[0] for category in recipe_categories]

        return render_template("edit_recipe.html", recipe_id=recipe_id, recipe_name=recipe_name,\
            ingredients=ingredients, instructions=instructions, categories=categories,\
            recipe_categories=recipe_categories)


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
        check_csrf()
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
                     SELECT rec.id, rec.title, u.username
                     FROM recipes rec, users u, reviews rev
                     WHERE rev.comment LIKE '%' || ? || '%' AND rev.recipe_id = rec.id AND rec.user_id = u.id"""
            parameters = [search_string for i in range(4)]
            recipes = db.query(sql, parameters)

    return render_template("search.html", recipes=recipes)


@app.route("/user/<int:user_id>")
def user(user_id):
    try:
        sql = "SELECT username FROM users WHERE id = ?"
        username = db.query(sql, [user_id])[0][0]
    except:
        abort(404)

    sql = "SELECT title, id FROM recipes WHERE user_id = ?"
    created = db.query(sql, [user_id])

    sql = """SELECT rev.recipe_id AS id, rec.title
             FROM reviews rev, recipes rec
             WHERE rev.user_id = ? AND rev.recipe_id = rec.id"""
    reviewed = db.query(sql, [user_id])

    return render_template("user.html", username=username, created=created, reviewed=reviewed)


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
            sql = "SELECT id, password_hash FROM users WHERE username = ?"
            user_id, password_hash = db.query(sql, [username])[0]
        except:
            result = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", result=result, username=username)

        # deal with test users from init.sql for which no password hash is stored
        if password_hash == None:
            result = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", result=result, username=username)

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
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
        del session["csrf_token"]

    return redirect("/")


def check_csrf():
    if "csrf_token" not in session:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
