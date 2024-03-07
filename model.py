import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# LIEN DE TRAVAIL
# https://data36.com/polynomial-regression-python-scikit-learn/
# https://www.w3schools.com/python/python_ml_decision_tree.asp

class Model:
    # global
    dico = {'SOFT': 0, 'MEDIUM': 1, 'HARD': 2}

    @staticmethod
    def create_dataframe(file_path, year, circuit, dico):
        # Lecture du fichier CSV
        data = pd.read_csv(file_path)
        # Suppression des lignes avec des valeurs manquantes
        df = data.dropna(axis=0, how='any')
        # Filtrage pour le numéro de circuit spécifique et les années 2022 et 2023
        df = df[df['CircuitNumber'] == circuit]
        df = df[(df['Year'] == year[0]) | (df['Year'] == year[1])]

        # Sélection des colonnes pertinentes
        X = df[["DriverNumber", "LapNumber", "Compound", "EstimatedFuel",
                "NumberOfLapsWithSameCompound", "AirTemp", "Humidity",
                "Rainfall", "TrackTemp"]].copy()

        # scalaires pour la colonne "Compound"
        X["Compound"] = X["Compound"].map(dico)

        # Suppression des lignes où Compound est UNKNOWN
        X = X[X['Compound'] != 'UNKNOWN']

        # LapTime -> cible (y)
        y = df["LapTime"]

        return X, y

    @staticmethod
    def train_polynomial_regression_model(X, y, degree=3):
        """
        Entraîne un modèle de régression polynomiale sur l'ensemble de données fourni.

        Args:
        - X (DataFrame): Les features d'entraînement.
        - y (Series): La variable cible.
        - degree (int): Degré du polynôme à utiliser pour la transformation des features.

        Returns:
        - model (LinearRegression): Le modèle entraîné.
        - rmse (float): La racine de l'erreur quadratique moyenne du modèle sur les données d'entraînement.
        """
        # Transformation polynomiale des features
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        poly_features = poly.fit_transform(X)

        # Régression polynomiale sur l'ensemble complet de données
        poly_reg_model = LinearRegression()
        poly_reg_model.fit(poly_features, y)

        # Prédictions sur l'ensemble complet de données
        y_predicted = poly_reg_model.predict(poly_features)

        # Calcul de la racine de l'erreur quadratique moyenne (RMSE)
        rmse = np.sqrt(mean_squared_error(y, y_predicted))

        print("RMSE:", rmse)

        return poly_reg_model, rmse

    ################################################
    @staticmethod
    def plot_polynomial_predictions(model, X, y, dico):
        """
        Réalise les prédictions avec un modèle de régression polynomiale donné et affiche les résultats.

        Args:
        - model: Le modèle de régression polynomiale entraîné.
        - X (DataFrame): Les features pour les prédictions.
        - y (Series): La variable cible pour évaluer les prédictions.
        - dico (dict): Le dictionnaire utilisé pour mapper les valeurs de Compound.

        Returns:
        - None
        """
        # Prédiction des valeurs avec le modèle de régression polynomiale
        poly = PolynomialFeatures(degree=3, include_bias=False)
        y_predicted = model.predict(poly.fit_transform(X))

        # Récupération de NumberOfLapsWithSameCompound à partir de X
        NumberOfLapsWithSameCompound = X["NumberOfLapsWithSameCompound"]

        # Création d'une carte de couleur pour chaque composant
        colors = ['blue', 'green', 'red']

        # Création des sous-graphiques
        fig, axs = plt.subplots(1, len(colors), figsize=(15, 6), sharey=True)
        fig.suptitle("Polynomial prediction for NumberOfLapsWithSameCompound", size=16)

        # Tracé de la prédiction polynomiale pour chaque composant
        for i, color in enumerate(colors):
            compound_data = NumberOfLapsWithSameCompound[X["Compound"] == i]
            y_data = y[X["Compound"] == i]
            y_predicted_data = y_predicted[X["Compound"] == i]
            axs[i].scatter(compound_data, y_data, color=color, label=f'{list(dico.keys())[i]} - Données réelles')
            axs[i].scatter(compound_data, y_predicted_data, color=color, marker='x',
                           label=f'{list(dico.keys())[i]} - Prédiction polynomiale')
            axs[i].set_xlabel('NumberOfLapsWithSameCompound')
            axs[i].legend()

        # Affichage global
        plt.xlabel('NumberOfLapsWithSameCompound')
        plt.ylabel('LapTime')
        plt.show()

    ####################################################################

    @staticmethod
    def predict_lap_time(model, pilote, lap_number, compound, estimated_fuel, num_laps_same_compound, air_temp, humidity,
                         rainfall,
                         track_temp, dico, degree=3):
        """
        Prédit le temps au tour en fonction des caractéristiques spécifiées et affiche le résultat.

        Args:
        - model (LinearRegression): Le modèle de régression polynomiale entraîné.
        - lap_number (int): Le numéro du tour de piste.
        - compound (str): Le type de pneu ('SOFT', 'MEDIUM', ou 'HARD').
        - estimated_fuel (float): Le carburant estimé restant dans le réservoir.
        - num_laps_same_compound (int): Le nombre de tours effectués avec le même type de pneu.
        - air_temp (float): La température de l'air.
        - humidity (float): L'humidité de l'air.
        - rainfall (float): La quantité de pluie.
        - track_temp (float): La température de la piste.
        - driver_number (int): Le numéro du pilote.
        - dico (dict): Le dictionnaire de correspondance entre les types de pneus et les scalaires.

        Returns:
        - None
        """
        # Préparer les données pour la prédiction
        data_for_prediction = pd.DataFrame({"DriverNumber": [pilote],
                                            "LapNumber": [lap_number],
                                            "Compound": [compound],
                                            "EstimatedFuel": [estimated_fuel],
                                            "NumberOfLapsWithSameCompound": [num_laps_same_compound],
                                            "AirTemp": [air_temp],
                                            "Humidity": [humidity],
                                            "Rainfall": [rainfall],
                                            "TrackTemp": [track_temp]})

        # Prédire le temps au tour
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        lap_time_prediction = model.predict(poly.fit_transform(data_for_prediction))

        # Convertir le temps en minutes et secondes
        minutes = int(lap_time_prediction[0] // 60)
        secondes = int(lap_time_prediction[0] % 60)

        # Afficher le temps au tour prédit
        #print(f"Prédiction - Temps au tour : {minutes} min {secondes} sec")

        return lap_time_prediction
