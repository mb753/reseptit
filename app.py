import math
import secrets
import sqlite3
import time

from flask import Flask
from flask import abort, g, render_template, redirect, request, session

import config
import recipes
import users


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
    page_count = math.ceil(recipes.count() / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    offset = page_size * (page - 1)
    recipe_list = recipes.get_list(page_size, offset)

    return render_template("index.html", recipes=recipe_list, page=page, page_count=page_count)


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def show_recipe(recipe_id):
    recipe = recipes.get(recipe_id)
    if recipe is None:
        abort(404)

    reviews = recipes.get_reviews(recipe_id)
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
        recipes.add_review(grade, comment, recipe_id, user_id)

        return redirect("/recipe/" + str(recipe_id))

    grades = [review["grade"] for review in reviews]
    grade_count = len(grades)
    if grade_count > 0:
        mean_grade = f"{round(sum(grades) / grade_count, 1)} / 5"
    else:
        mean_grade = "n/a"

    ingredients = recipes.get_ingredients(recipe_id)
    instructions = recipes.get_instructions(recipe_id)
    categories = recipes.get_categories(recipe_id)
    categories = " | ".join(category["name"] for category in categories)

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
        recipe = recipes.get(recipe_id)
        if recipe is None:
            abort(404)
        if session["user_id"] != recipe["user_id"]:
            abort(403)

    if request.method == "POST":
        check_csrf()

        recipe_name = request.form["recipe_name"]
        ingredients = request.form["ingredients"].split("\n")
        instructions = request.form["instructions"].split("\n")
        categories = request.form.getlist("category")

        if recipe_name == "":
            recipe_name = "Nimetön resepti"
        ingredients = [ingredient.strip() for ingredient in ingredients]
        instructions = [instruction.strip() for instruction in instructions]

        # figure out how to do the following in one transaction

        if not existing_recipe:
            recipe_id = recipes.add(recipe_name, session["user_id"])
        else:
            recipes.update_name(recipe_name, recipe_id)

        recipes.update_ingredients(ingredients, recipe_id)
        recipes.update_instructions(instructions, recipe_id)
        recipes.update_categories(categories, recipe_id)

        return redirect("/recipe/" + str(recipe_id))

    if request.method == "GET":

        categories = recipes.available_categories()

        if not existing_recipe:
            return render_template("edit_recipe.html", categories=categories)

        ingredients = recipes.get_ingredients(recipe_id)
        ingredients = "\n".join(ingredient[0] for ingredient in ingredients)

        instructions = recipes.get_instructions(recipe_id)
        instructions = "\n".join(instruction[0] for instruction in instructions)

        recipe_categories = recipes.get_categories(recipe_id)
        recipe_categories = [category["id"] for category in recipe_categories]

        return render_template("edit_recipe.html", recipe_id=recipe_id, recipe_name=recipe["title"],\
            ingredients=ingredients, instructions=instructions, categories=categories,\
            recipe_categories=recipe_categories)


@app.route("/delete_recipe/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    recipe = recipes.get(recipe_id)
    if recipe is None:
        abort(404)

    if "user_id" not in session:
        abort(403)
    if session["user_id"] != recipe["user_id"]:
        abort(403)

    if request.method == "POST":
        check_csrf()
        recipes.delete(recipe_id)
        return redirect("/")

    return render_template("/delete_recipe.html", recipe_name=recipe["title"], recipe_id=recipe_id)


@app.route("/search", methods=["GET", "POST"])
def search():
    result = None

    if request.method == "POST":
        search_string = request.form["search_string"]
        if search_string != "":
            result = recipes.search(search_string)

    return render_template("search.html", recipes=result)


@app.route("/user/<int:user_id>")
def user(user_id):
    username = users.get_username(user_id)
    if username is None:
        abort(404)

    created = recipes.user_recipes(user_id)
    reviewed = recipes.user_reviews(user_id)

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

        try:
            user_id = users.create_user(username, password1)
        except sqlite3.OperationalError:
            # Error message "sqlite3.OperationalError: database is locked" may appear
            # after having repeatedly tried to create a user that already exists.
            result = "VIRHE: jokin meni pieleen, yritä vähän ajan kuluttua uudestaan."
            return render_template("register.html", result=result, username=username)

        if user_id is None:
            result = "VIRHE: tunnus on jo varattu"
            return render_template("register.html", result=result, username=username)

        return render_template("register.html", result=f"Tunnus {username} luotu")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id is None:
            result = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", result=result, username=username)

        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)

        return redirect("/")

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
