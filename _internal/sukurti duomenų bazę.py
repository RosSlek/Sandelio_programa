import psycopg2
from psycopg2 import sql

def kurti_duomenu_baze():
    try:
        duomenys = open("duomenu baze.txt", "r")
        duomenu_baze = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        user = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        password = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        host = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        port = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        duomenys.close()

        conn = psycopg2.connect(database="postgres", user=user, password=password, host=host, port= port)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql.SQL("CREATE DATABASE{}").format(sql.Identifier(duomenu_baze)))
        print("Database created successfully!")

        conn.close()

        conn = psycopg2.connect(database=duomenu_baze, user='postgres', password='PGadmin', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()

        sandelio_istorija = '''CREATE TABLE SANDELIO_ISTORIJA(Polietileno_plėvelė_0_85x50m CHAR(20), Hidroizoliacinė_plėvelė_0_65x45m CHAR(20), Sausas_tinko_mišinys_2_5kg CHAR(20), Cementinis_mišinys_4kg CHAR(20), Partijos_numeris CHAR(20), Atsakingas_asmuo CHAR(30), Data CHAR(30), Papildoma_informacija CHAR(100))'''
        gamybos_istorija = '''CREATE TABLE GAMYBOS_ISTORIJA(Polietileno_plėvelė_m CHAR(20), Hidroizoliacinė_plėvelė_m CHAR(20), Sausas_tinko_mišinys_kg CHAR(20), Cementinis_mišinys_kg CHAR(20), Partijos_numeris CHAR(20), Medžiagos_ID CHAR(20), Atsakingas_asmuo CHAR(30), Data CHAR(30), Papildoma_informacija CHAR(100))'''
        gamybos_darbu_registras = '''CREATE TABLE GAMYBOS_DARBU_REGISTRAS(Užsakymo_numeris CHAR(20), Polietileno_plėvelė_m CHAR(20), Hidroizoliacinė_plėvelė_m CHAR(20), Sausas_tinko_mišinys_kg CHAR(20), Cementinis_mišinys_kg CHAR(20), Medžiagos_ID CHAR(20), Atsakingas_asmuo CHAR(30), Data CHAR(30), Papildoma_informacija CHAR(100))'''

        cursor.execute(sandelio_istorija)
        cursor.execute(gamybos_istorija)
        cursor.execute(gamybos_darbu_registras)

        print("Tables created successfully!")
        conn.commit()
        conn.close()

    except psycopg2.Error as e:
        print(f"An error occurred while creating the database: {e}")

kurti_duomenu_baze()