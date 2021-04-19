__auther__ = 'Ashish Patil'

from flask import Flask,request,jsonify
from mysql import connector
import mysql
import json

def insertActor():

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    gender = request.args.get('gender')
    checkPresent = request.args.get('checkPresent')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )
    cursor = con.cursor()
    cursor.execute("select current_value from counter where name = 'actors'")
    primary_key = cursor.fetchall()[0][0]
    cursor.close()

    cursor = con.cursor()
    cursor.execute("select * from actors where first_name = %s and last_name = %s", (first_name, last_name))
    actor_data = cursor.fetchall();
    cursor.close()

    if (checkPresent == 'True' and len(actor_data) == 1):
        return "1"
    elif (checkPresent == 'True' and len(actor_data) != 1):
        return "0"

    if len(actor_data) != 0:
        return "0"

    cursor = con.cursor()
    cursor.execute("insert into actors(id,first_name,last_name,gender) "
                   "values(%s,%s,%s,%s)", (primary_key, first_name, last_name, gender,))
    con.commit()
    cursor.close()

    cursor = con.cursor()
    cursor.execute("update counter set current_value = %s where name = 'actors'",(primary_key+1,))
    con.commit()
    cursor.close()

    return "1"

def insertDirector():

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    checkPresent = request.args.get('checkPresent')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )

    cursor = con.cursor()
    cursor.execute("select current_value from counter where name = 'directors'")
    primary_key = cursor.fetchall()[0][0]
    cursor.close()

    cursor = con.cursor()
    cursor.execute("select * from directors where first_name = %s and last_name = %s", (first_name, last_name))
    director_data = cursor.fetchall();
    cursor.close()

    if(checkPresent == 'True' and len(director_data) == 1):
        return "1"
    elif(checkPresent == 'True' and len(director_data) != 1):
        return "0"

    if len(director_data) != 0:
        return "0"

    cursor = con.cursor()
    cursor.execute("insert into directors(id,first_name,last_name) "
                   "values(%s,%s,%s)", (primary_key, first_name, last_name,))
    con.commit()
    cursor.close()

    cursor = con.cursor()
    cursor.execute("update counter set current_value = %s where name = 'directors'", (primary_key + 1,))
    con.commit()
    cursor.close()

    return "1"

