from PyQt5.QtGui import QFont, QPixmap, QIcon
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, \
    QMessageBox, QHBoxLayout, QButtonGroup, QRadioButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
import requests
import random
from simulation import *
from graphique import *


class ChoixCircuit(QWidget):
    """
    Cette classe fournit un widget permettant à l'utilisateur de choisir un circuit et de lancer une simulation.

    Attributes:
    - LancerSimulationClicked(pyqtSignal): Signal émis lorsque l'utilisateur clique sur le bouton pour lancer la simulation,
      avec le nom du circuit sélectionné comme argument.

    Methods:
    - __init__(circuits, parent=None): Initialise le widget avec une liste de circuits.
    - emit_signal(): Émet le signal LancerSimulationClicked avec le nom du circuit sélectionné.
    """
    LancerSimulationClicked = pyqtSignal(str)

    def __init__(self, circuits, parent=None):
        """
        Initialise le widget ChoixCircuit.

        Args:
        - circuits (list): Liste des noms des circuits disponibles.
        - parent (QWidget): Widget parent (par défaut None).
        """
        super().__init__(parent)
        self.circuits = circuits

        # Création du layout vertical pour organiser les widgets
        layout = QVBoxLayout()

        label_choix_circuit = QLabel("Choisissez votre circuit", self)
        label_choix_circuit.setAlignment(Qt.AlignCenter)
        label_choix_circuit.setFont(QFont("Arial", 30))
        label_choix_circuit.setObjectName("label_message_identifiant")
        layout.addWidget(label_choix_circuit)

        # Ajout d'une liste déroulante pour sélectionner le circuit
        self.circuit_combo = QComboBox(self)
        self.circuit_combo.addItems(self.circuits)
        self.circuit_combo.setObjectName("combo_circuit")
        layout.addWidget(self.circuit_combo)

        # Ajout d'un bouton stylisé pour lancer la simulation
        button_lancer = QPushButton("Continuer", self)
        button_lancer.clicked.connect(self.emit_signal)
        button_lancer.setObjectName("lancer_button")
        layout.addWidget(button_lancer)

        # Application du style CSS
        self.setStyleSheet(
            """
            QLabel#label_message_identifiant {
                color: #333;
            }

            QComboBox#combo_circuit {
                font-size: 18px;
                padding: 10px;
            }

            QPushButton#lancer_button {
                background-color: red;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
            """
        )

        self.setLayout(layout)

    def emit_signal(self):
        """
        Émet le signal LancerSimulationClicked avec le nom du circuit sélectionné.
        """
        selected_circuit = self.circuit_combo.currentText()
        self.LancerSimulationClicked.emit(selected_circuit)


class ChoixDriver(QWidget):
    """
    Cette classe permet de choisir un pilote pour une course sur un circuit spécifié.

    Attributes:
    - LancerClicked (pyqtSignal): Signal émis lors du clic sur le bouton pour lancer la course.

    Methods:
    - __init__(self, circuit, parent=None): Initialise l'interface graphique pour choisir un pilote.
    - emit_signal(self): Émet le signal contenant le pilote sélectionné et le circuit choisi.
    """
    LancerClicked = pyqtSignal(str, str)

    def __init__(self, circuit, parent=None):
        """
        Initialise l'interface de sélection du pilote pour une course sur un circuit donné.

        Args:
        - circuit (str): Le nom du circuit pour lequel choisir le pilote.
        - parent: Le widget parent (par défaut None).
        """
        super().__init__(parent)
        self.setWindowTitle("Choix du pilote")
        self.circuit = circuit

        # Récupérer la liste des pilotes pour le circuit sélectionné depuis le fichier CSV
        self.drivers = list(Simulation.dico_pilotes.keys())

        layout = QVBoxLayout()

        label_pilote = QLabel(f"Choisissez votre pilote pour le circuit {circuit}", self)
        label_pilote.setAlignment(Qt.AlignCenter)  # Centrer le contenu du label
        label_pilote.setFont(QFont("Arial", 30))
        label_pilote.setObjectName("label_message_pilote")
        layout.addWidget(label_pilote)

        # Ajout d'une liste déroulante pour sélectionner le pilote
        self.driver_combo = QComboBox(self)
        self.driver_combo.addItems(self.drivers)
        self.driver_combo.setObjectName("combo_driver")
        layout.addWidget(self.driver_combo)

        # Ajout d'un bouton stylisé pour lancer la simulation
        button_lancer = QPushButton("Lancer la course", self)
        button_lancer.clicked.connect(self.emit_signal)
        button_lancer.setObjectName("lancer_button")
        layout.addWidget(button_lancer)

        # Application du style CSS
        self.setStyleSheet(
            """
            QLabel#label_message_pilote {
                color: #333;
            }

            QComboBox#combo_driver {
                font-size: 18px;
                padding: 10px;
            }

            QPushButton#lancer_button {
                background-color: red;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
            """
        )

        self.setLayout(layout)

    def emit_signal(self):
        """
        Émet un signal avec le pilote sélectionné et le circuit associé lorsque le bouton est cliqué.
        """
        selected_driver = self.driver_combo.currentText()
        self.LancerClicked.emit(selected_driver, self.circuit)


