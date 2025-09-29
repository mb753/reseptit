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

Kloonaa repositorio ja siirry kyseiseen hakemistoon.

Halutessasi luo virtuaaliympäristö ja käynnistä se (ohjeet Linuxille):

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Asenna `flask`-kirjasto (jos loit virtuaaliympäristön, se asentuu vain sinne):

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus näin:

```
$ flask run
```

Nyt voit avata sovelluksen selaimessa osoitteessa `127.0.0.1:5000`.

## Testaus suurella datamäärällä

Korvataksesi tietokannan sisällön hyvin suurella määrällä testidataa:
* Varmista ensin, että tietokanta tauluineen on olemassa (luontiohjeet ylempänä).
* Suorita sen jälkeen skripti `seed.py`. Varaudu siihen, että skriptin suoritus kestää kauan.

Etusivun, reseptisivujen ja käyttäjäsivujen pitäisi tämän jälkeen edelleen avautua nopeasti tietokannassa olevien indeksien ansiosta.

Jos haluat, että terminaaliin tulostuu tieto siitä, kuinka kauan kunkin sivun avautuminen kesti, poista tiedostosta `app.py` funktioiden `before_request()` ja `after_request()` kommentointi.

Jos haluat kokeilla, kuinka paljon hitaampaa toiminta on ilman tietokannan indeksejä, avaa tietokantatiedosto SQLite-tulkissa (`$ sqlite3 database.db`) ja poista kukin indeksi komennolla `DROP INDEX indeksin_nimi;`. Voit katsoa indeksien nimet tiedostosta `schema.sql` tai tulkista komennolla `.indices`. Suorita lopuksi vielä komento `VACUUM;` jos haluat vapauttaa indeksien viemän levytilan.

Omalla koneellani, suurta testidataa käytettäessä, indeksit vaikuttivat näin:
* tietokannan koko ilman indeksejä n. 900 Mt, indeksien kanssa n. 1,4 Gt
* reseptisivun avaus ilman indeksejä n. 2 sek., indeksien kanssa n. 0 sek.
* käyttäjäsivun avaus ilman indeksejä n. 0,75 sek., indeksien kanssa n. 0 sek.
