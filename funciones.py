# LIBRERÍAS
import pandas as pd
import pathlib as path
import requests

# FUNCIONES PARA DESEMPEÑAR LA NECESIDAD DEL CLIENTE:

def API_frankfurter(url):
    # Extraccion de la informacion de la API que nos detallan. 
    # La funcion comprueba que la variable url sea un string para seguir con el proceso.
    # En el caso de que es string:
    # 1. Nos imprime el estado del código si da un error podemos identificar el fallo. 
    # 2. Comprobamos que nuestras keys sean correctas por si da un error debido a que hayan actualizado las keys de la página web. 
    # 3. Pasamos a un Dataframe los datos obtenidos.


    if isinstance(url,str):
        try:
            response = requests.get(url,timeout=15) # Tiene un tiempo de 15 segundos para obtener la informacion, 
                                                    # si no responde, considero que la API ha fallado.
            print(f'Estado del script: {response.status_code}') # 1

            data = response.json()

            print(f'keys: {data.keys()}') # 2

            df = pd.DataFrame(data) # 3

            return df
        except requests.exceptions.RequestException as error:
            print(f"ERROR al consultar la API: {error}")
            return None

    else: # En el caso de que no sea la url un string:
        print('La url introducida no es tipo string, porfavor verificalo')

def variacion(df):
    # Creacion de una nueva columna que nos permite calcular la variacion que existe del día actual con el anterior.
    # Nos devuelve de nuevo el dataframe pero con la nueva columna calculada.
    df['change_pct'] = 0.00
    
    for i in range(len(df)):
        valor_actual = df['rate'].iloc[i]
        valor_anterior = df['rate'].iloc[i - 1]
        if i != 0: 
            df.loc[i,'change_pct'] = round(((valor_actual -  valor_anterior) / valor_anterior) * 100,2)
        
    return df

def tratamiento_df(df):
    # Tratamiento de nuestros datos, en esta funcion comprobamos que todo esté correcto,
    # en el caso de que no lo sea, saltan el error descrito
    # Comprobamos si existe un archivo CSV previo, si no existe lo crea y en el caso de que exista adjunta los nuevos datos.
    # La función siempre mostrará los resultados del último día añadido.

    cols_interes = ['date','rate','change_pct']
    csv_path = path.Path('data/tipo_cambio_EUR_USD.csv')
    if isinstance(df,pd.DataFrame): #1
        df = df.rename(columns={'rates' : 'rate'})
        if not csv_path.exists(): 
            #df['date'] = pd.to_datetime(df['date']) - CASO DE QUE QUERAMOS PASAR LA FECHA A TIPO DATETIME.

            df = variacion(df)

            df[cols_interes].to_csv('data/tipo_cambio_EUR_USD.csv',index=False)
            

            print(f'''No existe un archivo CSV previo, se ha creado uno nuevo llamado "tipo_cambio_EUR_USD.csv".\n
                Los resultados obtenidos son los siguientes:\n
                [date],rate,change_pct\n
                [{df['date'].iloc[-1]}],{df['rate'].iloc[-1]},{df['change_pct'].iloc[-1]}%''')
        else:
            df_past = pd.read_csv('data/tipo_cambio_EUR_USD.csv')

            if df["date"].iloc[0] in df_past["date"].values:
                print("Ya existe un registro para esta fecha. No se añade una fila duplicada.")
            else:
                df_new = pd.concat([df_past, df], ignore_index=True)

                #df_new['date'] = pd.to_datetime(df_new['date']) - CASO DE QUE QUERAMOS PASAR LA FECHA A TIPO DATETIME.

                df_new = variacion(df_new)

                df_new[cols_interes].to_csv('data/tipo_cambio_EUR_USD.csv',index=False)

                print(f'''Adjuntando los nuevo datos al archivo "tipo_cambio_EUR_USD.csv"\n
                    Los resultados obtenidos son los siguientes:\n
                    [date],rate,change_pct\n
                    [{df_new['date'].iloc[-1]}],{df_new['rate'].iloc[-1]},{df_new['change_pct'].iloc[-1]}%''')

    
    else:
        print('ERROR #1: No se ha pasado en la primera variable un tipo pd.DataFrame, porfavor vuelva a revisarlo')


def frankfurter_wrapper():
    # Funcion que automatiza todo el proceso, llamando las otras funciones.
    # Esto nos permitirá que en el notabook principal quede un codigo limpio.
    url = "https://api.frankfurter.dev/v1/latest?from=EUR&to=USD"
    df = API_frankfurter(url)
    
    if df is not None:
        tratamiento_df(df)
    else:
        print("El proceso ha finalizado sin actualizar el histórico.")
    