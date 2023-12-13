import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from babel.numbers import format_currency

sns.set(style="dark")

# netflix information movies
def informasi_tipe_netflix(df):
    informasi_data = df['type'].value_counts()
    
    return informasi_data

def sutradara_jumlah_movie(df):
    sutradara_movie = df.loc[df['type'] == 'Movie', 'director'].value_counts().head(10)
    
    return sutradara_movie

def negara_terbanyak_netflix(df):
    movie_df = df[df['type'] == 'Movie']
    tv_show_df = df[df['type'] == 'TV Show']
    
    negara_terbanyak_movie = movie_df['country'].value_counts().head(10)
    negara_terbanyak_tv_show = tv_show_df['country'].value_counts().head(10)
    
    return negara_terbanyak_movie, negara_terbanyak_tv_show

def season_Tv_netflix(df):
    season_tv = df.loc[df['type'] == 'TV Show', ['duration']].value_counts().head(10)
    
    return season_tv

def season_movie_netflix(df):
    season_movie = df.loc[df['type'] == 'Movie', ['duration']].value_counts().head(10)
    
    return season_movie

def rating_populer_netflix(df):
    rating_tv = df.loc[df['type'] == 'TV Show', 'rating'].value_counts()
    rating_movie = df.loc[df['type'] == 'Movie', 'rating'].value_counts()
    
    return rating_movie, rating_tv

def netflix_per_month(df):
    df['month_added'] = pd.to_datetime(df['date_added'], errors='coerce') 
    df['month_added'] = df['month_added'].dt.strftime('%B')
    perbulan = df.groupby(['type', 'month_added'])['title'].count().reset_index(name="count")
    
    return perbulan


data = pd.read_csv("NetflixDataset.csv")

#set tanggal dari sampe kapan
datetime_columns = ["date_added", "date_added"]
data.sort_values(by="date_added", inplace=True)
data.reset_index(inplace=True)

for column in datetime_columns:
    data[column] = pd.to_datetime(data[column])

min_date = data["date_added"].min()
max_date = data["date_added"].max()    

with st.sidebar:
    start_date, end_date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
        )
    
    options = st.multiselect('Hasil Analisis Bisnis :',
                             ['Country that makes films and TV shows', 'Directors by number of films made', 'Movies And TV Show', 'Movies with the most seasons', 'Number of Movies and TV Shows Added', 'Ratings for Movies on Netflix', 'Ratings for TV Shows on Netflix', 'TV shows with the most seasons'
                            ])

main_df = data[
    (data["date_added"] >= str(start_date)) & (data["date_added"] <= str(end_date))
]

informasi_data = informasi_tipe_netflix(main_df)
sutradara_movie = sutradara_jumlah_movie(main_df)
negara_terbanyak_movie, negara_terbanyak_tv_show = negara_terbanyak_netflix(main_df)
season_tv = season_Tv_netflix(main_df)
season_movie = season_movie_netflix(main_df)
rating_movie, rating_tv = rating_populer_netflix(main_df)
perbulan = netflix_per_month(main_df)
#sampe sini code tanggal

if not options:
    st.markdown(
        """
        <h1 style="text-align: center;">Netflix Movies and TV Shows Analyze Dashboard</h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <h4 style="text-align: center;">The results of the analysis of Netflix Movies and TV Shows</h4>
    """,
    unsafe_allow_html=True
    )

