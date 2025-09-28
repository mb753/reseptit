"""
Run this script to overwrite the existing database with a large amount of test data.
Before starting, make sure the database exists and includes the required tables.
"""

import random
import sqlite3

db = sqlite3.connect("database.db")
db.execute("PRAGMA foreign_keys = ON")

print("emptying database")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM users")
db.execute("DELETE FROM category_names")


CATEGORY_NAME_COUNT = 10
USER_COUNT = 100000

RECIPE_COUNT = USER_COUNT * 10
RECIPE_CATEGORIES_COUNT = RECIPE_COUNT * 3
INGREDIENT_COUNT = RECIPE_COUNT * 10
INSTRUCTION_COUNT = RECIPE_COUNT * 10
REVIEW_COUNT = RECIPE_COUNT * 10


def rand(limit):
    """Choose a random integer between 1 and limit (inclusive)."""
    return random.randint(1, limit)


print(f"creating {CATEGORY_NAME_COUNT:,} category names")
for i in range(1, CATEGORY_NAME_COUNT + 1):
    db.execute("INSERT INTO category_names (category_name) VALUES (?)",
               [f"luokka{i}"])

print(f"creating {USER_COUNT:,} users")
for i in range(1, USER_COUNT + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               [f"käyttäjä{i}"])

print(f"creating {RECIPE_COUNT:,} recipes")
for i in range(1, RECIPE_COUNT + 1):
    db.execute("INSERT INTO recipes (title, user_id) VALUES (?, ?)",
                [f"resepti{i}", rand(USER_COUNT)])

print(f"creating {RECIPE_CATEGORIES_COUNT:,} recipe categories")
for i in range(1, RECIPE_CATEGORIES_COUNT + 1):
    db.execute("INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)",
                    [rand(RECIPE_COUNT), rand(CATEGORY_NAME_COUNT)])

print(f"creating {INGREDIENT_COUNT:,} ingredients")
for i in range(1, INGREDIENT_COUNT + 1):
    db.execute("INSERT INTO ingredients (ingredient, recipe_id) VALUES (?, ?)",
                [f"aines{i}", rand(RECIPE_COUNT)])

print(f"creating {INSTRUCTION_COUNT:,} instructions")
for i in range(1, INSTRUCTION_COUNT + 1):
    db.execute("INSERT INTO instructions (instruction, recipe_id) VALUES (?, ?)",
                [f"askel{i}", rand(RECIPE_COUNT)])

print(f"creating {REVIEW_COUNT:,} reviews")
for i in range(1, REVIEW_COUNT + 1):
    db.execute("INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (?, ?, ?, ?)",
                [rand(5), f"kommentti{i}", rand(RECIPE_COUNT), rand(USER_COUNT)])


print("committing changes")
db.commit()

db.close()
print("finished")
