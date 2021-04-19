__auther__ = 'Ashish Patil'

from flask import Flask,request,jsonify
from mysql import connector
import mysql
import json

def addReview():

    name = request.args.get('name')
    movie_name = request.args.get('movie_name')
    review_message = request.args.get('review_message')
    star = request.args.get('star')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )
    cursor = con.cursor()
    cursor.execute("insert into review(name,movie_name,review_message,star) "
                   "values(%s,%s,%s,%s)", (name, movie_name, review_message, star,))
    con.commit()
    cursor.close()

    return "1";


def getReview():

    movie_name = request.args.get('name')

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Stacker#123',
        database='IMDB'
    )

    cursor = con.cursor()
    cursor.execute("select * from review where movie_name = %s", (movie_name,))

    review_data = cursor.fetchall()
    cursor.close()

    if(len(review_data)==0):
        return ""

    final_dict = review_function(review_data)
    final_dict_up = json.dumps(final_dict)

    return str(final_dict_up)

def review_function(l1):
  final_dict = {}
  id = 1
  for row in l1:
    each_review = {}
    each_review["name"] = row[0]
    each_review["movie_name"] = row[1]
    each_review["comment"] = row[2]
    each_review["rating"] = row[3]
    final_dict[id] = each_review
    id = id+1
  return final_dict



