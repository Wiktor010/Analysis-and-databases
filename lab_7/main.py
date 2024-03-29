import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple, Iterator

from pandas import DataFrame

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020');

def film_in_category(category_id:int)-> Union[Iterator[DataFrame], DataFrame, None]:
    if type(category_id) == int:
        df = pd.read_sql("SELECT film.title, language.name languge, category.name category FROM film " 
                         "INNER JOIN language ON film.language_id = language.language_id " 
                         "INNER JOIN film_category ON film.film_id = film_category.film_id " 
                         "INNER JOIN category ON film_category.category_id = category.category_id " 
                         "WHERE category.category_id = {a} ".format(a=category_id) +
                         "ORDER BY film.title, language.name", con=connection)

        return df

    else:
        return None



    # ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    # Przykład wynikowej tabeli:
    # |   |title          |languge    |category|
    # |0	|Amadeus Holy	|English	|Action|
    #
    # Tabela wynikowa ma być posortowana po tylule filmu i języku.
    #
    # Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    #
    # Parameters:
    # category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    #
    # Returns:
    # pd.DataFrame: DataFrame zawierający wyniki zapytania
    # '''
    return None
    
def number_films_in_category(category_id:int)-> Union[Iterator[DataFrame], DataFrame, None]:
    if type(category_id) == int:
        df = pd.read_sql("SELECT category.name category, COUNT(category.name) FROM film " 
                         "INNER JOIN film_category ON film.film_id = film_category.film_id " 
                         "INNER JOIN category ON film_category.category_id = category.category_id " 
                         "WHERE category.category_id = {a} ".format(a=category_id) +
                         "GROUP BY category.name ", con=connection)

        return df

    else:
        return None


    # ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    # Przykład wynikowej tabeli:
    # |   |category   |count|
    # |0	|Action 	|64	  |
    #
    # Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    #
    # Parameters:
    # category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    #
    # Returns:
    # pd.DataFrame: DataFrame zawierający wyniki zapytania
    # '''
    return None

def number_film_by_length(min_length: Union[int,float] = 0, max_length: Union[int,float] = 1e6 ) :
    u = Union[int, float].__args__
    if isinstance(min_length, u) and isinstance(max_length, u) and min_length < max_length:
        df = pd.read_sql("SELECT film.length, COUNT(film.length) FROM film " 
                         "WHERE film.length BETWEEN '{a}' AND '{b}' ".format(a=min_length, b=max_length) +
                         "GROUP BY film.length ", con=connection)

        return df

    else:
        return None



    # ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości pomiędzy wartościami min_length a max_length.
    # Przykład wynikowej tabeli:
    # |   |length     |count|
    # |0	|46 	    |64	  |
    #
    # Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    #
    # Parameters:
    # min_length (int,float): wartość minimalnej długości filmu
    # max_length (int,float): wartość maksymalnej długości filmu
    #
    # Returns:
    # pd.DataFrame: DataFrame zawierający wyniki zapytania
    # '''
    return None

def client_from_city(city:str)-> Union[Iterator[DataFrame], DataFrame, None]:
    if isinstance(city,str):
        df = pd.read_sql("SELECT city.city, customer.first_name, customer.last_name FROM city " 
                         "INNER JOIN address ON city.city_id = address.city_id " 
                         "INNER JOIN customer ON address.address_id = customer.address_id "
                         "WHERE city.city = '{a}' ".format(a=city) +
                         "ORDER BY customer.last_name, customer.first_name", con=connection)

        return df

    else:
        return None


    # ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    # Przykład wynikowej tabeli:
    # |   |city	    |first_name	|last_name
    # |0	|Athenai	|Linda	    |Williams
    #
    # Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    #
    # Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    #
    # Parameters:
    # city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    #
    # Returns:
    # pd.DataFrame: DataFrame zawierający wyniki zapytania
    # '''


def avg_amount_by_length(length:Union[int,float])->pd.DataFrame:

    if isinstance(length, (int,float)):
        df = pd.read_sql("SELECT film.length, AVG(payment.amount) FROM film " 
                         "INNER JOIN inventory ON film.film_id = inventory.film_id "
                         "INNER JOIN rental ON inventory.inventory_id = rental.inventory_id " 
                         "INNER JOIN payment ON rental.rental_id = payment.rental_id " 
                         "WHERE film.length = '{a}'".format(a=length) +
                         "GROUP BY film.length ", con=connection)

        return df

    else:
        return None

    # ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    # Przykład wynikowej tabeli:
    # |   |length |avg
    # |0	|48	    |4.295389
    #
    #
    # Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    #
    # Parameters:
    # length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    #
    # Returns:
    # pd.DataFrame: DataFrame zawierający wyniki zapytania
    # '''


def client_by_sum_length(sum_min:Union[int,float])->pd.DataFrame:
    if isinstance(sum_min, (int, float)) and sum_min >= 0:
        df = pd.read_sql("SELECT customer.first_name, customer.last_name, SUM(film.length) FROM film " 
                         "INNER JOIN inventory ON film.film_id = inventory.film_id " 
                         "INNER JOIN rental ON inventory.inventory_id = rental.inventory_id " 
                         "INNER JOIN customer ON rental.customer_id = customer.customer_id " 
                         "GROUP BY customer.first_name, customer.last_name " 
                         "HAVING SUM(film.length) >= '{a}'".format(a=sum_min) +
                         "ORDER BY SUM(film.length), customer.last_name, customer.first_name", con=connection)

        return df
    else:
        return None

    # ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    # Przykład wynikowej tabeli:
    # |   |first_name |last_name  |sum
    # |0  |Brian	    |Wyman  	|1265
    #
    # Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    # Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    #
    # Parameters:
    # sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    #
    # Returns:
    # pd.DataFrame: DataFrame zawierający wyniki zapytania
    # '''

def category_statistic_length(name:str)->pd.DataFrame:
    if isinstance(name, str):
        df = pd.read_sql("SELECT category.name category, AVG(film.length), SUM(film.length), " 
                         "MIN(film.length), MAX(film.length) FROM film " +
                         "INNER JOIN film_category ON film.film_id = film_category.film_id " 
                         "INNER JOIN category ON film_category.category_id = category.category_id " 
                         "WHERE category.name = '{a}' ".format(a=name) +
                         "GROUP BY category.name ", con=connection)

        return df
    else:
        return None

    # ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    # Przykład wynikowej tabeli:
    # |   |category   |avg    |sum    |min    |max
    # |0	|Action 	|111.60 |7143   |47 	|185
    #
    # Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    #
    # Parameters:
    # name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    #
    # Returns:
    # pd.DataFrame: DataFrame zawierający wyniki zapytania
    # '''
