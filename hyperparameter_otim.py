""" ## Importação das bibliotecas """
import pandas as pd
import json
import pickle
import random
from genetic_algorithm import mutate, order_crossover, calculate_fitness, sort_population, generate_population, tournament_selection
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

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

# Treinamento RF
rf = Pipeline(
    [
      ("model", RandomForestClassifier(random_state=42))
    ]
)
rf.fit(x_train_escalonado, y_train)
y_predito_rf = rf.predict(x_test_escalonado)

# Treinamento SVM
svm = Pipeline(
    [
        ("linear_svc", LinearSVC(C=1, random_state=42))
    ]
)
svm.fit(x_train_escalonado, y_train)
y_predito_svm = svm.predict(x_test_escalonado)

# Treinamento KNN
knn = Pipeline(
    [
        ("model", KNeighborsClassifier(n_neighbors=9))
    ]
)
knn.fit(x_train_escalonado, y_train)
y_predito_knn = knn.predict(x_test_escalonado)

"""# Avaliação dos modelos"""

kfold  = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
result_rf = cross_val_score(rf, x_train_escalonado, y_train, cv = kfold, scoring="recall_macro").mean()
result_svm = cross_val_score(svm, x_train_escalonado, y_train, cv = kfold, scoring="recall_macro").mean()
result_knn = cross_val_score(knn, x_train_escalonado, y_train, cv = kfold, scoring="recall_macro").mean()

databases = {"x_train": x_train_escalonado, "x_test": x_test_escalonado, "y_train": y_train, "y_test": y_test}

"""# Configuração do algoritmo genético"""

# Parâmetros do otimizador
POPULATION_SIZE = 100
N_GENERATIONS = 10
#models: 'knn' | 'rf' | 'svm'
model = 'rf'
MUTATION_PROBABILITY = 0.5

"""# Fazendo a otimização dos hiperparâmetros de todos os modelos"""

population = generate_population(POPULATION_SIZE, model)
best_fitness_values = []
best_solutions = []

for generation in range(N_GENERATIONS):
    population_fitness = [calculate_fitness(individual, model, databases) for individual in population]    
    
    population, population_fitness = sort_population(population,  population_fitness)
    
    best_fitness = population_fitness[0]
    best_solution = population[0]
       
    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)    
    print(f"Generation {generation}: Best fitness = {best_fitness}")
    # Elitismo: manter o melhor indivíduo quando for recriar a população
    new_population = [population[0]]  
    
    while len(new_population) < POPULATION_SIZE:
        # Selection por truncamento
        # Nesse caso, pega os 10 melhores indivíduos e escolhe 2 dentre eles para passar pelo processo de crossover. Comentei pois o processo de torneio tinha uma variabilidade maior.

        #parent1, parent2 = random.choices(population[:10], k=2)

        # Selection por torneio
        parent1 = tournament_selection(population, population_fitness)
        parent2 = tournament_selection(population, population_fitness)
        # # Com esse while, não permito que os pais sejam os mesmos, então ele vai realizar o processo novamente até achar pais diferentes.
        while parent1 == parent2:
            parent2 = tournament_selection(population, population_fitness)

        # Crossover
        child1 = order_crossover(parent1, parent2)
        # Mutation
        child1 = mutate(child1, MUTATION_PROBABILITY, model)
        new_population.append(child1)
    population = new_population

trained_model: any

match model:
    case 'rf':
        print("Recall do modelo Random Forest (sem otimização): {0}".format(result_rf))
        print("=====================================")
        print("Recall do modelo Random Forest (otimizado): {0}".format(best_fitness))
        print("Hiperparâmetros otimizados: {0}".format(best_solution))
        trained_model = RandomForestClassifier(
            n_estimators=best_solution["rf_n_estimators"],
            max_depth=best_solution["rf_max_depth"],
            min_samples_split=best_solution["rf_min_samples_split"],
            min_samples_leaf=best_solution["rf_min_samples_leaf"],
            max_features=best_solution["rf_max_features"],
            random_state=42,
            n_jobs=-1
        )
    case 'svm':
        print("Recall do modelo SVM (sem otimização): {0}".format(result_svm))
        print("=====================================")
        print("Recall do modelo SVM (otimizado): {0}".format(best_fitness))
        print("Hiperparâmetros otimizados: {0}".format(best_solution))
        trained_model = LinearSVC(
            C=best_solution["svm_C"],
            max_iter=best_solution["svm_max_iter"],
            tol=best_solution["svm_tol"],
            random_state=42
        )
    case 'knn':
        print("Recall do modelo KNN (sem otimização): {0}".format(result_knn))
        print("=====================================")
        print("Recall do modelo KNN (otimizado): {0}".format(best_fitness))
        print("Hiperparâmetros otimizados: {0}".format(best_solution))
        trained_model = KNeighborsClassifier(
            n_neighbors=best_solution["knn_neighbors"],
            weights=best_solution["knn_weights"],
            metric=best_solution["knn_metric"],
            p=best_solution["knn_p"]
        )
    case _:
        print("Model not found.")     

trained_model.fit(x_train_escalonado, y_train)

result = {
    "model": model,
    "hyperparameters": best_solution,
    "recall_cv": best_fitness
}

with open("results_model.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

with open('model.pkl', 'wb') as file:
    pickle.dump(trained_model, file)

with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

print("Modelo exportado com sucesso!")

"""# Testes feitos e observações adicionais estarão no arquivo tests.md"""