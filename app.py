from flask import Flask
from flask import abort, render_template
import db

app = Flask(__name__)

@app.route("/")
def index():
    recipes = db.query("""SELECT r.title, r.id, u.username
                       FROM recipes r, users u
                       WHERE r.user_id = u.id
                       """)
    return render_template("index.html", message="Reseptisovellus on rakenteilla.", recipes=recipes)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = db.query("""SELECT r.title, u.username
                      FROM recipes r, users u
                      WHERE r.id = ? AND r.user_id = u.id
                      """, [recipe_id])
    recipe = recipe[0] if recipe else abort(404)
    ingredients = db.query("SELECT ingredient FROM ingredients WHERE recipe_id = ?", [recipe_id])
    instructions = db.query("SELECT instruction FROM instructions WHERE recipe_id = ?", [recipe_id])
    return render_template("recipe.html", message="Reseptisovellus on rakenteilla.", recipe=recipe, ingredients=ingredients, instructions=instructions)
