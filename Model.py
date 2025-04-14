import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from datetime import datetime

# Cargar el dataset
csv_path = '/Users/cristiancastro/Documents/Formación/Ingenierías de software/Semestre 8/IA/Python/MIO/dataset.csv'
try:
    df = pd.read_csv(csv_path, sep=';')
    print("Dataset cargado exitosamente.")
    print(f"Número de filas: {len(df)}")
    print("Columnas encontradas:", list(df.columns))
except FileNotFoundError:
    print(f"Error: No se encontró '{csv_path}'. Verifica la ruta del archivo.")
    exit()
except Exception as e:
    print(f"Error al cargar el CSV: {e}")
    exit()

# Verificar columnas esperadas
expected_columns = ['Origen', 'Destino', 'Ruta', 'TiempoViaje', 'Hora', 'DíaSemana', 'Pasajeros', 'Retraso']
if not all(col in df.columns for col in expected_columns):
    print("Error: Faltan columnas esperadas. Columnas actuales:", list(df.columns))
    print("Columnas esperadas:", expected_columns)
    exit()

# Convertir Hora a minutos desde medianoche
def hora_a_minutos(hora):
    try:
        # Limpiar espacios y caracteres extraños
        hora = hora.strip().replace('\u202f', ' ').replace('\xa0', ' ')
        # Manejar formatos AM/PM (12 horas)
        if 'a. m.' in hora.lower() or 'p. m.' in hora.lower():
            # Reemplazar a. m./p. m. para estandarizar
            hora = hora.replace('a. m.', 'AM').replace('p. m.', 'PM')
            try:
                dt = datetime.strptime(hora, '%I:%M:%S %p')
                return dt.hour * 60 + dt.minute
            except ValueError:
                dt = datetime.strptime(hora, '%I:%M %p')
                return dt.hour * 60 + dt.minute
        elif 'AM' in hora or 'PM' in hora:
            try:
                dt = datetime.strptime(hora, '%I:%M:%S %p')
                return dt.hour * 60 + dt.minute
            except ValueError:
                dt = datetime.strptime(hora, '%I:%M %p')
                return dt.hour * 60 + dt.minute
        # Manejar formato 24 horas (HH:MM:SS o HH:MM)
        else:
            if len(hora.split(':')) == 3:
                h, m, _ = map(int, hora.split(':'))
                return h * 60 + m
            else:
                h, m = map(int, hora.split(':'))
                return h * 60 + m
    except Exception as e:
        print(f"Error en formato de hora: {hora}. Usando valor por defecto (0). Error: {e}")
        return 0

# Aplicar conversión y verificar
df['Hora'] = df['Hora'].apply(hora_a_minutos)
unique_horas = df['Hora'].unique()
print(f"Valores únicos de Hora después de conversión (primeros 10): {unique_horas[:10]}")
if all(h == 0 for h in unique_horas):
    print("Advertencia: Todos los valores de Hora son 0. El formato de hora podría seguir siendo incorrecto.")

# Preprocesamiento
le_origen = LabelEncoder()
le_destino = LabelEncoder()
le_ruta = LabelEncoder()
le_dia = LabelEncoder()

df['Origen'] = le_origen.fit_transform(df['Origen'])
df['Destino'] = le_destino.fit_transform(df['Destino'])
df['Ruta'] = le_ruta.fit_transform(df['Ruta'])
df['DíaSemana'] = le_dia.fit_transform(df['DíaSemana'])

# Seleccionar características y objetivo
X = df[['Origen', 'Destino', 'Ruta', 'Hora', 'DíaSemana', 'Pasajeros', 'Retraso']]
y = df['TiempoViaje']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
try:
    model.fit(X_train, y_train)
    print("Modelo entrenado exitosamente.")
except Exception as e:
    print(f"Error al entrenar el modelo: {e}")
    exit()

# Predecir y evaluar
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nResultados del modelo:")
print(f"Error Cuadrático Medio (MSE): {mse:.2f}")
print(f"Coeficiente de Determinación (R²): {r2:.2f}")

# Ejemplo de predicción
try:
    ejemplo = pd.DataFrame({
        'Origen': [le_origen.transform(['Universidades'])[0]],
        'Destino': [le_destino.transform(['San Fernando'])[0]],
        'Ruta': [le_ruta.transform(['T47A'])[0]],
        'Hora': [hora_a_minutos('07:30')],
        'DíaSemana': [le_dia.transform(['Lunes'])[0]],
        'Pasajeros': [50],
        'Retraso': [0]
    })
    prediccion = model.predict(ejemplo)
    print(f"\nTiempo estimado para Universidades -> San Fernando: {prediccion[0]:.2f} minutos")
except ValueError as e:
    print(f"Error en la predicción de ejemplo: {e}")
    print("Verifica que 'Universidades', 'San Fernando', 'T47A' y 'Lunes' estén en el dataset.")

# Importancia de características
importancias = pd.Series(model.feature_importances_, index=X.columns)
print("\nImportancia de características:")
print(importancias.sort_values(ascending=False))