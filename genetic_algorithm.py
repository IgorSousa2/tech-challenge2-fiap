from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer, recall_score, classification_report
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold
import random
import copy

HYPERPARAMS_RF = { 
    "rf_n_estimators": [50, 100, 150, 200, 300, 500],
    "rf_max_depth": [3, 5, 10, 15, 20, None],
    "rf_min_samples_split": [2, 5, 10],
    "rf_min_samples_leaf": [1, 2, 4],
    "rf_max_features": ["sqrt", "log2", None]
} 

HYPERPARAMS_SVM = { 
    "svm_C": [0.0001,1,10,100,1000],
    "svm_max_iter": [2000, 5000, 10000],
    "svm_tol": [1e-2, 1e-3, 1e-4, 1e-5]
} 

HYPERPARAMS_KNN = { 
    "knn_neighbors": [3,5,7,9,11,13,15,17,19], 
    "knn_weights": ['uniform','distance'],
    "knn_metric": ['cosine','euclidean','manhattan'],
    "knn_algorithm": ['auto','ball_tree','kd_tree','brute'],
    "knn_p": [1,2,3]
}

HYPERPARAMS = {
    'rf': HYPERPARAMS_RF,
    'svm': HYPERPARAMS_SVM,
    'knn': HYPERPARAMS_KNN
}

kfold  = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

def create_individual(model):
    # Cria o indivíduo com um valor aleatório dentre as opções de cada hiperparâmetro. 
    match model:
        case 'rf':
            return { 
                "rf_n_estimators": random.choice( HYPERPARAMS_RF["rf_n_estimators"] ), 
                "rf_max_depth": random.choice( HYPERPARAMS_RF["rf_max_depth"] ), 
                "rf_min_samples_split": random.choice( HYPERPARAMS_RF["rf_min_samples_split"] ),
                "rf_min_samples_leaf": random.choice( HYPERPARAMS_RF["rf_min_samples_leaf"] ),
                "rf_max_features": random.choice( HYPERPARAMS_RF["rf_max_features"] )
            } 
        case 'svm':
            return { 
                "svm_C": random.choice( HYPERPARAMS_SVM["svm_C"] ), 
                "svm_max_iter": random.choice( HYPERPARAMS_SVM["svm_max_iter"] ),
                "svm_tol": random.choice( HYPERPARAMS_SVM["svm_tol"] )
            } 
        case 'knn':
            return { 
                "knn_neighbors": random.choice( HYPERPARAMS_KNN["knn_neighbors"] ), 
                "knn_weights": random.choice( HYPERPARAMS_KNN["knn_weights"] ), 
                "knn_metric": random.choice( HYPERPARAMS_KNN["knn_metric"] ),
                # Comentando hiperparâmetro pois não funciona com determinadas metrics
                #"knn_algorithm": random.choice( HYPERPARAMS_KNN["knn_algorithm"] ),
                "knn_p": random.choice( HYPERPARAMS_KNN["knn_p"] ),
            } 
        case _:
            return "Model not found."
        
def generate_population(size, model): 
    return [ create_individual(model) for _ in range(size) ]         

def calculate_fitness(individual, model, databases):
    # Pega os valores de hiperparâmetro do indivíduo e realiza o treinamento de um modelo. Após treinar, realiza a avaliação do modelo e retorna a métrica de recall.
    match model:
        case 'rf':
            rf = RandomForestClassifier(
                n_estimators=individual["rf_n_estimators"],
                max_depth=individual["rf_max_depth"],
                min_samples_split=individual["rf_min_samples_split"],
                min_samples_leaf=individual["rf_min_samples_leaf"],
                max_features=individual["rf_max_features"],
                random_state=42,
                n_jobs=-1
            )
            return cross_val_score(rf,databases["x_train"],databases["y_train"],cv=kfold, scoring="recall_macro").mean()
        case 'svm':
            svm = LinearSVC(
                C=individual["svm_C"],
                max_iter=individual["svm_max_iter"],
                tol=individual["svm_tol"],
                random_state=42
            )
            return cross_val_score(svm,databases["x_train"],databases["y_train"],cv=kfold,scoring="recall_macro").mean()
        case 'knn':
            knn = KNeighborsClassifier(
                n_neighbors=individual["knn_neighbors"],
                weights=individual["knn_weights"],
                metric=individual["knn_metric"],
                # No caso do hiperparâmetro algorithm, ele tem valores que só funcionam com a metric euclidean ou manhattan. 
                # Como o algoritmo genético seleciona aleatoriamente os demais valores de hiperparâmetros, pode acontecer uma quebra do treino do modelo por incompatibilidade.
                # Para utilizar esse hiperparâmetro, remova a opção de cosine das métricas. 
                #algorithm=individual["knn_algorithm"],
                p=individual["knn_p"]
            )
            return cross_val_score(knn,databases["x_train"],databases["y_train"],cv=kfold,scoring="recall_macro").mean()
        case _:
            return "Model not found."

def sort_population(population, fitness):
    # Ordena a população com base no valor de fitness. O reverse=True faz com que a lista seja decrescente.
    combined_lists = list(zip(population, fitness))

    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1], reverse=True)

    sorted_population, sorted_fitness = zip(*sorted_combined_lists)

    return sorted_population, sorted_fitness

def tournament_selection(population, fitness, tournament_size=3):
    # Treinamento por torneio. Com tournament_size=3, vai fazer uma busca na população e trazer 3 indivíduos aleatórios. 
    # Após isso, vai validar entre esses 3 quem tem o maior fitness.
    participants = random.sample(
        list(zip(population, fitness)),
        tournament_size
    )

    winner = max(participants, key=lambda x: x[1])

    return winner[0]

def order_crossover(parent1, parent2):
    # Realiza o cruzamento dos genes do filho com os dos pais, aleatoriamente.
    child = {}

    for key in parent1:
        child[key] = random.choice(
            [parent1[key], parent2[key]]
        )

    return child

def mutate(individual, mutation_probability, model):
    # Caso a chance de mutação ocorra, irá escolher um valor aleatório dentre os hiperparâmetros disponíveis para substituí-lo. 
    hyperparams = HYPERPARAMS[model]
    child = copy.deepcopy(individual)

    if random.random() < mutation_probability:
        gene = random.choice(list(child.keys()))
        child[gene] = random.choice(hyperparams[gene])

    return child