else:
    for option in options:

        if option == 'Movies And TV Show':
            # code movies and tv show
            st.subheader("Netflix Movies And TV Show")
            col1, col2 = st.columns(2)
            with col1:
                movie_count = informasi_data.get('Movie', 0)
                st.metric("Total Movie", value=movie_count)

            with col2:
                tv_count = informasi_data.get('TV Show', 0)
                st.metric("Total TV Show", value=tv_count)

            fig, ax = plt.subplots(figsize=(8, 6))
            informasi_data.plot(kind='bar', rot=0, ax=ax)
            ax.set_title('Netflix Movies And TV Show')
            ax.set_xlabel('Type')
            ax.set_ylabel('Total')

            st.pyplot(fig)
            # end movies and tv show

        elif option == 'Directors by number of films made':
            #10 sutradara teratas berdasarkan jumlah film yang dibuat
            st.subheader("Directors by number of films made")
            fig, ax = plt.subplots(figsize=(8, 6))
            sutradara_movie.plot(kind='bar', x='index', y='director', rot=45, ax=ax,color='red')
            ax.set_title('Directors by number of films made')
            ax.set_xlabel('Director')
            ax.set_ylabel('Total')

            st.pyplot(fig)
            # end 

        elif option == 'Country that makes films and TV shows':
            # Start
            st.subheader("Countries with Most Movies and TV Shows on Netflix")
            fig, ax = plt.subplots(figsize=(14, 6))

            negara_terbanyak_movie.plot(kind='bar', position=0, width=0.4, color='skyblue', ax=ax, label='Movies')

            negara_terbanyak_tv_show.plot(kind='bar', position=1, width=0.4, color='orange', ax=ax, label='TV Shows')

            ax.set_title('Countries with Most Movies and TV Shows on Netflix')
            ax.set_xlabel('Country')
            ax.set_ylabel('Number of Titles')
            ax.legend()

            st.pyplot(fig)

            fig, ax = plt.subplots(figsize=(14, 6))

            negara_terbanyak_movie.plot(kind='line', x='Country', y='Movies', marker='o', color='skyblue', linestyle='-', linewidth=2, ax=ax, label='Movies')

            negara_terbanyak_tv_show.plot(kind='line', x='Country', y='TV Shows', marker='o', color='orange', linestyle='-', linewidth=2, ax=ax, label='TV Shows')

            ax.set_title('Countries with Most Movies and TV Shows on Netflix')
            ax.set_xlabel('Country')
            ax.set_ylabel('Number of Titles')
            ax.legend()

            st.pyplot(fig)
            #End

        elif option == 'Movies with the most seasons':
            #Movie with the most seasons
            st.subheader("Movies with the most seasons")
            fig, ax = plt.subplots(figsize=(8, 6))
            season_movie.plot(kind='line', x='index', y='duration', marker='o' ,rot=45, ax=ax,color='green')
            ax.set_title('Movies with the most seasons')
            ax.set_xlabel('Season')
            ax.set_ylabel('Total')

            st.pyplot(fig)
            # end 

        elif option == 'TV shows with the most seasons':
            #TV shows with the most seasons
            st.subheader("TV shows with the most seasons")
            fig, ax = plt.subplots(figsize=(8, 6))
            season_tv.plot(kind='line', x='index', y='duration', rot=45, ax=ax, marker='o',color='yellow')
            ax.set_title('TV shows with the most seasons')
            ax.set_xlabel('Season')
            ax.set_ylabel('Total')

            st.pyplot(fig)
            # end 

        elif option == 'Ratings for Movies on Netflix':
            #start diagram pie rating movie
            st.subheader("Ratings for Movies on Netflix")

            top_rating_movies = rating_movie.head(5)
            other_ratings_count = rating_movie.sum() - top_rating_movies.sum()

            top_rating_movies['Others'] = other_ratings_count

            fig, ax = plt.subplots(figsize=(8, 8))

            ax.pie(top_rating_movies, labels=top_rating_movies.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

            ax.set_title('Ratings for Movies on Netflix')

            st.pyplot(fig)
            #end

        elif option == 'Ratings for TV Shows on Netflix':
            #start diagram pie rating tv
            st.subheader("Ratings for TV Shows on Netflix")

            top_ratings_tv_show = rating_tv.head(5)
            other_ratings_count = rating_tv.sum() - top_ratings_tv_show.sum()

            top_ratings_tv_show['Others'] = other_ratings_count

            fig, ax = plt.subplots(figsize=(8, 8))

            ax.pie(top_ratings_tv_show, labels=top_ratings_tv_show.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

            ax.set_title('Ratings for TV Shows on Netflix')

            st.pyplot(fig)
            #end pie Tv

        elif option == 'Number of Movies and TV Shows Added':
            st.subheader("Number of Movies and TV Shows Added Every Month")
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x='month_added', y='count', hue='type', data=perbulan)
            plt.title('Number of Movies and TV Shows Added Every Month')
            plt.xlabel('Per Month')
            plt.ylabel('Total')
            st.pyplot(fig)
            
st.caption("Copyright (c) Muhammad Fikri Ramadhan")