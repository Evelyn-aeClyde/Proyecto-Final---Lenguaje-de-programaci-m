import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import os 

def generar_grafico_importancia(df):
    print("="*60)
    print("      GENERANDO GRÁFICO DE IMPORTANCIA DE CARACTERÍSTICAS")
    print("="*60)

    df_modelo = df.copy()
    df_modelo['Placement'] = df_modelo['Placement'].apply(lambda x: 1 if x == 'Yes' else 0)
    df_modelo['Internship_Experience'] = df_modelo['Internship_Experience'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    X = df_modelo.drop(columns=['Placement', 'College_ID'])
    y = df_modelo['Placement']

    print("🧠 Entrenando modelo de Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    print("✅ Modelo entrenado.")

    feature_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    print("\n--- Importancia de cada Característica ---")
    print(feature_importance_df)

    print("\n📊 Generando gráfico...")
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importance_df, palette='viridis')
    
    plt.title('Importancia de Características para la Predicción de Colocación', fontsize=16)
    plt.xlabel('Importancia', fontsize=12)
    plt.ylabel('Característica', fontsize=12)
    
    nombre_carpeta = "grafico_importancia_caracteristicas"
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
    
    ruta_grafico = os.path.join(nombre_carpeta, "grafico_importancia_caracteristicas.png")

    plt.savefig(ruta_grafico, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: '{ruta_grafico}'")
    plt.show()

if __name__ == "__main__":
    try:
        df = pd.read_csv("college_student_placement_dataset.csv")
        generar_grafico_importancia(df)
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'college_student_placement_dataset.csv'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")