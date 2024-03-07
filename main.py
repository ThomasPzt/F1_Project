# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd

from model import *
from simulation import *


def main():
    year = [2022, 2023]
    pilote = 44
    circuit = 1
    longueur_circuit = 57
    # Lecture du fichier CSV et création du DataFrame
    X, y = Model.create_dataframe("data.csv", year, circuit, Model.dico)

    # Entraînement du modèle de régression polynomiale
    poly_reg_model, _ = Model.train_polynomial_regression_model(X, y)

    # Affichage des prédictions sur l'ensemble des données
    #Model.plot_polynomial_predictions(poly_reg_model, X, y, Model.dico)

    lap_number_value = 1
    num_laps_value = 0
    compound_value = 'SOFT'
    df_resultat = pd.DataFrame(columns=["DriverNumber", "LapNumber", "LapTime", "Compound",
                                        "NumberOfLapsWithSameCompound", "AirTemp",
                                        "Humidity", "Rainfall", "TrackTemp"])
    stand_tours = []

    while lap_number_value <= longueur_circuit:
        print(f"Tour numéro {lap_number_value}")

        num_simulations = int(input("Combien de tour voulez vous simulez ?"))
        stand = input("Voulez vous faire un arrêt au stand ?(True or False)").lower() == "true"
        if stand:
            compound_value = input("Donnez le type de pneu, SOFT MEDIUM or HARD")
            num_laps_value = 0
            stand_tours.append(lap_number_value)

        # Création d'un DataFrame pour stocker les valeurs initiales de la simulation
        df_simu = pd.DataFrame({
            "DriverNumber": [pilote],
            "LapNumber": [lap_number_value],
            "Compound": [Model.dico[compound_value]],
            "NumberOfLapsWithSameCompound": [num_laps_value]
        })

        # Exécuter la simulation
        if not lap_number_value == 1:
            df_resultat = pd.concat(
                [df_resultat, Simulation.simulation(poly_reg_model, X, df_simu, num_simulations, stand)])
        else:
            df_resultat = Simulation.simulation(poly_reg_model, X, df_simu, num_simulations, stand)

        lap_number_value += num_simulations

    # Plot des temps prédits en fonction du numéro du tour
    for index, row in df_resultat.iterrows():
        if row["DriverNumber"] == pilote:
            color = 'red' if row["LapNumber"] in stand_tours else 'green'
            plt.plot(row["LapNumber"], row["LapTime"], marker='o', color=color)
        else:
            plt.plot(row["LapNumber"], row["LapTime"], marker='o', color='blue')
    plt.xlabel('Lap Number')
    plt.ylabel('Predicted Lap Time (seconds)')
    plt.title('Predicted Lap Time vs. Lap Number')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
