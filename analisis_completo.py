import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analisis_completo_de_datos(df):
    """
    Realiza un análisis estadístico y gráfico de las columnas numéricas
    y genera un gráfico circular para la columna 'Placement'.
    """
    print("="*60)
    print("           INICIANDO ANÁLISIS ESTADÍSTICO COMPLETO")
    print("="*60)

    nombre_carpeta = "Graficos_Completos"
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
        print(f"📁 Carpeta '{nombre_carpeta}' creada para guardar los gráficos.")

    # --- ANÁLISIS DE COLUMNAS NUMÉRICAS ---
    columnas_numericas = df.select_dtypes(include=np.number).columns
    print(f"\nSe analizarán las siguientes columnas numéricas: {list(columnas_numericas)}")

    for columna in columnas_numericas:
        print("\n" + "-"*50)
        print(f"Análisis de la columna: '{columna}'")
        print("-"*50)
        
        datos_columna = df[columna].dropna()

        media = np.mean(datos_columna)
        mediana = np.median(datos_columna)
        # Usamos .get(0, 'N/A') por si no hay moda.
        moda = datos_columna.mode().get(0, 'N/A')
        desviacion_std = np.std(datos_columna)
        
        print(f"  - Media (Promedio): {media:.2f}")
        print(f"  - Mediana (Valor central): {mediana:.2f}")
        print(f"  - Moda (Valor más frecuente): {moda}")
        print(f"  - Desviación Estándar: {desviacion_std:.2f}")
        
        plt.figure(figsize=(10, 6))
        sns.histplot(datos_columna, kde=True, bins=30)
        
        plt.axvline(media, color='red', linestyle='--', label=f'Media: {media:.2f}')
        plt.axvline(mediana, color='green', linestyle='-', label=f'Mediana: {mediana:.2f}')
        if moda != 'N/A':
             plt.axvline(moda, color='purple', linestyle=':', label=f'Moda: {moda:.2f}')
        
        plt.title(f'Distribución de "{columna}"', fontsize=16)
        plt.xlabel(columna, fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.legend()
        
        ruta_grafico = os.path.join(nombre_carpeta, f"distribucion_{columna}.png")
        plt.savefig(ruta_grafico)
        print(f"✅ Gráfico de distribución guardado en: '{ruta_grafico}'")
        plt.show()

    # =================================================================
    # == NUEVA SECCIÓN: ANÁLISIS DE LA COLUMNA CATEGÓRICA 'PLACEMENT' ==
    # =================================================================
    
    print("\n" + "-"*50)
    print("Análisis de la columna: 'Placement'")
    print("-"*50)

    # Contar los valores 'yes' y 'no'
    placement_counts = df['Placement'].value_counts()
    print("Conteo de valores:")
    print(placement_counts)

    # Crear el gráfico circular (pie chart)
    plt.figure(figsize=(8, 8))
    plt.pie(
        placement_counts, 
        labels=placement_counts.index, 
        autopct='%1.1f%%',  # Muestra el porcentaje con un decimal
        startangle=90,      # Inicia el primer sector en la parte superior
        colors=['#2ca02c', '#d62728'] # Verde para 'Yes', Rojo para 'No'
    )
    
    plt.title('Distribución de Resultados de Placement', fontsize=16)
    plt.axis('equal')  # Asegura que el gráfico sea un círculo perfecto.
    
    # Guardar el gráfico circular
    ruta_grafico_pie = os.path.join(nombre_carpeta, "distribucion_placement_pie.png")
    plt.savefig(ruta_grafico_pie)
    print(f"\n✅ Gráfico de círculo guardado en: '{ruta_grafico_pie}'")
    plt.show()

    print("\n" + "="*60)
    print("🎉 Análisis completado. Todos los gráficos han sido guardados.")
    print("="*60)


if __name__ == "__main__":
    try:
        df = pd.read_csv("college_student_placement_dataset.csv")
        # Aseguramos que la columna 'Placement' tenga el formato correcto para el análisis
        df['Placement'] = df['Placement'].str.capitalize()
        analisis_completo_de_datos(df)
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'college_student_placement_dataset.csv'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")