import tkinter as tk
from tkinter import ttk
from modelo import build_weather_query, get_city_entry




#def vista_principal(ventana):
ventana = tk.Tk()
ventana.title("Clima Mundial")
ventana.config(width=400, height=300)

city_label = ttk.Label(text="Ciudad: ")
city_label.place(x=20, y=20)

city_entry = ttk.Entry()
city_entry.place(x=65, y=20)

city_button = ttk.Button(text='Buscar', command=get_city_entry)

city_button.place (x=200, y=19)

current_weather_label = ttk.Label(text="Clima Actual")
current_weather_label.place(x=62, y=60)

ventana.mainloop()

    # --------------------------------------------------
    # TREEVIEW
    # --------------------------------------------------





