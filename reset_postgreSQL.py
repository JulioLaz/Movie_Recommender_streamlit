from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

def crear_conexion():
    df = pd.read_csv('user_ratings.csv', names=['userId', 'movieId', 'title', 'rating', 'timestamp'], header=0)
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Conexión establecida con éxito!")
        df.columns = ['userId', 'movieId', 'title', 'rating', 'timestamp']
        df.to_sql('ratings', engine, if_exists='append', index=False)

        print("¡Datos guardados en la base de datos!")
    except Exception as e:
        print(f"Error al conectar o guardar los datos: {str(e)}")

crear_conexion()