import text_desplazado as tdz
import streamlit as st

def create_movie_welcome_page():
    # Set page config
   #  st.set_page_config(page_title="Movie Recommendations", layout="wide")
   #  tdz.title_poster('', 'Welcome to Movie Recommendations!')
    custom_css = """
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/pkaSdxw.png");
        background-size: cover;
    }
    @keyframes rotate {
        from { transform: rotateY(0deg); }
        to { transform: rotateY(360deg); }
    }
    .rotating-logo {
        animation: rotate 5s linear infinite;
        display: inline-block;
    }
    .center-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 60vh;
    }
    </style>
    """

    # HTML content
      #   <h1 style="color: white; text-align: center; margin-bottom: 20px;">Welcome to Movie Recommendations!</h1>
    html_content = f"""
    {custom_css}
    <div class="center-content">
        <div class="rotating-logo">
            <img src="https://i.imgur.com/ravhd3L.png" alt="Cinemio Logo" style="width: 70vw;">
        </div>
    </div>
    """
      #   <h2 style="color: white; text-align: center; margin-top: 20px;">PRESENTA</h2>

    # Render the HTML content
    st.markdown(html_content, unsafe_allow_html=True)

if __name__ == "__main__":
    create_movie_welcome_page()