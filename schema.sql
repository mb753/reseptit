CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE category_names (
    id INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE
);

CREATE TABLE recipe_categories (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE,
    category_id INTEGER REFERENCES category_names
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    ingredient TEXT,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE
);

CREATE TABLE instructions (
    id INTEGER PRIMARY KEY,
    instruction TEXT,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    grade INTEGER,
    comment TEXT,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE,
    user_id INTEGER REFERENCES users
);
