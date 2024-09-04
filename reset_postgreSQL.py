from sqlalchemy import create_engine, text
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



def borrar_todas_las_filas():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Conexión establecida con éxito!")
            
            # Ejecutar la instrucción SQL para borrar todas las filas
            connection.execute(text("DELETE FROM ratings"))
            # connection.execute(text("DELETE FROM ventas"))
            # connection.execute(text("DELETE FROM new_user_movie"))
            print("¡Todas las filas han sido borradas de la tabla 'new_user_movie'!")
    
    except Exception as e:
        print(f"Error al conectar o al borrar las filas: {str(e)}")


from sqlalchemy import create_engine, inspect

def obtener_nombres_de_tablas():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)

        # Obtener los nombres de todas las tablas en la base de datos
        nombres_de_tablas = inspector.get_table_names()

        if nombres_de_tablas:
            print("Tablas en la base de datos:")
            for nombre in nombres_de_tablas:
                print(nombre)
        else:
            print("No se encontraron tablas en la base de datos.")
    
    except Exception as e:
        print(f"Error al conectar o al obtener los nombres de las tablas: {str(e)}")


from sqlalchemy import create_engine, MetaData

def borrar_todas_las_tablas():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        meta = MetaData()  # No se usa 'bind' aquí
        meta.reflect(bind=engine)  # Se pasa 'engine' al reflejar las tablas

        # Borrar todas las tablas
        meta.drop_all(bind=engine)
        print("¡Todas las tablas han sido eliminadas!")

    except Exception as e:
        print(f"Error al borrar las tablas: {str(e)}")

# crear_conexion()
# borrar_todas_las_tablas()
# borrar_todas_las_filas()
# obtener_nombres_de_tablas()