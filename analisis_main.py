import pandas as pd
from pyswip import Prolog
import os
import time

# --- IMPORTACIONES PARA MACHINE LEARNING ---
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# --- FUNCIONES DE CONFIGURACIÓN E INICIALIZACIÓN ---

def inicializar_prolog():
    """Inicializa el motor de Prolog y carga el archivo de reglas."""
    prolog = Prolog()
    prolog.retractall("estudiante(_,_,_,_,_,_,_,_,_,_,_)")
    try:
        prolog.consult("reglas_placement.pl")
        print("✅ Base de conocimiento 'reglas_placement.pl' cargada correctamente.")
        return prolog
    except Exception as e:
        print(f"❌ ERROR FATAL: No se pudo cargar 'reglas_placement.pl'.\n   Detalle: {e}")
        return None

def cargar_y_preparar_datos_csv(nombre_archivo_csv):
    """Carga y prepara los datos del CSV."""
    try:
        df = pd.read_csv(nombre_archivo_csv)
        df['Internship_Experience'] = df['Internship_Experience'].str.lower()
        df['Placement'] = df['Placement'].str.lower()
        print(f"✅ Se cargaron {len(df)} registros del archivo '{nombre_archivo_csv}'.")
        return df
    except FileNotFoundError:
        print(f"❌ ERROR FATAL: No se encontró el archivo CSV '{nombre_archivo_csv}'.")
        return None

def cargar_hechos_en_prolog(prolog, df):
    """Carga los datos del DataFrame en Prolog."""
    print("\n🧠 Cargando datos en el motor lógico de Prolog... (Puede tardar un momento)")
    try:
        query_template = "assertz(estudiante({},'{}',{},{},{},{},'{}',{},{},{},'{}'))"
        for row in df.itertuples(index=True):
            query = query_template.format(row[0], *row[1:])
            list(prolog.query(query))
        print("✅ ¡Motor lógico listo! Todos los datos han sido cargados.")
        return True
    except Exception as e:
        print(f"❌ Error durante la carga de hechos en Prolog: {e}")
        return False

# --- FUNCIONES DE MACHINE LEARNING ---

def entrenar_modelo_ia(df):
    """Entrena un modelo de IA y lo devuelve junto con sus componentes."""
    print("\n🤖 Entrenando modelo de Inteligencia Artificial...")
    df_modelo = df.copy()
    codificadores = {}
    for columna in ['College_ID', 'Internship_Experience', 'Placement']:
        le = LabelEncoder()
        df_modelo[columna] = le.fit_transform(df_modelo[columna])
        codificadores[columna] = le
        
    X = df_modelo.drop('Placement', axis=1)
    y = df_modelo['Placement']
    
    modelo = RandomForestClassifier(n_estimators=100, random_state=42, oob_score=True)
    modelo.fit(X, y)
    print(f"✅ Modelo de IA entrenado. Precisión estimada: {modelo.oob_score_ * 100:.2f}%")
    return modelo, codificadores, X.columns

def predecir_empleabilidad_con_ia(modelo, codificadores, columnas_modelo):
    """Pide datos al usuario y usa el modelo para predecir la probabilidad de contratación."""
    print("\n=========================================================")
    print("--- Predicción de Empleabilidad con IA ---")
    print("=========================================================")
    print("Introduce los datos del estudiante para predecir su resultado:")
    datos_estudiante = {}
    try:
        for columna in columnas_modelo:
            if columna == 'College_ID':
                datos_estudiante[columna] = 0 # Usamos un valor por defecto
            elif columna == 'Internship_Experience':
                respuesta = input(" - ¿Tiene experiencia en pasantías? (yes/no): ").lower()
                datos_estudiante[columna] = codificadores[columna].transform([respuesta])[0]
            else:
                valor = float(input(f" - Introduce el valor para '{columna}': "))
                datos_estudiante[columna] = valor

        df_nuevo = pd.DataFrame([datos_estudiante])
        probabilidades = modelo.predict_proba(df_nuevo)
        prob_contratado = probabilidades[0][1]
        
        print("\n----------------- PREDICCIÓN -----------------")
        print(f"✅ La probabilidad de que este estudiante sea contratado es del: {prob_contratado * 100:.2f}%")
        print("--------------------------------------------")
    except Exception as e:
        print(f"❌ Error en la entrada de datos. Detalle: {e}")

