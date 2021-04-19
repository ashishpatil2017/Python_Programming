__auther__ = 'Ashish Patil'

def validateLenght(record):
    #this function checks number of records from the query result
    #if number of records greater than one or zero then return false
    #if number of records equals to one then returns true
    if(len(record) == 1):
        return True
    return False

def validateNumberOfMoviesForDirectorOrActor(n):
    if n>0:
        return True
    return False

def fillMovieAPIDetails(movie_data, genre_data, director_data, actor_data):
  MovieDictionary = {}
  Actor_details = {}
  actor_list = []
  roles_list = []
  genre_list = []
  directors = ""
  MovieDictionary['Movie_Name'] = movie_data[0][1]
  MovieDictionary['Year'] = movie_data[0][2]
  for val in genre_data :
    genre_list.append(val[0])
  MovieDictionary['Genres'] = genre_list
  for val in director_data:
    directors = directors + val[0] + " " + val [1]
    if(len(director_data)):
      directors = directors + ","
  MovieDictionary['Director_Name'] = directors[:-1]
  for i, val in enumerate(actor_data):
    actor_list.append(val[0]+ " " +val[1])
    roles_list.append(val[2])
  Actor_details['Actor_Names'] = actor_list
  Actor_details['Roles'] = roles_list
  MovieDictionary['Five_Actors'] = Actor_details
  return MovieDictionary
