import sqlite3


def make_connection():
    con = sqlite3.connect("weatherdb.db")
    return con

def create_table():
    con = make_connection()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS clima
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             fecha text ,
             ciudad text,
             temperatura text ,
             velocidad_viento text)
    """
    cursor.execute(sql)
    con.commit()
    print("la tabla fue creada")




def insert_data(data:tuple):
    con=make_connection()
    cursor=con.cursor()
    # data_db = (weather_data["current_time"], weather_data["location"],weather_data["temperature"], weather_data["wind_info"])
    sql="INSERT INTO clima(fecha, ciudad,temperatura, velocidad_viento) VALUES(?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()



def request_data_table():
    sql = "SELECT * FROM clima"
    con=make_connection()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    return resultado
        
