__auther__ = 'Ashish Patil'

def fillSearchDirectorAPI(first_name,last_name,number_of_movies,movie_data):
  SearchDirector_Dict = {}
  movie_dict = {}
  movie_list = []
  year_list = []
  SearchDirector_Dict['Director_First_Name'] = first_name
  SearchDirector_Dict['Director_Last_Name'] = last_name
  SearchDirector_Dict['Number_Of_Movies'] = number_of_movies
  for i , val in enumerate(movie_data):
    movie_list.append(val[1])
    year_list.append(val[2])
  movie_dict['Movie_Names'] = movie_list
  movie_dict['Release_Years'] = year_list
  SearchDirector_Dict['Top_5_Movies'] = movie_dict
  return SearchDirector_Dict
