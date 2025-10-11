# Pylint-raportti

Pylint antaa sovelluksesta seuraavan palautteen:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:66:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:66:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:117:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:129:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:129:0: R0912: Too many branches (13/12) (too-many-branches)
app.py:129:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:203:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:203:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:221:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:237:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:249:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:249:0: R0911: Too many return statements (8/6) (too-many-return-statements)
app.py:249:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:294:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:294:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:315:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:324:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:332:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:12:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:19:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:29:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module recipes
recipes.py:8:0: C0301: Line too long (105/100) (line-too-long)
recipes.py:1:0: C0114: Missing module docstring (missing-module-docstring)
recipes.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:5:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
recipes.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:12:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
recipes.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:52:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:65:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:70:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:88:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:102:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:127:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:132:0: C0116: Missing function or method docstring (missing-function-docstring)
recipes.py:139:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 8.46/10
```

Seuraavassa perustelut, miksi nämä ilmoitukset on jätetty huomiotta.

## Useat ilmoitukset tyyppiä `C0114: Missing module docstring (missing-module-docstring)` tai `C0116: Missing function or method docstring (missing-function-docstring)`

Projekti on sen verran pieni ja moduulit ja funktiot on sen verran kuvaavasti nimetty, että uskon niiden toiminnan avautuvan riittävän hyvin myös ilman selitystekstejä.

## Useampi ilmoitus tyyppiä `R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)`

Jos oikein ymmärrän, mitä tämä ilmoitus tahtoo sanoa, kyse on siitä, että saman funktion `return`-komentojen antamilla palautusarvoilla ei ole aina samaa rakennetta, vaan palautettujen arvojen määrä voi vaihdella. Tämä johtuu siitä, että eri tilanteissa sivupohjien tarvitsemien tietojen määrä vaihtelee. Pylint ilmeisesti haluaisi, että tilanteissa, joissa jotakin parametria ei tarvita, se kuitenkin välitettäisiin arvolla `None` sen sijaan että se jätetään kokonaan välittämättä. En ole vakuuttunut siitä, että tämä parantaisi koodin luettavuutta.

## Ilmoitus `app.py:129:0: R0912: Too many branches (13/12) (too-many-branches)`

Funktio `edit_recipe()` haarautuu Pylintin mielestä liian moneen `if`-`else`-haaraan. Epäilen, että 12 haaran yläraja on mielivaltainen luku eikä perustu nimenomaisen funktioni analyysiin. Omasta mielestäni funktio on selkeä ja toimiva juuri näin.

## Ilmoitus `app.py:249:0: R0911: Too many return statements (8/6) (too-many-return-statements)`

Näköjään Pylintin mielestä funktio saisi sisältää korkeintaan 6 `return`-komentoa. Tätäkin epäilen hatusta vedetyksi luvuksi, jota Pylint soveltaa kaavamaisesti kaikkiin funktioihin ja joka ei perustu nimenomaisen funktioni analyysiin. Funktio `register()` sisältää 8 `return`-komentoa, mutta se on mielestäni selkeä näin.

## Ilmoitus `config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)`

Tämä liittyy moduuliin `config.py`, joka on tehty kurssimateriaalin mallin mukaisesti. `secret_key` tulkitaan tässä vakioksi, joka konvention mukaan pitäisi kirjoittaa isolla. Se ei kuitenkaan oikeasti ole kovakoodattu vakio, vaan pikemminkin ympäristömuuttuja, jolla voisi olla jokin toinenkin arvo.

## Useampi ilmoitus tyyppiä `W0102: Dangerous default value [] as argument (dangerous-default-value)`

Nämä liittyvät moduuliin `db.py`, joka sekin on tehty kurssimateriaalin mallin mukaisesti. Lista on tosiaan kyseenalainen oletusparametri, koska sen sisältö säilyy funktiokutsujen välillä, mutta tässä tapauksessa vahinkoa ei pääse syntymään, koska oletusarvo-lista pysyy tyhjänä koko ajan.

## Ilmoitus `recipes.py:8:0: C0301: Line too long (105/100) (line-too-long)`

Tämän voisi ehkä korjatakin, mutta toisaalta pidän siitä, että rivin 8 koodi, joka on vaihtoehtoinen rivin 6 koodille, näkyy yhdellä rivillä niin kuin vaihtoehtonsakin. Funktio on "symmetrisempi" näin.

## Useampi ilmoitus tyyppiä `R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)`

Tämäkin liittyy moduuliin `recipes.py`, riveihin 5- ja 12-. Koodin voisi kirjoittaa lyhyemmin poistamalla `else`-avainsanat, mutta mielestäni tuon avainsanan käyttö tekee koodin rakenteen helpommin hahmotettavaksi, koska kaksi vaihtoehtoista haaraa näkyy samalla tavalla.
