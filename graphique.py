import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO


class GraphiqueClassement:

    liste_pilotes = [1, 2, 4, 10, 11, 14, 16, 18, 20, 21, 22, 23, 24, 27, 31, 44, 55, 63, 77, 81]

    @staticmethod
    def afficher_classement(df_resultat):
        cumulative_times_per_driver_per_lap = {}

        for index, row in df_resultat.iterrows():
            driver_number = row["DriverNumber"]
            lap_time = row["LapTime"]

            if driver_number in cumulative_times_per_driver_per_lap:
                cumulative_times_per_driver_per_lap[driver_number].append(lap_time)
            else:
                cumulative_times_per_driver_per_lap[driver_number] = [lap_time]

        num_laps = max(len(times) for times in cumulative_times_per_driver_per_lap.values())

        df_ranking = pd.DataFrame(index=range(1, 20 + 1), columns=[])

        for lap in range(1, num_laps + 1):
            lap_cumulative_times = {}
            for driver, times in cumulative_times_per_driver_per_lap.items():
                if len(times) >= lap:
                    lap_cumulative_times[driver] = times[lap - 1]
            sorted_drivers = sorted(lap_cumulative_times, key=lap_cumulative_times.get)
            df_ranking[f'Tour_{lap}'] = sorted_drivers

        colormap = plt.get_cmap('tab20')

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, driver in enumerate(GraphiqueClassement.liste_pilotes):
            positions = []
            for tour in range(1, num_laps + 1):
                if driver in df_ranking[f'Tour_{tour}'].values:
                    position = df_ranking[f'Tour_{tour}'].values.tolist().index(driver) + 1
                    positions.append(position)
                else:
                    positions.append(None)

            ax.plot(range(1, num_laps + 1), positions, marker='o', c='black',
                     markerfacecolor=colormap(i / len(GraphiqueClassement.liste_pilotes)), markersize=5)

        # Affichage du classement des pilotes
        ax.set_xlabel('Tour')
        ax.set_ylabel('Classement des Pilotes')
        ax.set_title('Classement des Pilotes par Tour')
        ax.grid(True)

        # Sauvegarde du graphique dans un fichier temporaire
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return buf

    @staticmethod
    def afficher_temps_predit(df_resultat, pilote, stand):
        fig, ax = plt.subplots()

        for index, row in df_resultat.iterrows():
            if row["DriverNumber"] == pilote:
                color = 'red' if row["LapNumber"] in stand else 'green'
                ax.plot(row["LapNumber"], row["LapTime"], marker='o', color=color)
            else:
                ax.plot(row["LapNumber"], row["LapTime"], marker='o', color='blue')

        ax.set_xlabel('Lap Number')
        ax.set_ylabel('Predicted Lap Time (seconds)')
        ax.set_title('Predicted Lap Time vs. Lap Number')
        ax.grid(True)

        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return buf
