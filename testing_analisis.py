import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# https://youtu.be/iX_on3VxZzk?si=ONpvhSIVrYU9l_SA
#https://pandas.pydata.org/docs/reference/frame.html
#https://numpy.org/doc/stable/user/index.html << https://joserzapata.github.io/courses/python-ciencia-datos/numpy/

# pd.set_option('display.max_rows', None)

# DataFrame sin valores Null
df = pd.read_csv('water_potability.csv', sep=',')
# ds = pd.read_csv('water_potability.csv', sep=',') # comparaciones
# Reemplaza los nan por la mediana
df.fillna(df.median(), inplace=True)


# ============================================ Limpieza de Atipicos y Normalizacion ================================================== #

def atipicos_col(col_name):
    sample_ordenado = sorted(col_name)
    n = len(sample_ordenado)

    # Cuartiles
    Q1 = sample_ordenado[n // 4]
    Q2 = (sample_ordenado[n // 2 - 1] + sample_ordenado[n // 2]) / 2
    Q3 = sample_ordenado[3 * n // 4]
    iqr = Q3 - Q1

    # print(f'Cuantiles de {col_name.values}')
    # print('Valores mayores a: ', Q3 + (1.5 * iqr), ' => Son atipicos')
    # print('Valores menores a: ',Q1 - (1.5 * iqr), ' => Son atipicos')
    # print('\n')

    atipicos = []

    # Calcula los valores atipicos
    for x in sample_ordenado:
        if (x > Q3 + (1.5 * iqr) or (x < Q1 - (1.5 * iqr))):
            atipicos.append(x)
        else:
            pass
    
    # Retorna la lista ordenada para despues armar el nuevo dataframe.
    return atipicos

def limpieza_col(data_frame):
    columnas = data_frame.columns.to_list()
    del columnas[0], columnas[6]
    atipicos = 0

    for item in columnas:
        atipicos = atipicos_col(data_frame[item])
        for x in atipicos:
            data_frame.loc[data_frame[item] == x, item] = data_frame[item].median() # Los atipicos se llenan con la mediana

    return data_frame

# Consultar por esto
# Columnas 'ph' y 'Trihalomethanes' vuelven todas en NaN, por eso las borro en la segunda linea de 'limpieza_col()'
df = limpieza_col(df)
# print('\nPOST LIMPIEZA\n',df.describe())

# ====================================== ERROR^2 =========================================== #

# Prueba con una línea dada
# m = 1.93939
# b = 4.73333
# sum_of_squares = 0.0
# df_copy = df[['ph', 'Potability']].copy()
# # calcular la suma de cuadrados
# for p in df_copy.itertuples(index=False):
#     y_salida = p[1]
#     y_predict = m*p[0] + b
#     residual_squared = (y_predict - y_salida)**2
#     sum_of_squares += residual_squared
# print(f"suma de cuadrados = {sum_of_squares}")

# ========================= GRAFICOS POST LIMPIEZA ============================ #
# Son horribles

# def regresion_lin(df, column):
#     plt.figure(figsize=(8, 5))
    
#     # Todas excepto potabilidad
#     data = df[[column, 'Potability']].dropna()
#     X = data['Potability'].values.reshape(-1, 1)
#     y = data[column].values
    
#     # Arma la regresion
#     model = LinearRegression()
#     model.fit(X, y)
#     y_pred = model.predict(X)
    
#     # Puntos
#     plt.scatter(X, y, color='blue', label='Data')
    
#     # Regresion lineal
#     plt.plot(X, y_pred, color='red', label='Linear Regression')
    
#     # Titulos y Ejes
#     plt.title(f'{column} and Potability')
#     plt.xlabel('Potability')
#     plt.ylabel(column)
    
#     plt.show()

# # Esto solo itera para printear todas juntas
# ploteo_total = df.columns[:-1]
# for column in ploteo_total:
#     regresion_lin(df, column)

# plt.figure(figsize=(10, 8))
# matriz_corr = df.corr()

# sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', linewidths=0.3)
# plt.title('Matriz de Correlacion')
# plt.show()

# ============================================== RED NEURONAL ========================================= #

from sklearn.model_selection import train_test_split

# Extraigo las columnas de entrada
inputs = df.iloc[:, 0:9].values
outputs = df.iloc[:, -1].values

# Conjuntos de entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(inputs, outputs, test_size=1/3)

#shape retorna una tupla con las dimensiones de la matriz = (filas, columnas).
# por lo que shape[0], nos retorna las filas de la matriz.
n = x_train.shape[0] # número de registros de entrenamiento

# Red neuronal
# pesos
w_hidden_1 = np.random.rand(3,9)
w_output_1 = np.random.rand(1,3)

# Como seria para ponerle 2 capas de neuronas?
# w_hidden_2 = np.random.rand(,)
# w_output_2 = np.random.rand(,)

# sesgos
b_hidden = np.random.rand(3,1)
b_output = np.random.rand(1,1)

# Funciones de Activacion
relu = lambda x: np.maximum(x, 0)
sigmoide = lambda x: 1 / (1 + np.exp(-x))

def f_prop(X):
    z1 = w_hidden_1 @ X + b_hidden
    a1 = relu(z1)
    z2 = w_output_1 @ a1 + b_output
    a2 = sigmoide(z2)
    return z1, a1, z2, a2

test_predictions = f_prop(x_test.transpose())[3] # me interesa solo la capa de salida, A2
test_comparisons = np.equal((test_predictions >= .5).flatten().astype(int), y_test)
accuracy = sum(test_comparisons.astype(int) / x_test.shape[0])
print("ACCURACY: ", accuracy)


