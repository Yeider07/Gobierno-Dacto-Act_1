import pandas as pd


# URL del archivo CSV en GitHub
url = 'https://raw.githubusercontent.com/Yeider07/Gobierno-Dacto-Act_1/refs/heads/main/DevOps_0/Licencias_Terrazas_Integradas.csv'

datos = pd.read_csv(url)
print("Datos cargados exitosamente:")

################# elimina los registros que contengan valores nulos en más del 50% de sus columnas #################################

# Si una fila tiene menos del 50% de valores no nulos, se eliminará
umbral = len(datos.columns) * 0.5

# Eliminar filas que tienen más del 50% de valores nulos
filtrado_df = datos.dropna(thresh=umbral + 1)

# Calcular el número de registros eliminados
registros_eliminados = len(datos) - len(filtrado_df)

# Mostrar cuántos valores nulos tiene cada columna
print(datos.isnull().sum())
# número de registros eliminados
print(f"\nNúmero de registros eliminados: {registros_eliminados}")

########################## Detección y Eliminación de Duplicados ##############################################################

# Número de registros antes de eliminar duplicados
Contar_Original = len(datos)
print(f'Cantidad de registros: {Contar_Original}')

# Identificar y eliminar duplicados basados en las columnas 'id_local' y 'ref_licencia'
Licencias_SinDuplicados = datos.drop_duplicates(subset=['id_local', 'ref_licencia'])

# Número de registros después de eliminar duplicados
Contar = len(Licencias_SinDuplicados)

# Imprimir la cantidad de registros eliminados
print(f"Registros eliminados: {Contar_Original - Contar}")

################# Transformar columnas al formato correcto ########################################

datos['hora_ini_LJ_es'] = pd.to_datetime(datos['hora_ini_LJ_es'], errors='coerce')
datos['hora_fin_LJ_es'] = pd.to_datetime(datos['hora_fin_LJ_es'], errors='coerce')
datos['hora_ini_LJ_ra'] = pd.to_datetime(datos['hora_ini_LJ_ra'], errors='coerce')
datos['hora_fin_LJ_ra'] = pd.to_datetime(datos['hora_fin_LJ_ra'], errors='coerce')
datos['hora_ini_VS_es'] = pd.to_datetime(datos['hora_ini_VS_es'], errors='coerce')
datos['hora_fin_VS_es'] = pd.to_datetime(datos['hora_fin_VS_es'], errors='coerce')
datos['hora_ini_VS_ra'] = pd.to_datetime(datos['hora_ini_VS_ra'], errors='coerce')
datos['hora_fin_VS_ra'] = pd.to_datetime(datos['hora_fin_VS_ra'], errors='coerce')

# Convertir la columna 'sillas_ra' a tipo numérico
datos['sillas_ra'] = pd.to_numeric(datos['sillas_ra'], errors='coerce')

# Imprimir el tipo de dato de cada una de las columnas
print("Tipos de datos de cada columna:")
print(datos.dtypes)

# Crear una nueva columna que calcule el ratio entre "Superficie_TO" y "id_terraza"
datos['Superficie_TO'] =  datos['Superficie_ES'] + datos['Superficie_RA']
datos['Ratio'] = datos['Superficie_TO'] / datos['id_terraza']

########################## Eliminar columnas no deseadas #############################################

# Identificar columnas que terminan en '_x'
columnas_eliminadas = datos.columns[datos.columns.str.endswith('_x')]

# Eliminar columnas que terminan en '_x'
datos = datos.loc[:, ~datos.columns.str.endswith('_x')]

# Imprimir las columnas eliminadas
print("Columnas eliminadas:")
print(columnas_eliminadas)

# Eliminar la columna que tiene un nombre en blanco
datos = datos.loc[:, datos.columns != '']

################################# Guardar los datos ##########################
datos.to_csv('DataTerrazas.csv')



################### Importar el archivo a una base de datos SQL Server#######################################
import pyodbc
import os
conexion = pyodbc.connect('DRIVER={SQL SERVER};'
                           'SERVER=DESKTOP-FE1O4UB;'
                           'database=Gob_Datos_Devops_Act1;'
                           'Trusted_Connection=yes;')

Cursor = conexion.cursor()

# Query para ejecutar el BULK INSERT
query = """
BULK INSERT [Gob_Datos_Devops_Act1].[dbo].[DataTerrazas]
FROM 'C:\\Users\\Yeider\\Desktop\\Master Visual Analitics And Big Data\\Gobierno del dato y toma de decisiones\\Actividades\\Actividad 1\\DevOps\\DataTerrazas.csv'
WITH (
    FIELDTERMINATOR = ',',  
    FIRSTROW = 2,            
    FORMAT = 'CSV',          
    FIELDQUOTE = '"',        
    TABLOCK,                 
    ORDER (
[id_terraza],
[id_local],
[Cod_Postal],
[id_periodo_terraza],
[desc_periodo_terraza],
[id_situacion_terraza],
[desc_situacion_terraza],
[Superficie_ES],
[Superficie_RA],
[Fecha_confir_ult_decreto_resol],
[id_ndp_terraza],
[ID_VIAL],
[DESC_CLASE],
[DESC_NOMBRE],
[num_terraza],
[cal_terraza],
[desc_ubicacion_terraza],
[hora_ini_LJ_es],
[hora_fin_LJ_es],
[hora_ini_LJ_ra],
[hora_fin_LJ_ra],
[hora_ini_VS_es],
[hora_fin_VS_es],
[hora_ini_VS_ra],
[hora_fin_VS_ra],
[mesas_aux_es],
[mesas_aux_ra],
[mesas_es],
[mesas_ra],
[sillas_es],
[sillas_ra],
[Superficie_TO],
[Ratio],
[Unnamed: 0_y],
[id_distrito_local_y],
[desc_distrito_local_y],
[id_barrio_local_y],
[desc_barrio_local_y],
[cod_barrio_local],
[id_seccion_censal_local],
[desc_seccion_censal_local],
[coordenada_x_local_y],
[coordenada_y_local_y],
[id_tipo_acceso_local_y],
[desc_tipo_acceso_local_y],
[id_situacion_local_y],
[desc_situacion_local_y],
[id_ndp_edificio_y],
[id_vial_edificio_y],
[clase_vial_edificio_y],
[desc_vial_edificio_y],
[num_edificio_y],
[cal_edificio],
[secuencial_local_PC_y],
[id_ndp_acceso],
[id_vial_acceso],
[clase_vial_acceso],
[desc_vial_acceso],
[nom_acceso],
[num_acceso],
[cal_acceso],
[id_agrupacion],
[nombre_agrupacion],
[id_tipo_agrup],
[desc_tipo_agrup],
[id_planta_agrupado_y],
[rotulo_y],
[ref_licencia],
[id_tipo_licencia],
[desc_tipo_licencia],
[id_tipo_situacion_licencia],
[desc_tipo_situacion_licencia],
[Fecha_Dec_Lic]
    )  
);
"""

print('Se guardo la informacion en la Base de datos')
