import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=29a4ed4c4c87e26e776374706753dfb9&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path='https://image.tmdb.org/t/p/w500/'+poster_path
    return full_path

def rcd(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fatch poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster



st.title('Movie recommender system')
selected_movie=st.selectbox(
    'Select Movie',
    movies['title'].values

)

import streamlit as st

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = rcd(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])


    with col2:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

    with col3:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col4:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col5:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])