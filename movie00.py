import streamlit as st
import hydralit_components as hc
import datetime
import pytz
import time

# Set page config
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# Function to get current time
def get_current_time():
    return datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M:%S")


element_style = '''<style>
#root > div:nth-child(1) > div.withScreencast > div > div > header{
display: none}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5{
padding:0 !important;
}
'''
st.markdown(element_style, unsafe_allow_html=True)
# Define the menu
menu_data = [
    {'icon': "fas fa-film", 'label': "Genres", 'submenu': [
        {'icon': "🎭", 'label': "Drama"},
        {'icon': "🎬", 'label': "Action"},
        {'icon': "🗺️", 'label': "Adventure"},
        {'icon': "💕", 'label': "Romance"},
        {'icon': "🤠", 'label': "Western"},
        {'icon': "🏛️", 'label': "History"},
        {'icon': "👻", 'label': "Horror"},
        {'icon': "🕵️", 'label': "Mystery"},
        {'icon': "😱", 'label': "Thriller"},
        {'icon': "😂", 'label': "Comedy"},
        {'icon': "👪", 'label': "Family"},
        {'icon': "🦹", 'label': "Crime"},
        {'icon': "⚔️", 'label': "War"},
        {'icon': "🚀", 'label': "Sci-Fi"},
        {'icon': "🎵", 'label': "Music"},
        {'icon': "🎭", 'label': "Musical"},
        {'icon': "⚽", 'label': "Sport"},
        {'icon': "📜", 'label': "Biography"},
        {'icon': "🎞️", 'label': "Film-Noir"},
        {'icon': "🧙", 'label': "Fantasy"},
        {'icon': "🎨", 'label': "Animation"},
        {'icon': "🎥", 'label': "Documentary"},
        {'icon': "🔞", 'label': "Adult"},
        {'icon': "📰", 'label': "News"},
        {'icon': "📺", 'label': "Reality-TV"}
    ]},

    {'icon': "fas fa-star", 'label': "Top Rated"},
    {'icon': "fas fa-calendar-alt", 'label': "New Releases"},
    {'icon': "fas fa-users", 'label': "Community"},
]

# Override theme
over_theme = {'txc_inactive': '#FFFFFF'}
over_theme = {'txc_inactive': 'purple','menu_background':'gray','txc_active':'yellow','option_active':'black'}

# Create the navbar
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Login',
    hide_streamlit_markers=True,
    sticky_nav=True,
    # sticky_nav=True,
    sticky_mode='pinned',
)

# Display the time and location in the sidebar
# with st.sidebar:
#     st.write(f"Time: {get_current_time()} EST")
#     st.write("Location: NY, USA")  # Replace with actual location data

# Display the selected menu item
# st.info(f"Selected menu item: {menu_id}")

# Example content based on selection
if menu_id == "Home":
    st.title("Welcome to Movie Recommendations")
    st.write("Discover your next favorite movie!")
elif menu_id == "Genres":
    st.title("Movie Genres")
    st.write("Explore movies by genre")
elif menu_id == "Top Rated":
    st.title("Top Rated Movies")
    st.write("Check out the highest-rated films")
elif menu_id == "New Releases":
    st.title("New Releases")
    st.write("The latest movies to hit the screens")
elif menu_id == "Community":
    st.title("Community")
    st.write("Connect with other movie enthusiasts")
elif menu_id == "Login":
    st.title("Login")
    st.write("Please log in to access personalized recommendations")
else:
    st.title(f"Exploring {menu_id} movies")
    st.write(f"Here are some great {menu_id} movies for you")

placeholder = st.empty()
# Add a placeholder for real-time updates

# Update the time every second


# a dedicated single loader 
# with hc.HyLoader('Now doing loading',hc.Loaders.pulse_bars,):
#     time.sleep(5)

# # for 3 loaders from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[3,0,5]):
#     time.sleep(5)

# # for 1 (index=5) from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=5):
#     time.sleep(5)

# for 4 replications of the same loader (index=2) from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[2,4,2,4,2,2,2,2]):
#     time.sleep(5)    
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[0]):
#     st.subheader('n 0')
#     time.sleep(2)    
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[1]):
#     st.subheader('n 1')
#     time.sleep(2)    
#     st.subheader('n 2')
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[2]):
#     st.subheader('n 3')
#     time.sleep(2)    
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[3]):
#     st.subheader('n 4')
#     time.sleep(2)    
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[4]):
#     st.subheader('n 5')
#     time.sleep(2)    
with hc.HyLoader('Espera un poco',hc.Loaders.standard_loaders,index=[5]):
    time.sleep(2)    


#can apply customisation to almost all the properties of the card, including the progress bar
theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
theme_neutral = {'bgcolor': '#f9f9f9','title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
theme_good = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}


# cc = st.columns(4)

# with cc[0]:
#  # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
#  hc.info_card(title='Some heading GOOD', content='All good!', sentiment='good',bar_value=90)

# with cc[1]:
#  hc.info_card(title='Some BAD BAD', content='This is really bad',bar_value=12,theme_override=theme_bad)

# with cc[2]:
#  hc.info_card(title='Some NEURAL', content='Oh yeah, sure.', sentiment='neutral',bar_value=55)

# with cc[3]:
#  #customise the the theming for a neutral content
#  hc.info_card(title='Some NEURAL',content='Maybe...',key='sec',bar_value=5,theme_override=theme_neutral)



  