from flask import Flask
from flask import render_template
import db

app = Flask(__name__)

@app.route("/")
def index():
    recipes = db.query("""SELECT r.title, u.username
                       FROM recipes r, users u
                       WHERE r.user_id = u.id
                       """)
    return render_template("index.html", message="Reseptisovellus on rakenteilla.", recipes=recipes)