class ChoiceResume(QWidget):
    """
    Cette classe représente l'interface récapitulative permettant de lancer la simulation.
    Elle affiche le nom du circuit sélectionné, le nom du pilote sélectionné ainsi que la photo du pilote le cas échéant.
    Lorsque le bouton "Lancer la course" est cliqué, un signal est émis avec le nom du pilote et le nom du circuit associé.

    Attributes:
    - LancerSimulationClicked (pyqtSignal): Un signal émis lors du clic sur le bouton pour lancer la simulation.

    Methods:
    - __init__(selected_circuit, selected_driver, headshot_url, parent=None): Initialise l'interface récapitulative
      avec le nom du circuit, le nom du pilote et l'URL de la photo du pilote.
    - emit_signal(): Émet un signal avec le pilote sélectionné et le circuit associé lorsque le bouton est cliqué.
    """
    LancerSimulationClicked = pyqtSignal(str, str)

    def __init__(self, selected_circuit, selected_driver, headshot_url, parent=None):
        """
        Initialise l'interface récapitulative pour lancer la simulation.

        Args:
        - selected_circuit (str): Le nom du circuit sélectionné.
        - selected_driver (str): Le nom du pilote sélectionné.
        - headshot_url (str): L'URL de la photo du pilote.
        - parent: Le widget parent (par défaut None).
        """
        super().__init__(parent)

        self.selected_circuit = selected_circuit
        self.selected_driver = selected_driver
        # Création du layout vertical pour organiser les widgets
        layout = QVBoxLayout()

        # Ajout d'un QLabel pour afficher le nom du circuit
        circuit_label = QLabel(f"Nom du circuit : {selected_circuit}", self)
        circuit_label.setAlignment(Qt.AlignCenter)
        circuit_label.setFont(QFont("Arial", 20))
        layout.addWidget(circuit_label)

        # Ajout d'un QLabel pour afficher le nom du pilote
        driver_label = QLabel(f"Nom du pilote : {selected_driver}", self)
        driver_label.setAlignment(Qt.AlignCenter)
        driver_label.setFont(QFont("Arial", 20))
        layout.addWidget(driver_label)

        # Vérification de l'URL avant de faire la requête
        if headshot_url and not pd.isna(headshot_url) and isinstance(headshot_url, str):
            try:
                response = requests.get(headshot_url)
                response.raise_for_status()  # Vérifier si la requête a réussi
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                headshot_label = QLabel(self)
                headshot_label.setPixmap(pixmap)
                headshot_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(headshot_label)
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération de l'image : {e}")

        # Ajout d'un bouton stylisé pour lancer la simulation
        button_lancer = QPushButton("Lancer la course", self)
        button_lancer.clicked.connect(self.emit_signal)
        button_lancer.setObjectName("lancer_button")
        layout.addWidget(button_lancer)

        # Application du style CSS
        self.setStyleSheet(
            """
            QLabel {
                color: #333;
            }

            QPushButton#lancer_button {
                background-color: red;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
            """
        )
        self.setLayout(layout)

    @pyqtSlot()
    def emit_signal(self):
        """
        Émet un signal avec le pilote sélectionné et le circuit associé lorsque le bouton est cliqué.
        """
        self.LancerSimulationClicked.emit(self.selected_driver, self.selected_circuit)


