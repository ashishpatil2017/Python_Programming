__auther__ = 'Ashish Patil'

from flask import Flask,request,jsonify
from mysql import connector
import mysql
import json

def getGenres():

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )

    cursor = con.cursor()
    cursor.execute("select distinct(genre) from movies_genres")
    all_genre = cursor.fetchall()
    cursor.close()

    genre_dict = getGenreDict(all_genre)
    genre_dict = json.dumps(genre_dict)

    return genre_dict

def getGenreDict(all_genre):
  genre_list = []
  genre_dict = {}
  for val in all_genre:
    genre_list.append(val[0])
  genre_dict['All_Genres'] = genre_list
  return genre_dict

def getMovies():

    genre_of_movies = request.args.get('genre')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )

    cursor = con.cursor()
    cursor.execute("DROP VIEW `imdb`.`moviesSortedForGenres`")
    cursor.close()

    cursor = con.cursor()
    cursor.execute("create view moviesSortedForGenres as select * from movies m join movies_genres mg on m.id = mg.movie_id "
                   "where mg.genre = 'Short' and rankscore is not null order by m.year desc limit 10")
    cursor.close()

    cursor = con.cursor()
    cursor.execute("select name, year, rankscore from moviesSortedForGenres order by rankscore desc")
    moviesForGenre = cursor.fetchall()
    cursor.close()

    moviesDictForGenre = jsonFillingForMovieGenre(moviesForGenre)
    moviesDictForGenre = json.dumps(moviesDictForGenre)

    return moviesDictForGenre

def jsonFillingForMovieGenre(moviesForGenre):
  movie_dict = {}
  movie = []
  year = []
  rankscore = []
  for val in moviesForGenre :
    movie.append(val[0])
    year.append(val[1])
    rankscore.append(val[2])
  movie_dict['Movies'] = movie
  movie_dict['Years'] = year
  movie_dict['Ratings'] = rankscore
  return movie_dict
