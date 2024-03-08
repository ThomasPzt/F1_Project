import matplotlib.pyplot as plt
import pandas as pd
from simulation import *


class GraphiqueClassement:

    @staticmethod
    def afficher_classement(df_resultat):
        # Créer un dictionnaire pour stocker les temps cumulés de course au tour par pilote
        cumulative_times_per_driver_per_lap = {}

        # Plot des temps prédits en fonction du numéro du tour
        for index, row in df_resultat.iterrows():
            driver_number = row["DriverNumber"]
            lap_time = row["LapTime"]
            lap_number = row["LapNumber"]

            # Vérifiez si le pilote est déjà dans le dictionnaire
            if driver_number in cumulative_times_per_driver_per_lap:
                # Ajoutez le temps de tour actuel à la liste des temps de course du pilote
                cumulative_times_per_driver_per_lap[driver_number].append(lap_time)
            else:
                # Si le pilote n'est pas dans le dictionnaire, ajoutez-le avec une liste vide
                cumulative_times_per_driver_per_lap[driver_number] = [lap_time]

        # Trouver le nombre total de tours
        num_laps = max(len(times) for times in cumulative_times_per_driver_per_lap.values())

        # Initialiser un DataFrame pour stocker le classement au tour par pilote
        df_ranking = pd.DataFrame(index=range(1, 20 + 1), columns=[])

        # Parcourir chaque tour
        for lap in range(1, num_laps + 1):
            # Créer un dictionnaire pour stocker les temps cumulés par pilote pour ce tour
            lap_cumulative_times = {}
            # Parcourir chaque pilote
            for driver, times in cumulative_times_per_driver_per_lap.items():
                # Vérifier si le pilote a atteint ce tour
                if len(times) >= lap:
                    # Ajouter le temps cumulé de ce tour pour ce pilote
                    lap_cumulative_times[driver] = times[lap - 1]
            # Trier les pilotes pour ce tour en fonction de leur temps cumulé
            sorted_drivers = sorted(lap_cumulative_times, key=lap_cumulative_times.get)
            # Ajouter le classement de ce tour dans le DataFrame
            df_ranking[f'Tour_{lap}'] = sorted_drivers

        # Définir une colormap
        colormap = plt.get_cmap('tab20')

        plt.figure(figsize=(10, 6))

        # Parcourir chaque pilote
        for i, driver in enumerate(Simulation.liste_pilotes):
            positions = []
            for tour in range(1, num_laps + 1):
                # Vérifier si le pilote a participé à ce tour
                if driver in df_ranking[f'Tour_{tour}'].values:
                    # Trouver sa position dans le classement pour ce tour
                    position = df_ranking[f'Tour_{tour}'].values.tolist().index(driver) + 1
                    positions.append(position)
                else:
                    # Si le pilote n'a pas participé à ce tour, ajouter None pour ignorer ce tour
                    positions.append(None)

            plt.plot(range(1, num_laps + 1), positions, marker='o', c='black',
                     markerfacecolor=colormap(i / len(Simulation.liste_pilotes)), markersize=5)

        # Affichage du classement des pilotes
        plt.xlabel('Tour')
        plt.ylabel('Classement des Pilotes')
        plt.title('Classement des Pilotes par Tour')
        #plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def afficher_temps_predit(df_resultat, pilote, stand):
        # Plot des temps prédits en fonction du numéro du tour
        for index, row in df_resultat.iterrows():
            if row["DriverNumber"] == pilote:
                color = 'red' if row["LapNumber"] in stand else 'green'
                plt.plot(row["LapNumber"], row["LapTime"], marker='o', color=color)
            else:
                plt.plot(row["LapNumber"], row["LapTime"], marker='o', color='blue')
        plt.xlabel('Lap Number')
        plt.ylabel('Predicted Lap Time (seconds)')
        plt.title('Predicted Lap Time vs. Lap Number')
        plt.grid(True)
        plt.show()
