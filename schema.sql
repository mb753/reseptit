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

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    ingredient TEXT,
    recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE instructions (
    id INTEGER PRIMARY KEY,
    instruction TEXT,
    recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    grade INTEGER,
    comment TEXT,
    recipe_id INTEGER REFERENCES recipes,
    user_id INTEGER REFERENCES users
);
