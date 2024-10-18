import pandas as pd


# Cargar el dataset de licencias.
df = pd.read_excel("Licencia_002.xlsx")

########################## Detección y Eliminación de Duplicados ##############################################################

# Número de registros antes de eliminar duplicados
Contar_Original = len(df)
print(Contar_Original)

# Identificar y eliminar duplicados basados en las columnas 'id_local' y 'ref_licencia'
Licencias_SinDuplicados = df.drop_duplicates(subset=['id_local', 'ref_licencia'])

# Número de registros después de eliminar duplicados
Contar = len(Licencias_SinDuplicados)

# Imprimir la cantidad de registros eliminados
print(f"Registros eliminados: {Contar_Original - Contar}")

df.to_excel('Licencias_SinDuplicados.xlsx')

############################### limpieza y normalización de cadenas de texto ########################################

# Cargar el dataset "Books" desde un archivo JSON
df = pd.read_json("books_corrected.json")

# Función para limpiar y normalizar cadenas de texto
def limpiar_texto(text):
    if isinstance(text, str):  # Verificar que el valor es una cadena
        texto_original = text  # Guardar el texto original
        text = text.lower()  # Convertir a minúsculas
        text = text.strip()  # Eliminar espacios al principio y al final
        return texto_original, text  # Retornar tanto el original como el transformado
    return text, text  # Para no cadenas, retorna el mismo valor

# Almacenar la cantidad de cambios por columna
change_counts = {}

# Aplicar la función de limpieza a todas las columnas categóricas
for col in df.select_dtypes(include=['object']).columns:
    original, limpiado = zip(*df[col].apply(limpiar_texto))  # Desempaquetar originales y limpios
    df[col] = limpiado  # Actualizar la columna con los valores limpios
    # Contar los cambios
    change_counts[col] = sum(1 for o, c in zip(original, limpiado) if o != c)

# Imprimir la cantidad de cambios realizados
for col, count in change_counts.items():
    print(f"Cantidad de cambios en la columna '{col}': {count}")


# Guardar el dataset limpio como "Books_Limpio.json"
df.to_json("Books_Limpio.json", orient='records', lines=True)

print("Dataset limpio guardado como 'Books_Limpio.json'.")