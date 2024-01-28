import pickle  
import streamlit as st  # creating the web application
import pandas as pd  
import requests  # For making HTTP requests

# Function to add custom CSS for the background
def change_background_color():
    st.markdown("""
        <style>
        .stApp {
            background-color: lightgreen;  
        }
        </style>
        """, unsafe_allow_html=True)

# Calling the function to change the background color
change_background_color()

# heading 
st.header('Movies Recommendation')

# Function to fetch movie posters from an external API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function for movie recommendations
def recommendation(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]]['title'])
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

# Loading movie data and similarity matrix from pickled files
all_movies = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(all_movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown box for the user to choose a movie
select_movie_names = st.selectbox("Which movie do you want a recommendation for?", movies['title'].values)

# Recommend button
if st.button('Recommend'):
    recommended_movies, recommended_movie_posters = recommendation(select_movie_names)
    
    cols = st.columns(5)  # Creating 5 columns for recommendations
    for i in range(5):
        with cols[i]:  
            st.text(recommended_movies[i])
            st.image(recommended_movie_posters[i], width=120)  
            st.write("\n")  # Adding spacing after each movie
