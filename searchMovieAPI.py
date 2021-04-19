__auther__ = 'Ashish Patil'

from flask import Flask,request,jsonify
from mysql import connector
import mysql
import json
import MovieUtil

def searchMovieAPI():

    movie_name = request.args.get('movie_name')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )
    cursor = con.cursor()

    # query to search movie record given movie name
    cursor.execute("select * from movies where name = %s", (movie_name,))

    movie_data = cursor.fetchall()
    cursor.close()

    # check for empty and more that one condition :
    isOneRecord = MovieUtil.validateLenght(movie_data)

    if not isOneRecord :
        return ""

    movie_id = movie_data[0][0]

    # query to find actor details releted to perticular movie_id
    cursor = con.cursor()
    cursor.execute("select a.first_name,a.last_name,r.role from actors a join roles r on a.id = r.actor_id where r.movie_id = %s limit 5",(movie_id,))
    actor_data = cursor.fetchall()
    cursor.close()

    # query to find genres of the perticular movie id
    cursor = con.cursor()
    cursor.execute("select genre from movies_genres where movie_id = %s", (movie_id,))
    genre_data = cursor.fetchall()
    cursor.close()

    # query to find director details releted to perticular movie_id
    cursor = con.cursor()
    cursor.execute("select d.first_name, d.last_name from movies_directors md join directors d on md.director_id = d.id "
                   "where movie_id = %s",(movie_id,))
    director_data = cursor.fetchall()
    cursor.close()

    actorAPIDictionary = MovieUtil.fillMovieAPIDetails(movie_data, genre_data, director_data, actor_data)
    actorAPIDictionary = json.dumps(actorAPIDictionary)
    return str(actorAPIDictionary)
