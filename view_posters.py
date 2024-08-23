import populares as pop
import requests
from io import BytesIO
import streamlit as st
from PIL import Image
import video

def view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating):

      def load_image_from_url(url):
         response = requests.get(f"https://image.tmdb.org/t/p/w500{url}")
         img = Image.open(BytesIO(response.content))
         img = img.resize((500, 800))  # Redimensionar a 3rem (1rem = 16px)
         return img    
      cols = st.columns(5)
      for i in range(5):
         with cols[i]:
               try:
                  image = load_image_from_url(lista_poster[i])
                  st.image(image, use_column_width=True)
                  st.markdown(
                     f"""
                     <div style="background-color:black;color:red;padding:0px;text-align:center;font-size:calc(12px + .1vw)">
                           {lista_originalTitle[i][:20] + "..." if len(lista_originalTitle[i]) > 25 else lista_originalTitle[i]}
                     </div>
                     """, unsafe_allow_html=True
                  )                
                  st.markdown(
                     f"""
                     <div style="display:flex; justify-content: space-evenly">
                           <div style="background-color:black;color:white;padding:0px;text-align:center;font-size:20px;font-weight:bold">
                           {lista_averageRating[i]}
                           </div>
                           <div style="background-color:black;color:black;padding:0px;text-align:end;font-size:calc(10px + .1vw)">
                              {"⭐" * min(int(lista_averageRating[i]), 5)}<br>
                              {"⭐" * (int(lista_averageRating[i]) - 5) if int(lista_averageRating[i]) > 5 else "."}
                           </div>
                     </div>
                     """, unsafe_allow_html=True
                  )
               
                  if st.button('To watch a traile', key=f'btn_{i}'):
                     video.open_and_click(lista_tconst[i])
               except IndexError:
                  st.error(f"Index {i} out of range for the title list.")
               except Exception as e:
                  st.markdown(
                     f"""
                     <div style="background-color:black;color:white;padding:20px;text-align:center;">
                           <b>{lista_originalTitle[i]}</b>
                     </div>
                     """, unsafe_allow_html=True
                  )
      # st.title("Top Rated Movies")
      # st.write("Check out the highest-rated films")

def title_poster_genre(menu_id):
    st.markdown(f"""
    <div> <p style="
        background-color:none;
        color:gold;
        padding:0px;
        text-align:center;
        font-size:2rem;
        animation: pulse 1.5s infinite;
        ">
        <b>Movie Posters {menu_id.upper()} Top 5</b>
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