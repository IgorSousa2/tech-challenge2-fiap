""" ## Importação das bibliotecas """

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import make_scorer, accuracy_score, f1_score, classification_report
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

"""## Análise exploratória dos dados"""

dados = pd.read_csv('./content/data.csv', sep=',')
dados = dados.loc[:, ~dados.columns.str.contains('^Unnamed')]

"""# Pré-Processamento de dados + Separação de bases (treino e teste)"""

x = dados[["concave points_mean", "radius_worst", "perimeter_worst", "concave points_worst"]]
y = dados["diagnosis"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42)
scaler = StandardScaler()
scaler.fit(x_train)
x_train_escalonado = scaler.transform(x_train)
x_test_escalonado = scaler.transform(x_test)

"""# Configuração e treinamento dos modelos"""

rf = Pipeline(
    [
      ("model", RandomForestClassifier(random_state=42))
    ]
)

rf.fit(x_train_escalonado, y_train)

y_predito_rf = rf.predict(x_test_escalonado)

svm = Pipeline(
    [
        ("linear_svc", LinearSVC(C=1))
    ]
)

svm.fit(x_train_escalonado, y_train)

y_predito_svm = svm.predict(x_test_escalonado)

error = []

for i in range(1,10):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(x_train_escalonado, y_train)
    pred_i = knn.predict(x_test_escalonado)
    error.append(np.mean(pred_i != y_test))

modelo_knn = KNeighborsClassifier(n_neighbors=9)
modelo_knn.fit(x_train_escalonado, y_train)
y_predito_knn = modelo_knn.predict(x_test_escalonado)

"""# Avaliação dos modelos"""

#Avaliação do modelo RF
print("Random Forest:")
print(classification_report(y_test, y_predito_rf))

#Avaliação do modelo SVM
print("SVM:")
print(classification_report(y_test, y_predito_svm))

#Avaliação do modelo KNN
print("KNN:")
print(classification_report(y_test, y_predito_knn))

kfold  = KFold(n_splits=5, shuffle=True)
result_rf = cross_val_score(rf, x, y, cv = kfold)
result_svm = cross_val_score(svm, x, y, cv = kfold)
result_knn = cross_val_score(modelo_knn, x, y, cv = kfold)

print("Média R^2 do modelo RF: {0}".format(result_rf.mean()))
print("Média R^2 do modelo SVM: {0}".format(result_svm.mean()))
print("Média R^2 do modelo KNN: {0}".format(result_knn.mean()))