def insertMovie():

    message = ""
    #Need to return final message :
    #1. Movie Already exist!
    #2. Successfully Inserted!

    movie_json = request.get_json()
    director_json = movie_json['Director']
    actor_json = movie_json['Actor']
    movie_genre = movie_json['Genre']

    movie_name = movie_json['Movie_Name']
    movie_year = movie_json['Year']

    #validate movie is present or not in the database, if present then return Message 1 else continue with the flow
    con = connectionDB()
    cursor = con.cursor()
    cursor.execute("select * from movies where name = %s",(movie_name,))
    movie_data = cursor.fetchall()
    cursor.close()

    if(len(movie_data) != 0):
        message = "Movie Already exist!"
        return message

    #validate and insert directors in the database and get primary keys
    director_keys = []
    for first_name,last_name in zip(director_json['first_name'],director_json['last_name']):
        con = connectionDB()
        cursor = con.cursor()
        cursor.execute("select * from directors where first_name = %s and last_name = %s", (first_name, last_name))
        director_data = cursor.fetchall();
        cursor.close()

        if(len(director_data) == 1):
            director_keys.append(director_data[0][0])
            continue
        elif (len(director_data) > 1):
            return "Multiple Director Data exist!"
        else:
            cursor = con.cursor()
            cursor.execute("select current_value from counter where name = 'directors'")
            primary_key = cursor.fetchall()[0][0]
            cursor.close()
            director_keys.append(primary_key)

            cursor = con.cursor()
            cursor.execute("insert into directors(id,first_name,last_name) "
                           "values(%s,%s,%s)", (primary_key, first_name, last_name,))
            con.commit()
            cursor.close()

            cursor = con.cursor()
            cursor.execute("update counter set current_value = %s where name = 'directors'", (primary_key + 1,))
            con.commit()
            cursor.close()

    #validate and insert actors in the database and get primary keys
    actor_key = []
    for first_name,last_name,gender in zip(actor_json['first_name'],actor_json['last_name'],actor_json['gender']):
        con = connectionDB()

        cursor = con.cursor()
        cursor.execute("select * from actors where first_name = %s and last_name = %s", (first_name, last_name))
        actor_data = cursor.fetchall();
        cursor.close()

        if (len(actor_data) == 1):
            actor_key.append(actor_data[0][0])
            continue
        elif (len(actor_data) > 1):
            return "Multiple Actor Data exist!"
        else:
            cursor = con.cursor()
            cursor.execute("select current_value from counter where name = 'actors'")
            primary_key = cursor.fetchall()[0][0]
            cursor.close()
            actor_key.append(primary_key)

            cursor = con.cursor()
            cursor.execute("insert into actors(id,first_name,last_name,gender) "
                           "values(%s,%s,%s,%s)", (primary_key, first_name, last_name, gender,))
            con.commit()
            cursor.close()

            cursor = con.cursor()
            cursor.execute("update counter set current_value = %s where name = 'actors'", (primary_key + 1,))
            con.commit()
            cursor.close()

    #insert movie details in movie table and get primary key of it
    con = connectionDB()
    cursor = con.cursor()
    cursor.execute("select current_value from counter where name = 'movies'")
    movie_id = cursor.fetchall()[0][0]
    cursor.close()

    cursor = con.cursor()
    cursor.execute("insert into movies(id,name,year,rankscore) "
                   "values(%s,%s,%s,%s)", (movie_id, movie_name, movie_year,0))
    con.commit()
    cursor.close()

    cursor = con.cursor()
    cursor.execute("update counter set current_value = %s where name = 'movies'", (movie_id + 1,))
    con.commit()
    cursor.close()

    #insert into roles table with movieid,actorid,roles
    insertIntoRolesTable(actor_json['role'],movie_id,actor_key)

    #insert into movie_genre table with movie_id and genres
    insertIntoGenreTable(movie_id,movie_genre)

    #insert into movies_director table with director_id and movie_id
    insertIntoMoviesDirectorTable(movie_id,director_keys)
    return "Successfully Inserted!"

def insertIntoMoviesDirectorTable(movie_id,director_keys):
    for index in range(0,len(director_keys)):
        con = connectionDB()
        cursor = con.cursor()
        cursor.execute("select * from movies_directors where movie_id = %s and "
                       "director_id = %s", (movie_id, director_keys[index],))
        row_len = len(cursor.fetchall())
        cursor.close()
        if (row_len != 0):
            return

        cursor = con.cursor()
        cursor.execute("insert into movies_directors(movie_id,director_id) "
                       "values(%s,%s)", (movie_id, director_keys[index],))
        con.commit()
        cursor.close()

def insertIntoGenreTable(movie_id, movie_genre):
    for index in range(0,len(movie_genre)):
        con = connectionDB()
        cursor = con.cursor()
        cursor.execute("select * from movies_genres where movie_id = %s and "
                       "genre = %s", (movie_id, movie_genre[index],))
        row_len = len(cursor.fetchall())
        cursor.close()
        if (row_len != 0):
            return

        cursor = con.cursor()
        cursor.execute("insert into movies_genres(movie_id,genre) "
                       "values(%s,%s)",(movie_id, movie_genre[index],))
        con.commit()
        cursor.close()

def insertIntoRolesTable(roles_data,movie_id,actor_key):
    for index in range(0,len(actor_key)):
        con = connectionDB()
        cursor = con.cursor()
        cursor.execute("select * from roles where actor_id = %s and movie_id = %s and "
                       "role = %s",(actor_key[index],movie_id,roles_data[index],))
        row_len = len(cursor.fetchall())
        cursor.close()
        if(row_len != 0):
            return

        cursor = con.cursor()
        cursor.execute("insert into roles(actor_id,movie_id,role) "
                       "values(%s,%s,%s)", (actor_key[index], movie_id, roles_data[index],))
        con.commit()
        cursor.close()

def connectionDB():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )
    return con




