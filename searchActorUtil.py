__auther__ = 'Ashish Patil'

def fillSearchActorAPI(first_name, last_name, NumberOfMovie, Movie_Data):
  searchActorDictionary = {}
  movie_dictionary = {}
  movie_list = []
  year_list = []
  roles_list = []
  searchActorDictionary['Actor_First_Name'] = first_name
  searchActorDictionary['Actor_Last_Name'] = last_name
  searchActorDictionary['Number_Of_Movies'] = NumberOfMovie
  for i, val in enumerate(Movie_Data):
    movie_list.append(val[1])
    year_list.append(val[2])
    roles_list.append(val[6])
  movie_dictionary['Movie_Names'] = movie_list
  movie_dictionary['Release_Years'] = year_list
  movie_dictionary['Roles'] = roles_list
  searchActorDictionary['Top_5_Movies'] = movie_dictionary
  return searchActorDictionary



