from flask import Flask
from flask import abort, render_template, redirect, request
import db

app = Flask(__name__)

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