class SimulationQualidfication(QWidget):
    """
    Cette classe représente l'interface de simulation de la qualification.
    Elle affiche la liste des pilotes dans un ordre aléatoire et permet de lancer la course.

    Attributes:
    - LancerCourseClicked (pyqtSignal): Un signal émis lors du clic sur le bouton pour lancer la course.

    Methods:
    - __init__(selected_circuit, selected_driver, parent=None): Initialise l'interface de simulation de la qualification
      avec le nom du circuit sélectionné, le nom du pilote sélectionné et une liste de pilotes dans un ordre aléatoire.
    - simuler_qualification(): Simule un classement aléatoire des pilotes.
    - emit_signal(): Émet un signal pour lancer la course avec le pilote sélectionné, le circuit associé et la liste de pilotes.
    """
    LancerCourseClicked = pyqtSignal(str, str, list)

    def __init__(self, selected_circuit, selected_driver, parent=None):
        """
        Initialise l'interface de simulation de la qualification avec le nom du circuit sélectionné,
        le nom du pilote sélectionné et une liste de pilotes dans un ordre aléatoire.

        Args:
        - selected_circuit (str): Le nom du circuit sélectionné.
        - selected_driver (str): Le nom du pilote sélectionné.
        - parent (QWidget): Le widget parent, par défaut None.
        """
        super().__init__(parent)

        self.selected_circuit = selected_circuit
        self.selected_driver = selected_driver

        self.pilotes_affiches = set()  # Add this line to initialize the set

        # Simulation de la qualification (classement aléatoire)
        self.pilotes = self.simuler_qualification()

        # Création du layout vertical pour organiser les widgets
        layout = QVBoxLayout()

        # Utilisation de QListWidget pour afficher la liste de pilotes
        pilotes_list_widget = QListWidget(self)
        for i, pilote in enumerate(self.pilotes, start=1):
            label_pilote = QLabel(f"{i}. {pilote}", self)
            label_pilote.setAlignment(Qt.AlignCenter)
            label_pilote.setFont(QFont("Arial", 20))

            # Set background color to red if it's the selected driver, otherwise use a different color
            background_color = "red" if pilote == self.selected_driver else "white"
            label_pilote.setStyleSheet(f"background-color: {background_color}; color: black;")

            layout.addWidget(label_pilote)

        # Ajout d'un bouton pour lancer la course
        button_lancer_course = QPushButton("Lancer la course", self)
        button_lancer_course.clicked.connect(self.emit_signal)
        button_lancer_course.setObjectName("lancer_course_button")
        layout.addWidget(button_lancer_course)

        # Application du style CSS
        self.setStyleSheet(
            """
            QListWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 10px;
            }

            QListWidget::item {
                border-bottom: 1px solid #ccc;
                padding: 5px;
            }

            QPushButton#lancer_course_button {
                background-color: green;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
            """
        )

        self.setLayout(layout)

    def simuler_qualification(self):
        """
        Simule un classement aléatoire des pilotes pour la qualification.

        Returns:
        - pilotes (list): Une liste de noms de pilotes dans un ordre aléatoire.
        """
        pilotes = list(Simulation.dico_pilotes.keys())
        random.shuffle(pilotes)
        return pilotes

    @pyqtSlot()
    def emit_signal(self):
        """
        Émet un signal pour lancer la course avec le pilote sélectionné, le circuit associé et la liste de pilotes.
        """
        if self.selected_driver not in self.pilotes_affiches:
            label_pilote = QLabel(f"Nom du pilote : {self.selected_driver}", self)
            label_pilote.setAlignment(Qt.AlignCenter)
            label_pilote.setFont(QFont("Arial", 20))
            self.layout().addWidget(label_pilote)
            self.pilotes_affiches.add(self.selected_driver)

        self.LancerCourseClicked.emit(self.selected_driver, self.selected_circuit, self.pilotes)


