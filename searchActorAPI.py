__auther__ = 'Ashish Patil'

from flask import Flask,request,jsonify
from mysql import connector
import mysql
import json
import MovieUtil
import searchActorUtil

def searchActorAPI():

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )
    cursor = con.cursor()

    cursor.execute("select * from actors where first_name = %s and last_name = %s",(first_name,last_name))

    actor_data = cursor.fetchall()
    cursor.close()

    # check for empty and more that one condition :
    isOneRecord = MovieUtil.validateLenght(actor_data)

    if not isOneRecord:
        return ""

    actor_id = actor_data[0][0]

    cursor = con.cursor()
    cursor.execute("select count(*) from roles where actor_id = %s", (actor_id,))

    NumberOfMovies = cursor.fetchall()[0][0]
    cursor.close()

    isGreaterThanZero = MovieUtil.validateNumberOfMoviesForDirectorOrActor(NumberOfMovies)

    if isOneRecord and isGreaterThanZero:
        cursor = con.cursor()
        cursor.execute("select * from movies m join roles r on m.id = r.movie_id where r.actor_id = %s order by m.year desc",
                       (actor_id,))

        movies_data = cursor.fetchall();
        cursor.close()

    searchActorDictionary = searchActorUtil.fillSearchActorAPI(first_name, last_name, NumberOfMovies, movies_data)
    searchActorDictionary = json.dumps(searchActorDictionary)

    return str(searchActorDictionary)