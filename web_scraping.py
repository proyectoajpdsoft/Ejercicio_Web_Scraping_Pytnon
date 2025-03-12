from bs4 import BeautifulSoup
import requests

try:
    # Conectamos con el servidor web indicado
    conServidorWeb = None
    conServidorWeb = requests.get("https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/get30dias")
    if conServidorWeb != None:
        # Obtenemos el contenido HTML de la web
        contenidoHTML = None
        contenidoHTML = BeautifulSoup(conServidorWeb.content, "html.parser")
        if contenidoHTML != None and contenidoHTML != "":
            # Buscamos y obtenemos la primera tabla que aparezca en la web (es la única)
            tabla = None
            tabla = contenidoHTML.find("table")
            if tabla != None and tabla != "":
                # Obtenemos todas las fila de la tabla (etiqueta "tr")
                filasTabla = None
                filasTabla = tabla.find_all("tr")
                if filasTabla != None and  filasTabla != "":
                    # Definimos el diccionario que contendrá las columnas de Evento y Magnitud
                    eventos_magnitudes = {}
                    for filaActual in filasTabla:
                        # Obtenemos todas las columnas de la tabla (etiqueta "td")
                        columnas = filaActual.find_all("td")
                        # Si ha encontrado una columna o más
                        if len(columnas) >= 1:
                            # Obtenemos la primera columna, que es la de Evento
                            evento = columnas[0].get_text()
                            # Obtenemos la columna 7, que es la de Magnitud
                            magnitud = columnas[6].get_text()
                            # Guardamos en el diccionario los valores obtenidos
                            eventos_magnitudes[evento] = magnitud

                    # Mostramos el resultado formateado en columnas
                    print (f"{"EVENTO":18}MAGNITUD")
                    for evento, magnitud in eventos_magnitudes.items():
                        print (f"{evento:18}{magnitud}")
                else:
                    print("No se ha obtenido columna en la tabla")
            else:
                print("No se ha obtenido ninguna tabla")
        else:
            print("No se ha obtenido información HTML de la web")
    else:
        print("No se ha podido conectar con el servidor web")
except Exception as e:
    print(f"Error al conectar al servidor web: {e}")
finally:
    # Cerramos la conexión con el servidor
    if conServidorWeb != None:
        conServidorWeb.close