# --- FUNCIÓN GENÉRICA DE EXPORTACIÓN (CORREGIDA) ---

def exportar_resultados(df_exportar, nombre_base_archivo, consulta_realizada=None):
    """
    Exporta el DataFrame proporcionado a formatos Excel y HTML.
    """
    if df_exportar.empty:
        print("ℹ️ No hay datos para exportar.")
        return

    nombre_carpeta = "Reportes"
    os.makedirs(nombre_carpeta, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # --- BLOQUE DE EXPORTACIÓN A EXCEL (RESTAURADO) ---
    try:
        ruta_excel = os.path.join(nombre_carpeta, f"{nombre_base_archivo}_{timestamp}.xlsx")
        with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
            df_exportar.to_excel(writer, index=False, sheet_name='Resultados')
            worksheet = writer.sheets['Resultados']
            for idx, col in enumerate(df_exportar):
                series = df_exportar[col]
                try:
                    max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = max_len
                except (ValueError, TypeError):
                    worksheet.column_dimensions[chr(65 + idx)].width = len(str(col)) + 2
        print(f"✅ ¡Reporte Excel exportado a '{ruta_excel}'!")
    except Exception as e:
        print(f"❌ Error al exportar a Excel: {e}")

    # --- BLOQUE DE EXPORTACIÓN A HTML ---
    try:
        ruta_html = os.path.join(nombre_carpeta, f"{nombre_base_archivo}_{timestamp}.html")
        html_tabla = df_exportar.to_html(index=False, justify='center', border=0, classes='styled-table')
        seccion_consulta = f"<h2>Consulta Realizada:</h2><p><code>{consulta_realizada}</code></p>" if consulta_realizada else ""
        html_completo = f"""<html><head><title>Reporte</title><style>body{{font-family:Arial,sans-serif;margin:20px}}h1,h2{{color:#333}}code{{background-color:#eee;border:1px solid #ddd;padding:2px 5px;border-radius:4px}}.styled-table{{border-collapse:collapse;margin:25px 0;font-size:0.9em;min-width:400px;box-shadow:0 0 20px rgba(0,0,0,0.15)}}.styled-table thead tr{{background-color:#009879;color:#fff;text-align:left}}.styled-table th,.styled-table td{{padding:12px 15px}}.styled-table tbody tr{{border-bottom:1px solid #ddd}}.styled-table tbody tr:nth-of-type(even){{background-color:#f3f3f3}}</style></head><body><h1>Reporte: {nombre_base_archivo.replace('_',' ').title()}</h1>{seccion_consulta}{html_tabla}</body></html>"""
        with open(ruta_html, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        print(f"✅ ¡Reporte HTML exportado a '{ruta_html}'!")
    except Exception as e:
        print(f"❌ Error al exportar a HTML: {e}")

def ejecutar_consulta_prolog(prolog, df, titulo_perfil, regla_prolog):
    """Ejecuta una consulta de Prolog y gestiona la exportación."""
    print(f"\n--- Consultando Perfil de Prolog: {titulo_perfil} ---")
    query_string = f"{regla_prolog}(StudentID)"
    try:
        resultados_prolog = list(prolog.query(query_string))
        if not resultados_prolog:
            print("ℹ️ No se encontraron estudiantes.")
            return
        lista_indices = sorted([res["StudentID"] for res in resultados_prolog])
        df_resultados = df.loc[lista_indices].copy()
        print(f"✅ Se encontraron {len(df_resultados)} estudiantes.")
        print("\nVista previa (primeros 5):\n", df_resultados.head().to_string())
        exportar_resultados(df_resultados, f"reporte_{regla_prolog}", consulta_realizada=f"Perfil de Prolog: {regla_prolog}(StudentID)")
    except Exception as e:
        print(f"❌ Error al procesar el perfil: {e}")

def busqueda_personalizada(df):
    """Permite al usuario realizar una búsqueda personalizada en los datos."""
    print("\n--- Búsqueda Personalizada por Columna ---")
    columnas = list(df.columns)
    for i, col in enumerate(columnas, 1):
        print(f"{i}. {col}")
    try:
        col_choice = int(input(f"\nElige el número de columna (1-{len(columnas)}): "))
        columna_seleccionada = columnas[col_choice - 1]
    except (ValueError, IndexError):
        print("❌ Opción no válida.")
        return
    operador = input("Introduce el operador (ej. >, <, ==, !=): ")
    if operador not in ['>', '<', '>=', '<=', '==', '!=']:
        print("❌ Operador no válido.")
        return
    valor = input(f"Introduce el valor para '{columna_seleccionada}': ")
    try:
        query_pandas = f"`{columna_seleccionada}` {operador} {float(valor) if pd.api.types.is_numeric_dtype(df[columna_seleccionada]) else f"'{valor.lower()}'"}"
        print(f"\n🔎 Ejecutando consulta: {query_pandas}")
        df_resultados = df.query(query_pandas)
        if df_resultados.empty:
            print("ℹ️ No se encontraron resultados.")
        else:
            print(f"✅ Se encontraron {len(df_resultados)} estudiantes.")
            print("\nVista previa (primeros 5):\n", df_resultados.head().to_string())
            exportar_resultados(df_resultados, "reporte_busqueda_personalizada", consulta_realizada=query_pandas)
    except Exception as e:
        print(f"❌ Error en la búsqueda: {e}")

def mostrar_todos_los_datos(df):
    """Muestra un resumen y exporta todos los datos."""
    print("\n--- Resumen y Exportación de Todos los Datos ---")
    print("\nPrimeros 5 registros:\n", df.head().to_string())
    exportar_resultados(df, "reporte_COMPLETO", consulta_realizada="Exportación de todos los 10,000 registros.")

def mostrar_menu():
    """Muestra el menú interactivo con todas las opciones explícitas."""
    print("\n" + "="*55)
    print("      SISTEMA HÍBRIDO DE ANÁLISIS Y PREDICCIÓN")
    print("="*55)
    print("\n--- Consultas de Perfiles (Prolog) ---")
    print(" 1. Académico Top")
    print(" 2. Fuerte Experiencia Práctica")
    print(" 3. Líder / Gran Comunicador")
    print(" 4. El Esforzado (Mejora Notable)")
    print(" 5. Apuesta Segura (Perfil Balanceado)")
    print(" 6. Técnico sin Pasantía")
    print(" 7. Estudiante en Riesgo Académico")
    print(" 8. Joya Escondida (Potencial Oculto)")
    print(" 9. Riesgo por Desmotivación")
    print("\n--- Búsquedas y Vistas (Python/Pandas) ---")
    print(" 10. Búsqueda Personalizada por Columna")
    print(" 11. Mostrar y Exportar Todos los Datos")
    print("\n--- PREDICCIÓN DE EMPLEABILIDAD ---")
    print(" 12. Predecir Empleabilidad con IA")
    print("\n--- Salir ---")
    print(" 13. Salir del programa")
    return input("\nElige una opción (1-13): ")

def main():
    """Función principal que orquesta el programa."""
    prolog = inicializar_prolog()
    if not prolog:
        return
    df = cargar_y_preparar_datos_csv("college_student_placement_dataset.csv")
    if df is None:
        return
    if not cargar_hechos_en_prolog(prolog, df):
        return

    modelo_ia, codificadores, columnas_modelo = entrenar_modelo_ia(df)
    
    mapa_opciones_prolog = {
        '1': ("Académico Top", "candidato_academico_top"),
        '2': ("Fuerte Experiencia Práctica", "candidato_practico"),
        '3': ("Líder / Gran Comunicador", "lider_comunicador"),
        '4': ("El Esforzado", "perfil_esforzado"),
        '5': ("Apuesta Segura", "apuesta_segura"),
        '6': ("Técnico sin Pasantía", "tecnico_sin_pasantia"),
        '7': ("Estudiante en Riesgo Académico", "estudiante_en_riesgo"),
        '8': ("Joya Escondida", "joya_escondida"),
        '9': ("Riesgo por Desmotivación", "riesgo_desmotivacion"),
    }

    while True:
        opcion = mostrar_menu()
        if opcion in mapa_opciones_prolog:
            titulo, regla = mapa_opciones_prolog[opcion]
            ejecutar_consulta_prolog(prolog, df, titulo, regla)
        elif opcion == '10':
            busqueda_personalizada(df)
        elif opcion == '11':
            mostrar_todos_los_datos(df)
        elif opcion == '12':
            predecir_empleabilidad_con_ia(modelo_ia, codificadores, columnas_modelo)
        elif opcion == '13':
            print("\n👋 Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Por favor, elige un número del 1 al 13.")

if __name__ == "__main__":
    main()