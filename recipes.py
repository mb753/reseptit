import db


def count():
    return db.query("SELECT COUNT(*) FROM recipes")[0][0]


def get_list(limit=-1, offset=0):
    sql = """SELECT r.title, r.id, u.username, u.id AS user_id
             FROM recipes r, users u
             WHERE r.user_id = u.id
             LIMIT ? OFFSET ?"""
    return db.query(sql, [limit, offset])


def get(recipe_id):
    try:
        sql = """SELECT r.title, r.id, u.username, u.id AS user_id
                 FROM recipes r, users u
                 WHERE r.id = ? AND r.user_id = u.id"""
        return db.query(sql, [recipe_id])[0]
    except IndexError:      # not found
        return None


def get_categories(recipe_id):
    sql = """SELECT cn.category_name AS name, cn.id
            FROM category_names cn, recipe_categories rc
            WHERE rc.recipe_id = ? AND rc.category_id = cn.id"""
    return db.query(sql, [recipe_id])


def get_ingredients(recipe_id):
    sql = "SELECT ingredient FROM ingredients WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])


def get_instructions(recipe_id):
    sql = "SELECT instruction FROM instructions WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])


def get_reviews(recipe_id):
    sql = """SELECT r.grade, r.comment, r.user_id, u.username
             FROM reviews r, users u
             WHERE r.recipe_id = ? AND u.id = r.user_id"""
    return db.query(sql, [recipe_id])


def add(recipe_name, user_id):
    sql = "INSERT INTO recipes (title, user_id) VALUES (?, ?)"
    db.execute(sql, [recipe_name, user_id])
    return db.last_insert_id()


def update_name(new_name, recipe_id):
    sql = "UPDATE recipes SET title = ? WHERE id = ?"
    db.execute(sql, [new_name, recipe_id])


def update_ingredients(ingredients, recipe_id):
    sql = "DELETE FROM ingredients WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = "INSERT INTO ingredients (ingredient, recipe_id) VALUES (?, ?)"
    parameters = [(ingredient, recipe_id) for ingredient in ingredients]
    db.executemany(sql, parameters)


def update_instructions(instructions, recipe_id):
    sql = "DELETE FROM instructions WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = "INSERT INTO instructions (instruction, recipe_id) VALUES (?, ?)"
    parameters = [(instruction, recipe_id) for instruction in instructions]
    db.executemany(sql, parameters)


def update_categories(categories, recipe_id):
    sql = "DELETE FROM recipe_categories WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = "INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)"
    parameters = [(recipe_id, category) for category in categories]
    db.executemany(sql, parameters)


def add_review(grade, comment, recipe_id, user_id):
    sql = "INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [grade, comment, recipe_id, user_id])


def delete(recipe_id):
    db.execute("DELETE FROM recipes WHERE id = ?", [recipe_id])


def search(search_string):
    sql = """SELECT r.title, r.id, u.username, u.id AS user_id
             FROM recipes r, users u
             WHERE r.title LIKE ? AND r.user_id = u.id
             UNION
             SELECT r.title, r.id, u.username, u.id AS user_id
             FROM recipes r, users u, ingredients i
             WHERE i.ingredient LIKE ? AND i.recipe_id = r.id AND r.user_id = u.id
             UNION                    
             SELECT r.title, r.id, u.username, u.id AS user_id
             FROM recipes r, users u, instructions i
             WHERE i.instruction LIKE ? AND i.recipe_id = r.id AND r.user_id = u.id
             UNION
             SELECT rec.title, rec.id, u.username, u.id AS user_id
             FROM recipes rec, users u, reviews rev
             WHERE rev.comment LIKE ? AND rev.recipe_id = rec.id AND rec.user_id = u.id"""
    search_string = "%" + search_string + "%"
    parameters = [search_string for i in range(4)]
    return db.query(sql, parameters)


def user_recipes(user_id):
    sql = "SELECT title, id FROM recipes WHERE user_id = ?"
    return db.query(sql, [user_id])


def user_reviews(user_id):
    sql = """SELECT rec.title, rec.id
             FROM recipes rec, reviews rev
             WHERE rev.user_id = ? AND rev.recipe_id = rec.id"""
    return db.query(sql, [user_id])


def available_categories():
    sql = "SELECT id, category_name FROM category_names"
    return db.query(sql)
