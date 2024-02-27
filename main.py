import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_image(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))

    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommand(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distences = similarity[movie_index]
    movies_list = sorted(list(enumerate(distences)),reverse=True,key = lambda x : x[1])[1:6]

    recommanded_movie = []
    recommaned_poster=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommanded_movie.append(movies.iloc[i[0]].title)
        recommaned_poster.append(fetch_image(movie_id)) # Fetch poster from API
    return recommanded_movie,recommaned_poster

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'What is your taste in movie ? ',
    movies['title'].values)
st.write('You selected:', selected_movie)


if st.button('Recommend movie'):
    name,poster =recommand(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    with col2:
        st.text(name[1])
        st.image(poster[1])
    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])
