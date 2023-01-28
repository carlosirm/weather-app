import sqlite3


def conexion():
    con = sqlite3.connect("weatherdb.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS clima
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             fecha numeric ,
             ciudad text,
             temperatura real ,
             velocidad_viento int)
    """
    cursor.execute(sql)
    con.commit()
    print("la tabla fue creada")

try:
    conexion()
    crear_tabla()
except:
    print("Hay un error")


def alta():
    data= ("2023/01/05", "caracas", 20, 30)
    con=conexion()
    cursor=con.cursor()
    sql="INSERT INTO clima(fecha, ciudad,temperatura, velocidad_viento) VALUES(?, ?, ?, ?,?)"
    cursor.execute(sql, data)
    con.commit()



def consultar():
    sql = "SELECT * FROM clima"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        


conexion()
crear_tabla()
#alta()
consultar()