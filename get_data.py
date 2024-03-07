import pandas as pd
import fastf1
import numpy as np

# Liste des années pour lesquelles vous souhaitez récupérer les données
years_list = [2018, 2019, 2020, 2021, 2022, 2023]  # Ajoutez d'autres années au besoin

# Initialiser une liste pour stocker les DataFrames de chaque course
all_race_dfs = []

# Boucle sur chaque année
for year in years_list:
    # Boucle sur chaque course dans l'année
    for race_info in range(1, 23):  # Mettez le nombre total de courses à la place de 23 si nécessaire
        try:
            # Charger les données de la course
            race = fastf1.get_session(year, race_info, 'R')
            race.load()
        except Exception as e:
            # If an error occurs (e.g., session not found), skip to the next race
            continue
        race.load()

        # Initialiser une liste pour stocker les DataFrames de chaque pilote
        driver_dfs = []

        driver_list = race.drivers

        # Boucle sur chaque pilote
        for driver in driver_list:
            # Récupérer les données des tours pour le pilote actuel`
            print(driver)
            driver_laps = race.laps.pick_driver(driver).pick_quicklaps().reset_index()

            # Vérifier si des données sont disponibles pour le pilote
            if not driver_laps.empty:
                # Récupérer les données de temps au tour, types de pneus et nombre de tours
                driver_laps_data = driver_laps[["LapNumber", "LapTime", "Compound"]]

                # Créer un DataFrame pour les données des tours
                df_laps = pd.DataFrame(driver_laps_data)

                # Ajouter une colonne pour le numéro du pilote
                df_laps['DriverNumber'] = driver

                df_laps['Year'] = year

                # Convertir le temps au tour de timedelta à secondes pour une meilleure lisibilité
                df_laps["LapTime"] = df_laps["LapTime"].dt.total_seconds()

                # Estimer la quantité d'essence embarquée à chaque tour
                initial_fuel = 110  # en kg
                final_fuel = 1  # en kg

                # Calculer la consommation moyenne par tour
                total_laps = df_laps["LapNumber"].values
                if total_laps.size > 0:
                    max_total_laps = np.max(total_laps)
                else:
                    max_total_laps = 1

                average_consumption_per_lap = (initial_fuel - final_fuel) / max(max_total_laps, 1)

                # Ajouter une colonne pour la quantité d'essence estimée à chaque tour
                df_laps['EstimatedFuel'] = initial_fuel - df_laps['LapNumber'] * average_consumption_per_lap
                df_laps['EstimatedFuel'] = df_laps['EstimatedFuel'].clip(lower=0)  # Assurer que la quantité d'essence ne devient pas négative

                # Ajouter une colonne pour le nombre de tours avec le même pneu à chaque tour
                df_laps['NumberOfLapsWithSameCompound'] = df_laps.groupby('Compound').cumcount() + 1

                # Créer une colonne CumulativeLapTime avec la somme cumulative des LapTime
                df_laps['CumulativeLapTime'] = df_laps['LapTime'].cumsum()

                # Charger les informations météorologiques
                weather_info = race.weather_data

                # Initialiser une nouvelle colonne 'Time' dans le DataFrame des tours
                df_laps['Time_seconds'] = np.nan

                # Pour chaque tour, trouver la mesure météorologique la plus proche dans le temps

                # Pour chaque tour, trouver la mesure météorologique la plus proche dans le temps
                for index, row in df_laps.iterrows():
                    closest_time_idx = (
                        np.abs((weather_info['Time'] - pd.to_timedelta(row['CumulativeLapTime'], unit='s'))))

                    # Ajouter une condition pour vérifier si closest_time_idx n'est pas vide
                    if not closest_time_idx.empty:
                        closest_time_idx = closest_time_idx.idxmin()
                        df_laps.at[index, 'Time_seconds'] = float(
                            weather_info.at[closest_time_idx, 'Time'].total_seconds())
                    else:
                        df_laps.at[index, 'Time_seconds'] = np.nan

                # Convertir la colonne 'Time_seconds' en timedelta64[ns]
                df_laps['Time_seconds'] = pd.to_timedelta(df_laps['Time_seconds'], unit='s')

                # Fusionner les DataFrames sur la colonne 'Time_seconds'
                result_df = pd.merge(df_laps, weather_info, left_on='Time_seconds', right_on='Time')

                # Ajouter le DataFrame du pilote actuel à la liste
                driver_dfs.append(result_df)

        # Concaténer tous les DataFrames des pilotes en un seul DataFrame pour la course
        race_df = pd.concat(driver_dfs, ignore_index=True)

        # Ajouter une colonne avec le numéro du circuit
        race_df.insert(0, 'CircuitNumber', race_info)

        # Ajouter le DataFrame de la course actuelle à la liste
        all_race_dfs.append(race_df)

# Concaténer tous les DataFrames des courses en un seul DataFrame
final_combined_df = pd.concat(all_race_dfs, ignore_index=True)

# Enregistrer le DataFrame final dans un fichier CSV
final_combined_df.to_csv('combined_data_all_races.csv', index=False)

# Afficher le DataFrame final
print(final_combined_df)
