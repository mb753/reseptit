# Reseptit

Tämä reseptisovellus on harjoitustyö liittyen kurssiin [Tietokannat ja web-ohjelmointi](https://hy-tikawe.github.io/materiaali/). Sovelluksen aihe ja toiminnot ovat kurssimateriaalissa ehdotetun mukaiset.

HUOM. Sovellus ei ole vielä valmis.

## Sovelluksen toiminnot

* Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt reseptit.
* Käyttäjä pystyy etsimään reseptejä hakusanalla.
* Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
* Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).
* Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.

## Sovelluksen asennus

Tarvitset Pythonin ja SQLiten. Tarvittaessa asenna nämä ensin.

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Kloonaa repositiorio ja siirry kyseiseen hakemistoon.

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus näin:

```
$ flask run
```

Nyt voit avata sovelluksen selaimessa osoitteessa 127.0.0.1:5000.