class Course(QWidget):
    """
    Widget pour afficher et gérer les conditions de la course, les informations de la course et les choix de pneus.

    Attributes:
    - ChoixPneuClicked (pyqtSignal): Signal émis lorsqu'un choix de pneu est confirmé.

    Methods:
    - __init__: Initialise l'interface des conditions de la course.
    - setup_model: Initialise le modèle pour la prédiction.
    - setup_layout_resume: Configure le layout pour afficher les informations de résumé.
    - setup_layout_tableau: Configure le layout pour afficher les conditions actuelles de la course.
    - layout_graphique: Configure le layout pour afficher les graphiques de classement et de temps prédit.
    - setup_layout_classement_pilotes: Configure le layout pour afficher le classement actuel des pilotes.
    - setup_layout_temps_tour: Configure le layout pour afficher les temps du dernier tour.
    - setup_layout_temps_course: Configure le layout pour afficher les temps de course total.
    - setup_layout_info_pneu: Configure le layout pour afficher le type de pneu actuel.
    - setup_layout_tour_pneu: Configure le layout pour afficher le nombre de tours avec les mêmes pneus.
    - setup_layout_pneu: Configure le layout pour afficher les boutons de choix de pneus.
    - handle_soft_pneu_click: Gère le clic sur le bouton du pneu souple.
    - handle_medium_pneu_click: Gère le clic sur le bouton du pneu medium.
    - handle_hard_pneu_click: Gère le clic sur le bouton du pneu dur.
    - setup_layout_stand: Configure le layout pour afficher l'image et le bouton d'arrêt au stand.
    - handle_stand_button_click: Gère le clic sur le bouton d'arrêt au stand.
    - setup_button_valider_pneu: Configure le bouton pour valider le choix de pneus et lancer le tour.
    - fin_course_top: Configure le layout pour afficher la fin de la course.
    - layout_graphique_fin: Configure le layout pour afficher les graphiques à la fin de la course.
    - simulation: Effectue la simulation de la course.
    - clear_layout: Efface le contenu du layout.
    - emit_signal: Émet un signal lorsqu'un choix de pneu est confirmé.
    """
    ChoixPneuClicked = pyqtSignal(str)

    def __init__(self, selected_circuit, selected_driver, pilotes, parent=None):
        """
        Initialise l'interface des conditions de la course avec le nom du circuit sélectionné,
        le nom du pilote sélectionné et une liste de pilotes.

        Args:
        - selected_circuit (str): Le nom du circuit sélectionné.
        - selected_driver (str): Le nom du pilote sélectionné.
        - pilotes (list): Une liste de noms de pilotes.
        - parent (QWidget): Le widget parent, par défaut None.
        """
        super().__init__(parent)

        self.selected_circuit = selected_circuit
        self.selected_driver = selected_driver
        self.pilotes = pilotes

        self.layout = QVBoxLayout()
        self.layout_superieur = QHBoxLayout()
        self.layout_top_end = QHBoxLayout()
        self.layout_resume = QVBoxLayout()
        self.layout_tableau = QVBoxLayout()
        self.layout_graphiques_H = QHBoxLayout()
        self.layout_mid = QHBoxLayout()
        self.layout_classement_pilotes = QVBoxLayout()
        self.layout_temps_tour = QVBoxLayout()
        self.layout_temps_course = QVBoxLayout()
        self.layout_info_pneu = QVBoxLayout()
        self.layout_tour_pneu = QVBoxLayout()
        self.layout_pneu = QHBoxLayout()

        self.X, self.y = None, None
        self.model = None
        self.data = None
        self.tour = 0
        self.max_laps = 0
        self.num_tour_same_compounds = 0
        self.pneu = 'SOFT'
        self.df_resultat = pd.DataFrame(columns=["DriverNumber", "LapNumber", "LapTime", "Compound",
                                                 "NumberOfLapsWithSameCompound", "AirTemp",
                                                 "Humidity", "Rainfall", "TrackTemp"])
        self.df_simu = pd.DataFrame(columns=["DriverNumber", "LapNumber", "Compound", "NumberOfLapsWithSameCompound"])
        self.stand = 0
        self.stand_tours = []

        self.setup_model()
        self.max_laps = self.X["LapNumber"].max()
        self.data = Simulation.data(self.X, self.selected_driver, 1)

        self.setup_layout_resume()
        self.setup_layout_tableau()
        self.layout.addLayout(self.layout_superieur)

        self.setup_layout_classement_pilotes()
        self.setup_layout_temps_tour()
        self.setup_layout_temps_course()
        self.setup_layout_info_pneu()
        self.setup_layout_tour_pneu()
        self.layout_mid.addLayout(self.layout_classement_pilotes)
        self.layout_mid.addLayout(self.layout_temps_tour)
        self.layout_mid.addLayout(self.layout_temps_course)
        self.layout_mid.addLayout(self.layout_info_pneu)
        self.layout_mid.addLayout(self.layout_tour_pneu)
        self.layout.addLayout(self.layout_mid)

        self.setup_layout_pneu()
        self.layout.addLayout(self.layout_pneu)
        self.setup_button_valider_pneu()

        self.setStyleSheet(
            """
            QLabel {
                color: #333;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
            """
        )

        self.setLayout(self.layout)

    def setup_model(self):
        """
        Initialise le modèle en utilisant les données du fichier CSV.

        """
        self.X, self.y = Model.create_dataframe("data.csv", [2022, 2023], self.selected_circuit)
        self.model = Model.train_polynomial_regression_model(self.X, self.y)

    def setup_layout_resume(self):
        """
        Configure le layout pour afficher les informations de résumé sur le circuit, le pilote
        sélectionné et une éventuelle photo du pilote.

        """
        circuit_label = QLabel(f"Circuit: {self.selected_circuit}", self)
        circuit_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        circuit_label.setFont(QFont("Arial", 20))
        self.layout_resume.addWidget(circuit_label)

        tour_label = QLabel(f"Tour {self.tour} / {int(self.max_laps)}", self)
        tour_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        tour_label.setFont(QFont("Arial", 20))
        tour_label.setStyleSheet("color: red;")
        self.layout_resume.addWidget(tour_label)

        driver_label = QLabel(f"Pilote: {self.selected_driver}", self)
        driver_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        driver_label.setFont(QFont("Arial", 20))
        self.layout_resume.addWidget(driver_label)

        drivers_df = pd.read_csv("combined_result_with_drivers_2023.csv")
        headshot_url = drivers_df.loc[(drivers_df['meeting_name'] == self.selected_circuit) & (
                drivers_df['full_name'] == self.selected_driver), 'headshot_url'].iloc[0]

        if headshot_url and not pd.isna(headshot_url) and isinstance(headshot_url, str):
            try:
                response = requests.get(headshot_url)
                response.raise_for_status()
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                headshot_label = QLabel(self)
                headshot_label.setPixmap(pixmap)
                headshot_label.setAlignment(Qt.AlignCenter)
                self.layout_resume.addWidget(headshot_label)
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération de l'image : {e}")

        self.layout_superieur.addLayout(self.layout_resume)

    def setup_layout_tableau(self):
        """
        Configure le layout pour afficher les conditions actuelles de la course dans un tableau.

        """
        conditions_label = QLabel("Conditions Actuelles de la Course", self)
        conditions_label.setAlignment(Qt.AlignCenter)
        conditions_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout_tableau.addWidget(conditions_label)

        conditions_table = QTableWidget(self)
        conditions_table.setColumnCount(4)
        num_row = 2
        if conditions_table.rowCount() < num_row:
            conditions_table.setRowCount(num_row)

        for index, condition in enumerate(["AirTemp", "Humidity", "Rainfall", "TrackTemp"]):
            condition_value = self.data[condition].values[0] if condition in self.data.columns else "N/A"
            item = QTableWidgetItem(str(condition_value))  # Convertir en chaîne si ce n'est pas déjà le cas
            conditions_table.setItem(0, index, QTableWidgetItem(condition))
            conditions_table.setItem(1, index, item)
        self.layout_tableau.addWidget(conditions_table)
        self.layout_superieur.addLayout(self.layout_tableau)

    def layout_graphique(self):
        """
        Configure le layout pour afficher les graphiques de classement et de temps prédit.

        """
        image_buf_1 = GraphiqueClassement.afficher_classement(self.df_resultat)
        pixmap_1 = QPixmap()
        pixmap_1.loadFromData(image_buf_1.getvalue())
        pixmap_1 = pixmap_1.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)
        label_1 = QLabel()
        label_1.setPixmap(pixmap_1)
        self.layout_graphiques_H.addWidget(label_1)

        image_buf_2 = GraphiqueClassement.afficher_temps_predit(self.df_resultat, self.selected_driver,
                                                                self.stand_tours)
        pixmap_2 = QPixmap()
        pixmap_2.loadFromData(image_buf_2.getvalue())
        pixmap_2 = pixmap_2.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio)
        label_2 = QLabel()
        label_2.setPixmap(pixmap_2)
        self.layout_graphiques_H.addWidget(label_2)
        self.layout_superieur.addLayout(self.layout_graphiques_H)

    def setup_layout_classement_pilotes(self):
        """
        Configure le layout pour afficher le classement actuel des pilotes.

        """
        graphique_label = QLabel("Classement actuel de la course", self)
        graphique_label.setAlignment(Qt.AlignCenter)
        graphique_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout_classement_pilotes.addWidget(graphique_label)

        for i, pilote in enumerate(self.pilotes, start=1):
            label_pilote = QLabel(f"{i}. {pilote}", self)
            label_pilote.setAlignment(Qt.AlignCenter)
            label_pilote.setFont(QFont("Arial", 10))

            background_color = "red" if pilote == self.selected_driver else "white"
            label_pilote.setStyleSheet(f"background-color: {background_color}; color: black;")

            self.layout_classement_pilotes.addWidget(label_pilote)

    def setup_layout_temps_tour(self):
        """
        Configure le layout pour afficher les temps du dernier tour pour chaque pilote.

        """
        graphique_label = QLabel("Temps du dernier tour (sec)", self)
        graphique_label.setAlignment(Qt.AlignCenter)
        graphique_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout_temps_tour.addWidget(graphique_label)
        for pilote in self.pilotes:
            pilote_num = Simulation.dico_pilotes.get(pilote, None)
            if self.tour == 0:
                tmps_tour = 0.0
            else:
                tmps_tour = self.df_resultat[(self.df_resultat["DriverNumber"] == pilote_num) &
                                             (self.df_resultat["LapNumber"] == self.tour)]["LapTime"].values[0]
                tmps_tour = "{:.3f}".format(float(tmps_tour[0]))

            label_tmps = QLabel(f"{tmps_tour}", self)
            label_tmps.setAlignment(Qt.AlignCenter)
            label_tmps.setFont(QFont("Arial", 10))

            background_color = "red" if pilote == self.selected_driver else "white"
            label_tmps.setStyleSheet(f"background-color: {background_color}; color: black;")
            self.layout_temps_tour.addWidget(label_tmps)

    def setup_layout_temps_course(self):
        """
        Configure le layout pour afficher les temps de course total pour chaque pilote.

        """
        graphique_label = QLabel("Temps de course (sec)", self)
        graphique_label.setAlignment(Qt.AlignCenter)
        graphique_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout_temps_course.addWidget(graphique_label)

        total_race_time = Simulation.calculate_total_race_time(self.df_resultat)
        for pilote in self.pilotes:
            if self.tour == 0:
                total_time = 0.0
            else:
                pilote_num = Simulation.dico_pilotes.get(pilote, None)

                total_time = total_race_time[pilote_num][0]

            label_tmps = QLabel(f"{total_time:.3f}", self)
            label_tmps.setAlignment(Qt.AlignCenter)
            label_tmps.setFont(QFont("Arial", 10))

            background_color = "red" if pilote == self.selected_driver else "white"
            label_tmps.setStyleSheet(f"background-color: {background_color}; color: black;")

            self.layout_temps_course.addWidget(label_tmps)

    def setup_layout_info_pneu(self):
        """
        Configure le layout pour afficher le type de pneu actuel pour chaque pilote.

        """
        info_pneu_label = QLabel("Type de pneu", self)
        info_pneu_label.setAlignment(Qt.AlignCenter)
        info_pneu_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout_info_pneu.addWidget(info_pneu_label)

        for pilote in self.pilotes:
            pilote_num = Simulation.dico_pilotes.get(pilote, None)
            if self.tour == 0:
                if pilote == self.selected_driver:
                    pneu = self.pneu
                else:
                    pilote_df = self.X[self.X["DriverNumber"] == pilote_num]
                    type_pneu = pilote_df["Compound"].values[0]
                    pneu = next(key for key, val in Model.dico.items() if val == type_pneu)
            else:
                if pilote == self.selected_driver:
                    pneu = self.pneu
                else:
                    type_pneu = self.df_resultat[
                        (self.df_resultat["DriverNumber"] == pilote_num) & (
                                self.df_resultat["LapNumber"] == self.tour)][
                        "Compound"].values[0]
                    pneu = next(key for key, val in Model.dico.items() if val == type_pneu)

            label_pneu = QLabel(f"{pneu}", self)
            label_pneu.setAlignment(Qt.AlignCenter)
            label_pneu.setFont(QFont("Arial", 10))

            background_color = "red" if pilote == self.selected_driver else "white"
            label_pneu.setStyleSheet(f"background-color: {background_color}; color: black;")
            self.layout_info_pneu.addWidget(label_pneu)

    def setup_layout_tour_pneu(self):
        """
        Configure le layout pour afficher le nombre de tours avec les mêmes pneus pour chaque pilote.

        """
        tour_pneu_label = QLabel("Nombre de tour avec les mêmes pneus", self)
        tour_pneu_label.setAlignment(Qt.AlignCenter)
        tour_pneu_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout_tour_pneu.addWidget(tour_pneu_label)

        for pilote in self.pilotes:
            pilote_num = Simulation.dico_pilotes.get(pilote, None)
            if pilote == self.selected_driver:
                num_tour_same_type = self.num_tour_same_compounds
            else:
                if self.tour == 0:
                    num_tour_same_type = 0
                else:
                    num_tour_same_type = self.df_resultat[
                        (self.df_resultat["DriverNumber"] == pilote_num) & (
                                self.df_resultat["LapNumber"] == self.tour)][
                        "NumberOfLapsWithSameCompound"].values[0]

            label_tpneu = QLabel(f"{num_tour_same_type}", self)
            label_tpneu.setAlignment(Qt.AlignCenter)
            label_tpneu.setFont(QFont("Arial", 10))

            background_color = "red" if pilote == self.selected_driver else "white"
            label_tpneu.setStyleSheet(f"background-color: {background_color}; color: black;")
            self.layout_tour_pneu.addWidget(label_tpneu)

    def setup_layout_pneu(self):
        """
        Configure le layout pour afficher les boutons de choix de pneus.

        """
        pneu_layout = QHBoxLayout()
        button_group = QButtonGroup(self)
        button_group.setExclusive(True)

        for i, pneu_image_path in enumerate(["soft.png", "medium.png", "hard.png"]):
            pneu_button = QRadioButton("", self)
            pneu_button.setIcon(QIcon(pneu_image_path))
            pneu_button.setIconSize(QSize(100, 100))
            pneu_button.setStyleSheet("""
                       QRadioButton {
                           background-color: gray; /* Fond gris */
                           border: none;
                       }
                       QRadioButton:checked {
                           background-color: #45a049; /* Vert */
                       }
                   """)
            pneu_layout.addWidget(pneu_button)
            button_group.addButton(pneu_button)
            if i == 0:
                pneu_button.setChecked(True)

            if i == 0:
                pneu_button.clicked.connect(self.handle_soft_pneu_click)
            elif i == 1:
                pneu_button.clicked.connect(self.handle_medium_pneu_click)
            elif i == 2:
                pneu_button.clicked.connect(self.handle_hard_pneu_click)

        self.layout_pneu.addLayout(pneu_layout)

    def handle_soft_pneu_click(self):
        """
        Gère le clic sur le bouton du pneu soft.

        """
        self.pneu = "SOFT"
        self.num_tour_same_compounds = 0
        print("Pneu sélectionné : Soft")

    def handle_medium_pneu_click(self):
        """
        Gère le clic sur le bouton du pneu medium.

        """
        self.pneu = "MEDIUM"
        self.num_tour_same_compounds = 0
        print("Pneu sélectionné : Medium")

    def handle_hard_pneu_click(self):
        """
        Gère le clic sur le bouton du pneu hard.

        """
        self.pneu = "HARD"
        self.num_tour_same_compounds = 0
        print("Pneu sélectionné : Hard")

    def setup_layout_stand(self):
        """
        Configure le layout pour afficher les images et le bouton d'arrêt au stand.

        """
        stand_layout = QHBoxLayout()

        stand_image = QLabel(self)
        stand_pixmap = QPixmap("stand.png")
        stand_image.setFixedSize(300, 100)
        stand_image.setPixmap(stand_pixmap)
        stand_layout.addWidget(stand_image)

        # stand_layout.addStretch()

        stand_button = QPushButton("Arrêt au stand", self)
        stand_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff; /* Bleu */
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Vert */
            }
        """)
        stand_button.clicked.connect(
            self.handle_stand_button_click)
        stand_layout.addWidget(stand_button)

        stand_image2 = QLabel(self)
        stand_pixmap = QPixmap("stand2.png")
        stand_image2.setFixedSize(300, 100)
        stand_image2.setPixmap(stand_pixmap)
        stand_layout.addWidget(stand_image2)

        self.layout_pneu.addLayout(stand_layout)

    def handle_stand_button_click(self):
        """
        Gère le clic sur le bouton d'arrêt au stand.

        """
        self.stand = 1
        self.stand_tours.append(self.tour+1)
        self.pilotes = Simulation.update_ranking(Simulation.calculate_total_race_time(self.df_resultat))
        self.clear_layout(self.layout)

        self.data = Simulation.data(self.X, self.selected_driver, self.tour)

        self.setup_layout_resume()
        self.setup_layout_tableau()
        self.layout_graphique()
        self.layout.addLayout(self.layout_superieur)

        self.setup_layout_classement_pilotes()
        self.setup_layout_temps_tour()
        self.setup_layout_temps_course()
        self.setup_layout_info_pneu()
        self.setup_layout_tour_pneu()
        self.layout_mid.addLayout(self.layout_classement_pilotes)  # Ajouter le layout principal
        self.layout_mid.addLayout(self.layout_temps_tour)
        self.layout_mid.addLayout(self.layout_temps_course)
        self.layout_mid.addLayout(self.layout_info_pneu)  # Ajouter le layout principal
        self.layout_mid.addLayout(self.layout_tour_pneu)
        self.layout.addLayout(self.layout_mid)

        self.setup_layout_pneu()
        self.layout.addLayout(self.layout_pneu)
        self.setup_button_valider_pneu()

    def setup_button_valider_pneu(self):
        """
        Configure le bouton pour valider le choix de pneus et lancer le tour.

        """
        button_valider_pneu = QPushButton("Valider le choix de pneus et lancer le tour", self)
        button_valider_pneu.clicked.connect(self.simulation)
        self.layout.addWidget(button_valider_pneu)

    def fin_course_top(self):
        """
        Configure le layout pour afficher la fin de la course.

        """
        fin_label = QLabel("FIN DE COURSE")
        fin_label.setAlignment(Qt.AlignCenter)
        fin_label.setFont(QFont("Arial", 35))
        self.layout_resume.addWidget(fin_label)

        position_label = QLabel(f"Vous avez terminé {self.pilotes.index(self.selected_driver)+1}/20", self)
        position_label.setAlignment(Qt.AlignCenter)
        position_label.setFont(QFont("Arial", 20))
        position_label.setStyleSheet("color: red;")
        self.layout_resume.addWidget(position_label)

        self.layout_top_end.addLayout(self.layout_resume)

    def layout_graphique_fin(self):
        """
        Configure le layout pour afficher les graphiques à la fin de la course.

        """
        image_buf_1 = GraphiqueClassement.afficher_classement(self.df_resultat)
        pixmap_1 = QPixmap()
        pixmap_1.loadFromData(image_buf_1.getvalue())
        #pixmap_1 = pixmap_1.scaled(500, 500, aspectRatioMode=Qt.KeepAspectRatio)
        label_1 = QLabel()
        label_1.setPixmap(pixmap_1)
        self.layout_graphiques_H.addWidget(label_1)

        image_buf_2 = GraphiqueClassement.afficher_temps_predit(self.df_resultat, self.selected_driver,
                                                                self.stand_tours)
        pixmap_2 = QPixmap()
        pixmap_2.loadFromData(image_buf_2.getvalue())
        #pixmap_2 = pixmap_2.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio)
        label_2 = QLabel()
        label_2.setPixmap(pixmap_2)
        self.layout_graphiques_H.addWidget(label_2)

        self.layout_superieur.addLayout(self.layout_graphiques_H)

    def simulation(self):
        """
        Effectue la simulation de la course au tour par tour.

        """
        if not self.tour == self.max_laps:
            self.tour += 1
            self.num_tour_same_compounds += 1

            # Création d'un DataFrame pour stocker les valeurs initiales de la simulation
            self.df_simu = pd.DataFrame({
                "DriverNumber": [self.selected_driver],
                "LapNumber": [self.tour],
                "Compound": [Model.dico[self.pneu]],
                "NumberOfLapsWithSameCompound": [self.num_tour_same_compounds]
            })

            # Exécuter la simulation
            if not self.tour == 1:
                self.df_resultat = pd.concat(
                    [self.df_resultat, Simulation.simulation(self.model, self.X, self.df_simu, self.stand)])
            else:
                self.df_resultat = Simulation.simulation(self.model, self.X, self.df_simu, self.stand)

            self.stand = 0

            self.pilotes = Simulation.update_ranking(Simulation.calculate_total_race_time(self.df_resultat))
            self.clear_layout(self.layout)

            self.data = Simulation.data(self.X, self.selected_driver, self.tour)

            self.setup_layout_resume()
            self.setup_layout_tableau()
            self.layout_graphique()
            self.layout.addLayout(self.layout_superieur)

            self.setup_layout_classement_pilotes()
            self.setup_layout_temps_tour()
            self.setup_layout_temps_course()
            self.setup_layout_info_pneu()
            self.setup_layout_tour_pneu()
            self.layout_mid.addLayout(self.layout_classement_pilotes)  # Ajouter le layout principal
            self.layout_mid.addLayout(self.layout_temps_tour)
            self.layout_mid.addLayout(self.layout_temps_course)
            self.layout_mid.addLayout(self.layout_info_pneu)  # Ajouter le layout principal
            self.layout_mid.addLayout(self.layout_tour_pneu)
            self.layout.addLayout(self.layout_mid)

            self.setup_layout_stand()
            self.layout.addLayout(self.layout_pneu)
            self.setup_button_valider_pneu()

        else:
            self.clear_layout(self.layout)

            self.fin_course_top()
            self.layout.addLayout(self.layout_top_end)

            self.layout_graphique_fin()
            self.layout.addLayout(self.layout_superieur)

    def clear_layout(self, layout):
        """
        Efface le contenu du layout.

        Args:
        - layout (QLayout): Le layout à effacer.

        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    @pyqtSlot()
    def emit_signal(self):
        """
        Émet un signal lorsqu'un choix de pneu est confirmé.

        """
        selected_pneu = self.pneu_combo.currentText()
        self.ChoixPneuClicked.emit(selected_pneu)


