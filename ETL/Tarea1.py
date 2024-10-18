import pandas as pd
import numpy as np

# Cargar el DataFrame
df = pd.read_excel('Terrazas_202104.xlsx')

# Mostrar cuántos valores nulos tiene cada columna
print(df.isnull().sum())

################# elimina los registros que contengan valores nulos en más del 50% de sus columnas #################################

# Calcular el umbral de valores no nulos
# Si una fila tiene menos del 50% de valores no nulos, se eliminará
umbral = len(df.columns) * 0.5

# Eliminar filas que tienen más del 50% de valores nulos
filtrado_df = df.dropna(thresh=umbral + 1)

# Calcular el número de registros eliminados
registros_eliminados = len(df) - len(filtrado_df)

# Mostrar el DataFrame filtrado y el número de registros eliminados
print("\nDataFrame filtrado:")
print(filtrado_df)
print(f"\nNúmero de registros eliminados: {registros_eliminados}")

######################################### convertir  a formato de hora @########################################################################################################### 

df['hora_ini_LJ_es'] = pd.to_datetime(df['hora_ini_LJ_es'], errors='coerce')
df['hora_fin_LJ_es'] = pd.to_datetime(df['hora_fin_LJ_es'], errors='coerce')
df['hora_ini_LJ_ra'] = pd.to_datetime(df['hora_ini_LJ_ra'], errors='coerce')
df['hora_fin_LJ_ra'] = pd.to_datetime(df['hora_fin_LJ_ra'], errors='coerce')
df['hora_ini_VS_es'] = pd.to_datetime(df['hora_ini_VS_es'], errors='coerce')
df['hora_fin_VS_es'] = pd.to_datetime(df['hora_fin_VS_es'], errors='coerce')
df['hora_ini_VS_ra'] = pd.to_datetime(df['hora_ini_VS_ra'], errors='coerce')
df['hora_fin_VS_ra'] = pd.to_datetime(df['hora_fin_VS_ra'], errors='coerce')

# Convertir la columna 'sillas_ra' a tipo numérico
df['sillas_ra'] = pd.to_numeric(df['sillas_ra'], errors='coerce')

# Imprimir el tipo de dato de cada una de las columnas
print("Tipos de datos de cada columna:")
print(df.dtypes)

# Crear una nueva columna que calcule el ratio entre "Superficie_TO" y "id_terraza"
df['Superficie_TO'] =  df['Superficie_ES'] + df['Superficie_RA']
df['Ratio'] = df['Superficie_TO'] / df['id_terraza']

print(df['Ratio'])

df.to_excel('Terrazas_Normalizadas.xlsx')