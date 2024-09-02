import streamlit as st

def title_poster(menu_id, text):
    st.markdown(f"""
    <style>
    @keyframes scroll {{
      0% {{ transform: translateX(100%); }}
      100% {{ transform: translateX(-100%); }}
    }}

    @keyframes shimmer {{
      0% {{ background-position: -1000px 0; }}
      100% {{ background-position: 1000px 0; }}
    }}

    .movie-title {{
      overflow: hidden;
      background: #000;
      padding: 5px 0;
      margin-bottom: 5px;
    }}

    .movie-title-inner {{
      display: inline-block;
      white-space: nowrap;
      animation: scroll 8s linear infinite;
    }}

    .movie-title-text {{
      font-size: 3rem;
      font-weight: bold;
      text-transform: uppercase;
      background: linear-gradient(to right, #8f6B29, #FDE08D, #DF9F28);
      -webkit-background-clip: text;
      color: transparent;
      animation: shimmer 5s infinite linear;
      background-size: 200% 100%;
      padding: 0 20px;
    }}
    </style>

    <div class="movie-title">
      <div class="movie-title-inner">
        <span class="movie-title-text">{text} {menu_id.upper()}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)