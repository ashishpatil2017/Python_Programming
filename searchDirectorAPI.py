__auther__ = 'Ashish Patil'

from flask import Flask,request,jsonify
from mysql import connector
import mysql
import json
import directorAPIUtil
import MovieUtil

def searchDirectorAPI():

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )
    cursor = con.cursor()

    #query to search director for given director first name and director last name
    cursor.execute("select * from directors where first_name = %s and last_name =%s",(first_name,last_name))

    director_data = cursor.fetchall()
    cursor.close()

    #check for empty and more that one condition :
    isOneRecord = MovieUtil.validateLenght(director_data)

    if not isOneRecord:
        return ""

    director_id = director_data[0][0]

    cursor = con.cursor()
    cursor.execute("select count(*) from movies_directors where director_id = %s", (director_id,))

    NumberOfMovies = cursor.fetchall()[0][0]
    cursor.close()

    isGreaterThanZero = MovieUtil.validateNumberOfMoviesForDirectorOrActor(NumberOfMovies)

    if isOneRecord and isGreaterThanZero:
        cursor = con.cursor()
        cursor.execute("select * from movies m join movies_directors md on m.id = md.movie_id "
                       "where md.director_id = %s order by m.year desc limit 5",
            (director_id,))

        movies_data = cursor.fetchall();
        cursor.close()

        SearchDirector_Dict = directorAPIUtil.fillSearchDirectorAPI(first_name,last_name,NumberOfMovies,movies_data)
        SearchDirector_Dict = json.dumps(SearchDirector_Dict)
        return str(SearchDirector_Dict)

    return ""