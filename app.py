import pickle
import streamlit as st
import requests
from urllib.parse import quote


# PAGE CONFIG

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)



# FETCH MOVIE POSTER FROM OMDb 

def fetch_poster(movie_title):
    api_key = st.secrets["OMDB_API_KEY"]

    url = "https://www.omdbapi.com/?apikey={}&t={}".format(
        api_key,
        quote(movie_title)
    )

    response = requests.get(url)
    data = response.json()

    if data["Response"] == "True":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/300x450?text=No+Poster"



# RECOMMENDATION FUNCTION  

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_title = movies.iloc[i[0]].title

        recommended_movie_names.append(movie_title)

        recommended_movie_posters.append(
            fetch_poster(movie_title)
        )

    return recommended_movie_names, recommended_movie_posters


# SIDEBAR

with st.sidebar:
    st.title("🎬 Movie Recommender")
    st.divider()

    st.caption("📁 Project")
    st.write("Movie Recommendation System")

    st.caption("🎞️ Dataset")
    st.write("TMDB 5000 Movies")

    st.caption("🧠 Recommendation Type")
    st.write("Content-Based Filtering")

    st.caption("⚙️ Algorithm")
    st.write("CountVectorizer")

    st.caption("📐 Similarity")
    st.write("Cosine Similarity")

    st.divider()
    st.caption("👨‍💻 Developer")
    st.write("Revesh Rathod")
    st.link_button("GitHub Profile", "https://github.com/reveshrathod005", use_container_width=True)


# HERO SECTION

st.title("🎬 Movie Recommendation System")
st.subheader("Discover your next favorite movie using Machine Learning and Content-Based Recommendation.")
st.divider()


# LOAD DATA 

movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies["title"].values


# SEARCH SECTION

search_col1, search_col2, search_col3 = st.columns([1, 2, 1])

with search_col2:
    selected_movie = st.selectbox(
        "🔍 Search for a movie",
        movie_list,
    )
    recommend_clicked = st.button(
        "🎥 Recommend Movies",
        type="primary",
        use_container_width=True,
    )

# RECOMMENDATION RESULTS

if recommend_clicked:

    with st.spinner("🎬 Finding Similar Movies..."):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.divider()
    st.header("✨ Recommended For You")

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        name = recommended_movie_names[idx]
        poster = recommended_movie_posters[idx]

        with col:
            with st.container(border=True):
                st.image(poster, use_container_width=True)
                st.markdown(f"**{name}**")


# FOOTER

st.divider()
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.caption("Built with 🐍 Python · Streamlit · Scikit-learn · OMDb API")
with footer_col2:
    st.caption("Designed by **Revesh Rathod**")