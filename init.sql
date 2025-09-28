PRAGMA foreign_keys = ON;

DELETE FROM recipes;
DELETE FROM users;
DELETE FROM category_names;

INSERT INTO users (username) VALUES ('Chef de cuisine');
INSERT INTO users (username) VALUES ('Monsieur Michelin');
INSERT INTO users (username) VALUES ('Crème de la crème');

INSERT INTO category_names (category_name) VALUES ('Alkupala');
INSERT INTO category_names (category_name) VALUES ('Pääruoka');
INSERT INTO category_names (category_name) VALUES ('Jälkiruoka');
INSERT INTO category_names (category_name) VALUES ('Vegaaninen');

INSERT INTO recipes (title, user_id) VALUES ('Mikrokaurapuuro', 1);
INSERT INTO recipe_categories (recipe_id, category_id) VALUES (1, 2);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('1 dl pikakaurahiutaleita', 1);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('2 dl vettä tai maitoa', 1);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('halutessasi ripaus suolaa', 1);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Sekoita ainekset ja keitä mikrossa noin 2 minuuttia.', 1);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Nauti esimerkiksi marjojen kera.', 1);
INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (5, 'Helppoa, edullista, ravitsevaa ja terveellistä! Täydellinen opiskelijan aamupala.', 1, 2);
INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (2, 'Miksi tässä ei ole ananasta?', 1, 3);

INSERT INTO recipes (title, user_id) VALUES ('Kiireisen päivän linssikeitto', 1);
INSERT INTO recipe_categories (recipe_id, category_id) VALUES (2, 2);
INSERT INTO recipe_categories (recipe_id, category_id) VALUES (2, 4);
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

INSERT INTO recipes(title, user_id) VALUES ('Kreikkalainen jogurtti pähkinöillä ja hunajalla', 3);
INSERT INTO recipe_categories (recipe_id, category_id) VALUES (3, 3);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('kiinteähköä kreikkalaista jogurttia', 3);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('kuorittuja saksanpähkinöitä', 3);
INSERT INTO ingredients (ingredient, recipe_id) VALUES ('juoksevaa hunajaa', 3);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Annostele jogurtti kulhoihin.', 3);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Murra saksanpähkinät pienemmiksi paloiksi ja ripottele jogurtin päälle.', 3);
INSERT INTO instructions (instruction, recipe_id) VALUES ('Lopuksi valuta päälle sopivasti hunajaa.', 3);
INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (5, 'Taivaallista! Resepti ei ole helpoimmasta päästä, mutta se on kyllä vaivansa väärti.', 3, 2);
INSERT INTO reviews (grade, comment, recipe_id, user_id) VALUES (4, 'Aika hyvää, mutta ohje on vähän epätarkka määrien suhteen.', 3, 1);