class HomePage(QMainWindow):
    """
    Classe représentant la page d'accueil du simulateur de stratégie F1.

    Attributes:
    - home_page (QWidget): Le widget représentant la page d'accueil.

    Methods:
    - __init__: Initialise la page d'accueil du simulateur F1.
    - show_circuit_page: Affiche la page de choix de circuit.
    - show_driver_page: Affiche la page de choix de pilote.
    - resumeChoice: Affiche le résumé du choix du pilote.
    - lancer_simulation: Lance la simulation de la qualification.
    - courses: Gère la simulation de la course.
    - lancer_course: Lance la course.
    """
    def __init__(self):
        """
        Initialise la page d'accueil du simulateur F1.

        """
        super().__init__()

        self.setWindowTitle("F1 Strategy Simulator")

        self.home_page = QWidget(self)
        self.setWindowState(Qt.WindowMaximized)

        layout = QVBoxLayout()
        self.home_page.setLayout(layout)

        label_message = QLabel("Bienvenue sur notre simulateur de stratégie F1", self)
        label_message.setAlignment(Qt.AlignCenter)
        label_message.setFont(QFont("Arial", 30))
        label_message.setObjectName("label_message_identifiant")
        layout.addWidget(label_message)

        image_widget = QWidget(self.home_page)
        image_layout = QVBoxLayout(image_widget)
        image_layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_widget)

        image_label = QLabel(self.home_page)
        pixmap = QPixmap("logo.png")
        pixmap = pixmap.scaledToWidth(750, 750)
        image_label.setPixmap(pixmap)

        image_layout.addWidget(image_label)

        layout.addWidget(image_widget)

        button_suivant = QPushButton("Suivant", self.home_page)
        button_suivant.clicked.connect(self.show_circuit_page)
        layout.addWidget(button_suivant)

        button_suivant.setObjectName("home_button")

        self.setStyleSheet(
            """
            QPushButton#home_button {
                background-color: #4CAF50;
                color: white;
                font-size: 30px;
                border: none;
                border-radius: 5px;
                padding: 20px;
                margin: 20px;
            }
            QLabel#label_message_identifiant {
                color: #333;
            }
            """
        )

        self.setCentralWidget(self.home_page)

    @pyqtSlot()
    def show_circuit_page(self):
        """
        Affiche la page de choix de circuit.

        """
        circuits_df = pd.read_csv("combined_result_with_drivers_2023.csv")
        circuits = circuits_df['meeting_name'].unique().tolist()
        circuit_page = ChoixCircuit(circuits, self)

        circuit_page.LancerSimulationClicked.connect(self.show_driver_page)
        self.setCentralWidget(circuit_page)

    @pyqtSlot(str)
    def show_driver_page(self, selected_circuit):
        """
        Affiche la page de choix de pilote.

        Args:
        - selected_circuit (str): Le circuit sélectionné.

        """
        if selected_circuit == "Pre-Season Testing":
            QMessageBox.warning(self, "Erreur", "La simulation n'est pas possible pour Pre-Season Testing.")
            return

        driver_page = ChoixDriver(selected_circuit, self)
        driver_page.LancerClicked.connect(self.resumeChoice)
        self.setCentralWidget(driver_page)

    @pyqtSlot(str, str)
    def resumeChoice(self, selected_driver, selected_circuit):
        """
        Affiche le résumé du choix du pilote.

        Args:
        - selected_driver (str): Le pilote sélectionné.
        - selected_circuit (str): Le circuit sélectionné.

        """
        drivers_df = pd.read_csv("combined_result_with_drivers_2023.csv")
        headshot_url = drivers_df.loc[(drivers_df['meeting_name'] == selected_circuit) & (
                drivers_df['full_name'] == selected_driver), 'headshot_url'].iloc[0]

        resume_page = ChoiceResume(selected_circuit, selected_driver, headshot_url, self)
        resume_page.LancerSimulationClicked.connect(self.lancer_simulation)
        self.setCentralWidget(resume_page)

    @pyqtSlot(str, str)
    def lancer_simulation(self, selected_driver, selected_circuit):
        """
        Lance la simulation de la qualification.

        Args:
        - selected_driver (str): Le pilote sélectionné.
        - selected_circuit (str): Le circuit sélectionné.

        """
        simulation_qualification = SimulationQualidfication(selected_circuit, selected_driver, self)
        simulation_qualification.LancerCourseClicked.connect(self.courses)
        self.setCentralWidget(simulation_qualification)

    @pyqtSlot(str, str, list)
    def courses(self, selected_driver, selected_circuit, pilotes):
        """
        Gère la simulation de la course.

        Args:
        - selected_driver (str): Le pilote sélectionné.
        - selected_circuit (str): Le circuit sélectionné.
        - pilotes (list): La liste des pilotes.

        """
        course_choix = Course(selected_circuit, selected_driver, pilotes, self)
        self.setCentralWidget(course_choix)
        print(f"Course lancée avec le pilote {selected_driver} dans le cricuit {selected_circuit}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: white; }")

    window = HomePage()
    window.show()
    sys.exit(app.exec_())
