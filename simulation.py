import random
from model import *


class Simulation:
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
        'Max VERSTAPPEN': 33,
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
        cumulative_times_per_driver_per_lap = {}  # Dictionnaire pour stocker les temps cumulés par pilote
        time_increment = 0  # Incrément de temps initial

        for driver_name in liste:
            driver_number = Simulation.dico_pilotes.get(driver_name, None)
            # Ajout du temps cumulé avec l'incrément actuel pour ce pilote
            cumulative_times_per_driver_per_lap[driver_number] = time_increment
            # Incrément de temps pour le pilote suivant
            time_increment += 3  # Ajout de 3 secondes à chaque pilote
            break  # Sortie de la boucle une fois que le pilote est trouvé

        return cumulative_times_per_driver_per_lap

    @staticmethod
    def data(df, pilote, nbr_tour):
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
        perturbation_air_temp = random.uniform(-0.3, 0.3)
        perturbation_humidity = random.uniform(-0.5, 0.5)
        perturbation_track_temp = random.uniform(-0.3, 0.3)

        air_temp_perturbe = air_temp + perturbation_air_temp
        humidity_perturbe = humidity + perturbation_humidity
        track_temp_perturbe = track_temp + perturbation_track_temp

        return air_temp_perturbe, humidity_perturbe, track_temp_perturbe

    @staticmethod
    def simulation(model, df, df_value_simu, nbr_tour_simule, stand):
        # Déclaration de la liste pour stocker les données simulées pour chaque tour
        simulated_data = []
        # on prends les valeurs pour le pilote remplacé par le joueur
        pilote = df_value_simu["DriverNumber"].values[0]
        tour = df_value_simu["LapNumber"].values[0]

        for tour_simu in range(nbr_tour_simule):
            # on prend les mêmes valeurs pour tous les pilotes
            # récupération des données fixes
            tour_ec = tour + tour_simu
            data = Simulation.data(df, pilote, tour_ec)
            estimated_fuel = data["EstimatedFuel"].values[0]
            air_temp = data["AirTemp"].values[0]
            humidity = data["Humidity"].values[0]
            rainfall = data["Rainfall"].values[0]
            track_temp = data["TrackTemp"].values[0]

            # Ajouter une variation aléatoire aux données
            # air_temp, humidity, track_temp = Simulation.rand_constante(air_temp, humidity, track_temp)

            for driver in Simulation.liste_pilotes:
                if driver == pilote:
                    type_pneu = df_value_simu["Compound"].values[0]
                    num_tour_same_type = df_value_simu["NumberOfLapsWithSameCompound"].values[0] + tour_simu
                else:
                    pilote_df = df[df["DriverNumber"] == driver]
                    type_pneu = pilote_df["Compound"].values[0]
                    num_tour_same_type = pilote_df["NumberOfLapsWithSameCompound"].values[0]
                # Simulation en fonction des données
                tmp_tour = Model.predict_lap_time(model, driver, tour_ec, type_pneu, estimated_fuel,
                                                  num_tour_same_type,
                                                  air_temp, humidity, rainfall, track_temp,
                                                  Model.dico)
                # on a fait un tour en plus
                # tour += 1
                # incrémentation du nombre de tours avec les mêmes pneus
                num_tour_same_type += 1
                # on actualise le type de pneu (change qu'en cas d'arrêt au stand)
                # si arrêt au stand, on réinitialise
                if stand and driver == pilote:
                    print(tmp_tour)
                    tmp_tour += 3  # 3 secondes d'arrêt en moyenne
                    print(tmp_tour)
                    num_tour_same_type = 0
                    stand = False
                    print("arrêt au stand...")
                # Création d'un dictionnaire contenant les valeurs simulées pour ce tour
                tour_data = {
                    "DriverNumber": driver,
                    "LapNumber": tour_ec,
                    "LapTime": tmp_tour,
                    "Compound": type_pneu,
                    "NumberOfLapsWithSameCompound": num_tour_same_type,
                    "AirTemp": air_temp,
                    "Humidity": humidity,
                    "Rainfall": rainfall,
                    "TrackTemp": track_temp
                }

                # Ajout des valeurs simulées à la liste
                simulated_data.append(tour_data)

        # Créer un DataFrame à partir de la liste des données simulées
        simuler = pd.DataFrame(simulated_data)

        return simuler
