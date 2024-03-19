import random
from .model import *


class Simulation:
    """
    Cette classe fournit des fonctionnalités pour la simulation de courses de Formule 1, y compris la qualification,
    le calcul du temps de course total par pilote, la mise à jour du classement, la récupération des données
    de course pour un tour spécifique, la génération de perturbations aléatoires pour les données météorologiques,
    et la simulation de la course.

    Attributes:
    - liste_pilotes (list): Liste des numéros de pilotes.
    - dico_pilotes (dict): Dictionnaire de correspondance entre les noms des pilotes et leurs numéros.

    Methods:
    - qualification(liste): Simule la qualification en attribuant des temps cumulés aux pilotes.
    - calculate_total_race_time(df_resultat): Calcule le temps total de course par pilote.
    - update_ranking(total_race_time_per_driver): Met à jour le classement en fonction du temps total de course.
    - data(df, pilote, nbr_tour): Récupère les données de course pour un pilote spécifique et un tour donné.
    - rand_constante(air_temp, humidity, track_temp): Génère des perturbations aléatoires pour les données météorologiques.
    - simulation(model, df, df_value_simu, stand): Simule la course en prédisant les temps au tour pour chaque pilote.
    """

    liste_pilotes = [1, 2, 4, 10, 11, 14, 16, 18, 20, 21, 22, 23, 24, 27, 31, 44, 55, 63, 77, 81]
    dico_pilotes = {
        'Alexander ALBON': 23,
        'Pierre GASLY': 10,
        'Lance STROLL': 18,
        'Esteban OCON': 31,
        'Yuki TSUNODA': 22,
        'Logan SARGEANT': 2,
        'ZHOU Guanyu': 24,
        'Lando NORRIS': 4,
        'Carlos SAINZ': 55,
        'Charles LECLERC': 16,
        'Oscar PIASTRI': 81,
        'Sergio PEREZ': 11,
        'Max VERSTAPPEN': 1,
        'Kevin MAGNUSSEN': 20,
        'George RUSSELL': 63,
        'Fernando ALONSO': 14,
        'Nico HULKENBERG': 27,
        'Nyck DE VRIES': 21,
        'Valtteri BOTTAS': 77,
        'Lewis HAMILTON': 44
    }

    @staticmethod
    def qualification(liste):
        """
        Simule la qualification en attribuant des temps cumulés aux pilotes.

        Args:
        - liste (list): Liste des noms des pilotes participants à la qualification.

        Returns:
        - cumulative_times_per_driver_per_lap (dict): Dictionnaire contenant les temps cumulés par pilote.
        """
        cumulative_times_per_driver_per_lap = {}
        time_increment = 0

        for driver_name in liste:
            driver_number = Simulation.dico_pilotes.get(driver_name, None)
            cumulative_times_per_driver_per_lap[driver_number] = time_increment
            time_increment += 3
            break

        return cumulative_times_per_driver_per_lap

    @staticmethod
    def calculate_total_race_time(df_resultat):
        """
        Calcule le temps total de course par pilote.

        Args:
        - df_resultat (DataFrame): Le DataFrame contenant les résultats de la course.

        Returns:
        - total_race_time_per_driver (dict): Dictionnaire contenant les temps totaux de course par pilote.
        """
        cumulative_times_per_driver_per_lap = {}

        for index, row in df_resultat.iterrows():
            driver_number = row["DriverNumber"]
            lap_time = row["LapTime"]
            if driver_number in cumulative_times_per_driver_per_lap:
                cumulative_times_per_driver_per_lap[driver_number].append(lap_time)
            else:
                cumulative_times_per_driver_per_lap[driver_number] = [lap_time]

        total_race_time_per_driver = {}

        for driver_number, lap_times in cumulative_times_per_driver_per_lap.items():
            total_race_time_per_driver[driver_number] = sum(lap_times)

        return total_race_time_per_driver

    @staticmethod
    def update_ranking(total_race_time_per_driver):
        """
        Met à jour le classement en fonction du temps total de course.

        Args:
        - total_race_time_per_driver (dict): Dictionnaire contenant les temps totaux de course par pilote.

        Returns:
        - sorted_driver_names (list): Liste des noms des pilotes classés par ordre de temps total croissant.
        """
        sorted_drivers = sorted(total_race_time_per_driver, key=total_race_time_per_driver.get)
        sorted_driver_names = [pilot_name for pilot_number in sorted_drivers for pilot_name, num in
                               Simulation.dico_pilotes.items() if num == pilot_number]

        return sorted_driver_names

    @staticmethod
    def data(df, pilote, nbr_tour):
        """
        Récupère les données de course pour un pilote spécifique et un tour donné.

        Args:
        - df (DataFrame): Le DataFrame contenant les données de course.
        - pilote (string): Le nom du pilote.
        - nbr_tour (int): Le numéro du tour.

        Returns:
        - data (DataFrame): Les données de course pour le pilote et le tour spécifiés.
        """
        pilote = Simulation.dico_pilotes.get(pilote, None)
        tour = nbr_tour
        while True:
            filtre = (df["DriverNumber"] == pilote) & (df["LapNumber"] == tour)
            data = df.loc[filtre, ["EstimatedFuel", "AirTemp", "Humidity", "Rainfall", "TrackTemp"]]
            if not data.empty:
                return data
            else:
                tour -= 1
                if tour < 1:
                    raise ValueError("No data available for the requested lap number or previous laps.")

    @staticmethod
    def rand_constante(air_temp, humidity, track_temp):
        """
        Génère des perturbations aléatoires pour les données météorologiques.

        Args:
        - air_temp (float): Température de l'air.
        - humidity (float): Humidité.
        - track_temp (float): Température de la piste.

        Returns:
        - air_temp_perturbe (float): Température de l'air perturbée.
        - humidity_perturbe (float): Humidité perturbée.
        - track_temp_perturbe (float): Température de la piste perturbée.
        """
        perturbation_air_temp = random.uniform(-0.3, 0.3)
        perturbation_humidity = random.uniform(-0.5, 0.5)
        perturbation_track_temp = random.uniform(-0.3, 0.3)

        air_temp_perturbe = air_temp + perturbation_air_temp
        humidity_perturbe = humidity + perturbation_humidity
        track_temp_perturbe = track_temp + perturbation_track_temp

        return air_temp_perturbe, humidity_perturbe, track_temp_perturbe

    @staticmethod
    def simulation(model, df, df_value_simu, stand):
        """
        Simule la course en prédisant les temps au tour pour chaque pilote.

        Args:
        - model: Le modèle de prédiction des temps de tour.
        - df (DataFrame): Le DataFrame contenant les données de course.
        - df_value_simu (DataFrame): Le DataFrame contenant les valeurs de simulation pour un pilote et un tour donnés.
        - stand (int): Un indicateur binaire indiquant si le pilote est aux stands (1) ou non (0).

        Returns:
        - simuler (DataFrame): Le DataFrame contenant les données simulées pour chaque pilote.
        """
        simulated_data = []
        pilote = df_value_simu["DriverNumber"].values[0]
        pilote_num = Simulation.dico_pilotes.get(pilote, None)
        tour = df_value_simu["LapNumber"].values[0]
        data = Simulation.data(df, pilote, tour)
        estimated_fuel = data["EstimatedFuel"].values[0]
        air_temp = data["AirTemp"].values[0]
        humidity = data["Humidity"].values[0]
        rainfall = data["Rainfall"].values[0]
        track_temp = data["TrackTemp"].values[0]

        for driver in Simulation.liste_pilotes:
            type_pneu = None
            num_tour_same_type = None
            type_pneu_prec = None
            if driver == pilote_num:
                type_pneu = df_value_simu["Compound"].values[0]
                num_tour_same_type = df_value_simu["NumberOfLapsWithSameCompound"].values[0]
            else:
                pilote_df = pd.DataFrame()
                tour_pilote = tour

                while pilote_df.empty and tour_pilote < 57:
                    pilote_df = df[(df["DriverNumber"] == driver) & (df["LapNumber"] == tour_pilote)]
                    if not pilote_df.empty:
                        type_pneu = pilote_df["Compound"].values[0]
                        num_tour_same_type = pilote_df["NumberOfLapsWithSameCompound"].values[0]
                        if num_tour_same_type > tour:
                            num_tour_same_type = tour
                    else:
                        tour_pilote += 1

                if pilote_df.empty:
                    tour_pilote = tour - 1
                    while pilote_df.empty and tour_pilote >= 0:
                        pilote_df = df[(df["DriverNumber"] == driver) & (df["LapNumber"] == tour_pilote)]
                        if not pilote_df.empty:
                            type_pneu = pilote_df["Compound"].values[0]
                            num_tour_same_type = pilote_df["NumberOfLapsWithSameCompound"].values[0]
                        else:
                            tour_pilote -= 1

                tour_prec = tour_pilote-1
                pilote_df = pd.DataFrame()

                while pilote_df.empty and tour_prec > 1:
                    pilote_df = df[(df["DriverNumber"] == driver) & (df["LapNumber"] == tour_prec)]
                    if not pilote_df.empty:
                        type_pneu_prec = pilote_df["Compound"].values[0]
                    else:
                        tour_prec -= 1

            tmp_tour = Model.predict_lap_time(model, driver, tour, type_pneu, estimated_fuel,
                                              num_tour_same_type,
                                              air_temp, humidity, rainfall, track_temp)

            if type_pneu_prec == type_pneu or type_pneu_prec is None:
                pass
            else:
                tmp_tour += 20

            if stand == 1 and driver == pilote_num:
                tmp_tour += 20
                num_tour_same_type = 0
                stand = 0

            tour_data = {
                "DriverNumber": driver,
                "LapNumber": tour,
                "LapTime": tmp_tour,
                "Compound": type_pneu,
                "NumberOfLapsWithSameCompound": num_tour_same_type,
                "AirTemp": air_temp,
                "Humidity": humidity,
                "Rainfall": rainfall,
                "TrackTemp": track_temp
            }

            simulated_data.append(tour_data)

        simuler = pd.DataFrame(simulated_data)

        return simuler
