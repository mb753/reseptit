DELETE FROM users;
DELETE FROM recipes;
DELETE FROM ingredients;
DELETE FROM instructions;
DELETE FROM reviews;

INSERT INTO users (username) VALUES ('Chef de cuisine');
INSERT INTO users (username) VALUES ('Monsieur Michelin');
INSERT INTO users (username) VALUES ('Crème de la crème');

INSERT INTO recipes (title, user_id) VALUES ('Mikrokaurapuuro', 1);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('1 dl pikakaurahiutaleita', 1);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('2 dl vettä tai maitoa', 1);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('halutessasi ripaus suolaa', 1);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Sekoita ainekset ja keitä mikrossa noin 2 minuuttia.', 1);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Nauti esimerkiksi marjojen kera.', 1);
INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (5, 'Helppoa, edullista, ravitsevaa ja terveellistä! Täydellinen opiskelijan aamupala.', 1, 2);
INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (2, 'Miksi tässä ei ole ananasta?', 1, 3);

INSERT INTO recipes (title, user_id) VALUES ('Kiireisen päivän linssikeitto', 1);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('200 g kuivattuja punaisia linssejä', 2);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('1 purkki yrttitomaattimurskaa', 2);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('1 sipuli', 2);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('1 liemikuutio', 2);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('sopiva määrä vettä', 2);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('tilkka rypsiöljyä', 2);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Huuhtele linssit siivilässä.', 2);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Pilko sipuli ja kuullota se tilkassa öljyä kattilan pohjalla.', 2);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Lisää muut ainekset ja keitä noin 20 minuuttia.', 2);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Halutessasi viimeistele valmis annos tuoreilla yrteillä.', 2);
INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (5, 'Très bon! Tätä voi myös kivasti varioida. Voit esimerkiksi korvata yrttitomaattimurskan chilitomaattimurskalla ja lisätä yhden purkin curry-kaurakermaa.', 2, 2);
