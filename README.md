# Soccer Analysing


## Jak postawić projekt?

Projekt jest napisany przy wykorzystaniu standardowych modułów 'Python 3.8' a konkretnie
przy wykorzystaniu modułu 'Anakonda'. Przed początkiem parsowania danych niezbędnym jest postawienie
kilka dockier bloków.

W tym celu jedynie jest potrzebny [zaintalowany docker](https://docs.docker.com/docker-for-windows/install/)  
oraz wpisanie następującej komendy w terminalu:

```commandline
docker-compose.yml run -d
```

Następnie niezbędnie trzeba zainstalować wszystkie zewnętrzne python biblioteki.
Dla uruchomienia pobierania pakietów jedynie trzeba skorzystać z poniższego polecenia.

```commandline
pip install -r requirements.txt
```
Start projektu odbywa się za pomocą polecenia:
```commandline
scrapy runspider soccer/soccer/spiders/scraping.py -o data.json --loglevel=ERROR  --loglevel=INFO
```
Użycie flag ``--loglevel=ERROR`` powoduje, że w terminalu zastaną wyświetlane tylko błędy oraz flaka ``-o``
w skazuje na plik, w który zostaną zapisane zebrane dane.

## Pliki
* [scraping.py](soccer/soccer/spiders/scraping.py): główny plik scrapingu;
* [items.py](soccer/soccer/items.py): SoccerItem class;
* [Scraping.py](soccer/soccer/spiders/scraping.py): SoccerPipeline class, lączenie i zapis danych do database;

## Struktura bazy danych

![Database strukture](documentation/database.png)

## Jak pracuje?

1. Pobiera story internetowe dla poszczególnych Państw;
2. Z pobranych strony wyszukuje informacje o prowadzonych w nich ligach;
3. Wysyła Request dla lig/sezonów/stron;
4. Jeśli strona nie posiada danych o meczach przejść do 2, jeśli posiada to 5;
5. Wyszli do parsera;
6. Zapisz dane do objektu Item;
7. Wyszli i zapisz w bazie danych;

![Work plane](documentation/Map.jpg)

# Wyniki

| #  | Opis                       |        |
|:---|:---------------------------|:-------|
| 1  | Liczba meczów              | 121916 |
| 2  | Liczba przerobionych stron | 1432   |
| 3  | Liczba blędów              | 1      |




---------------------------------------------------------

