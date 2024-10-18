import pandas as pd   

terrazas = pd.read_excel('Terrazas_Normalizadas.xlsx')
licencias = pd.read_excel('Licencias_SinDuplicados.xlsx')

# INNER JOIN entre el dataset "Terrazas_Normalizadas" y "Licencias_SinDuplicados" usando la columna "id_local" ##################################
licencias_terrazas_integradas = pd.merge(terrazas, licencias, on='id_local', how='inner')

# Guardar archivo
licencias_terrazas_integradas.to_excel('Licencias_Terrazas_Integradas.xlsx', index=False)
licencias_terrazas_integradas.to_csv('Licencias_Terrazas_Integradas.csv', index=False)


######################### combina y Agrega Datos Geográficos #################################

Terrazas_202104 = ( pd.read_excel('Terrazas_202104.xlsx'))
Terrazas_202104.columns

# Agregar superficies por barrio
superficies_por_barrio = Terrazas_202104.groupby('desc_barrio_local')['Superficie_ES'].sum().reset_index()

# Documentar áreas con mayor y menor superficie agregada (por barrio)
barrio_max_superficie = superficies_por_barrio.loc[superficies_por_barrio['Superficie_ES'].idxmax()]
barrio_min_superficie = superficies_por_barrio.loc[superficies_por_barrio['Superficie_ES'].idxmin()]

print("Barrio con mayor superficie agregada:")
print(barrio_max_superficie)

print("\nBarrio con menor superficie agregada:")
print(barrio_min_superficie)

# Guardar el resultado en un nuevo archivo CSV
superficies_por_barrio.to_excel('Superficies_Agregadas.xlsx', index=False)

