import requests
from io import BytesIO
import streamlit as st
from PIL import Image
import star_score_rating as ssr
import ddbb
# load_dotenv()  # Carga las variables del archivo .env
# API_KEY = os.getenv("KEY")
API_KEY = st.secrets["KEY"]

df_links=ddbb.load_df_links()

@st.cache_data(ttl=300)
def obtener_info_pelicula(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["Response"] == "True":
        return {
            "titulo": data["Title"],
            "descripcion": data["Plot"],
            "poster_url": data["Poster"],
            "director": data["Director"],
            "Actors": data["Actors"],
            "Runtime": data["Runtime"],
            "Awards": data["Awards"],
            "Released": data["Released"],
            "BoxOffice": data["BoxOffice"],
        }
    else:
        return None

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def view_movie_details(imdb_id):
    movieId=df_links[df_links['imdbId']==imdb_id]['movieId']
    movieId=movieId.values[0]
    details = obtener_info_pelicula(imdb_id)
    if details:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(load_image_from_url(details["poster_url"]), use_column_width=True)
        with col2:
            st.title(details["titulo"])
            st.write(f"📅 **Año:** {details['Released']}")
            st.write(f"🎬 **Director:** {details['director']}")
            st.write(f"🎭 **Actor:** {details['Actors']}")
            st.write(f"⏱️ **Duración:** {details['Runtime']}")
            st.write(f"🏅 **Premios:** {details['Awards']}") 
            st.write(f"💰 **Box Office:** {details['BoxOffice']}")
           
        st.subheader("**Descripción:**")
        st.write(details['descripcion'])
        # st.write(type(movieId))
    else:
        st.sidebar.error("No se pudo obtener la información de la película.")
    ssr.rate_with_stars(movieId)
        # Star rating section
      #   st.write("**Rate this movie:**")
        
   #    #   rating = st.slider("Select your rating:", min_value=1, max_value=5, value=3)
   #      rating=3
   #      # Display stars based on selected rating
   #      star_full = Image.open('img/star.png')
   #      star_empty = Image.open('img/star-solid.png')
   #      for i in range(1, 6):
   #          if i <= rating:
   #              st.image(star_full, width=30)
   #          else:
   #              st.image(star_empty, width=30)

   #      st.write(f"Your rating: {rating} stars")            
   #  else:
   #      st.error("No se pudo obtener la información de la película.")

def view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating):
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            try:
                image = load_image_from_url(f"https://image.tmdb.org/t/p/w500{lista_poster[i]}")
                st.image(image, use_column_width=True)
                st.markdown(
                    f"""
                    <div style="background-color:#0e1117;color:red;padding:2px 0px;text-align:center;font-size:calc(12px + .1vw);height:2rem;box-sizing:unset">
                        {lista_originalTitle[i][:17] + "..." if len(lista_originalTitle[i]) > 22 else lista_originalTitle[i]}
                    </div>
                    """, unsafe_allow_html=True
                )
                
                st.markdown(
                    f"""
                    <div style="display:flex; justify-content: center;height:1.9rem;margin-bottom:15px;margin-top:3px;">
                        <div style="background-color:#0e1117;color:white;padding:0px;text-align:center;font-size:20px;font-weight:bold">
                        <span style="font-size:10px; padding-right:3px">rating</span>{lista_averageRating[i]}
                        </div>
                        <div style="background-color:#0e1117;color:#0e1117;padding:0px;text-align:end;font-size:calc(10px + .1vw)">
                            {"⭐" * min(int(float(lista_averageRating[i])), 5)}<br>
                            {"⭐" * (int(float(lista_averageRating[i])) - 5) if int(float(lista_averageRating[i])) > 5 else "."}
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )

                # def open_imdb_video(url):
                    # url = f"https://www.imdb.com/title/{tt}/"
                    # webbrowser.open_new_tab(url)

                col1,col2=st.columns(2)
                with col1:
                  if st.button('Trailer', key=f'btn_trailer_{i}'):
                    #  if st.button("Cargar Video"):
                            video_url = f"https://www.imdb.com/title/{lista_tconst[i]}/"
                            # if video_url:
                            st.write(f"[Ver en imbd]({video_url})")
                            # open_imdb_video(video_url)

                            # video.open_and_click(lista_tconst[i])
                with col2:
                  if st.button('Details', key=f'btn_details_{i}'):
                     st.session_state.show_details = lista_tconst[i]
                    #  st.rerun()
            except IndexError:
                st.error(f"Index {i} out of range for the title list.")
            except Exception as e:
                st.error(f"Error: {e}")
    
    if 'show_details' in st.session_state:
        st.sidebar.empty()
        with st.sidebar:
            st.sidebar.markdown(
                """
                <style>
                    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                        width: 40vw;
                     background-color:red;
                    }
                    /* wihdt sidebar */
                    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1i4v8s7.eczjsme18{
                     max-width: none !important;
                     width:40vw !important
                     }
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11{
                     max-width: none !important;
                     width:40vw !important                     }
                     /* sidebar */
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-16txtl3.eczjsme4{
                     padding: 1.5rem 1.5rem;}
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-16txtl3.eczjsme4 > div > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div > div > div > h1{
                     padding-top:0 !important;}
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-16txtl3.eczjsme4 > div > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(2) > div > div > div > div:nth-child(7) > div > div > p{
                     margin:0 !important}


                """,
                unsafe_allow_html=True,
            )
            view_movie_details(st.session_state.show_details)

def title_poster_genre(menu_id,text):
    st.markdown(f"""
    <div> <p style="
        background-color:none;
        color:gold;
        padding:0px;
        text-align:center;
        font-size:2rem;
        animation: pulse 1.5s infinite;
        ">
        <b>{text} {menu_id.upper()}</b>
        </p>
    </div>
    
    <style>
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
    """, unsafe_allow_html=True)