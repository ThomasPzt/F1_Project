from PyQt5.QtGui import QFont, QPixmap
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
import requests
import random
from simulation import *


class ChoixCircuit(QWidget):
    LancerSimulationClicked = pyqtSignal(str)

    def __init__(self, circuits, parent=None):
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
        selected_circuit = self.circuit_combo.currentText()
        self.LancerSimulationClicked.emit(selected_circuit)


class ChoixDriver(QWidget):
    LancerClicked = pyqtSignal(str, str)

    def __init__(self, circuit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choix du pilote")
        self.circuit = circuit

        # Récupérer la liste des pilotes pour le circuit sélectionné depuis le fichier CSV
        drivers_df = pd.read_csv("combined_result_with_drivers_2023.csv")
        self.drivers = drivers_df[drivers_df['meeting_name'] == circuit]['full_name'].unique().tolist()

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
        selected_driver = self.driver_combo.currentText()
        self.LancerClicked.emit(selected_driver, self.circuit)


class ChoiceResume(QWidget):
    LancerSimulationClicked = pyqtSignal(str, str)

    def __init__(self, selected_circuit, selected_driver, headshot_url, parent=None):
        super().__init__(parent)

        self.selected_circuit = selected_circuit
        self.selected_driver = selected_driver
        self.model = None
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
        self.LancerSimulationClicked.emit(self.selected_driver, self.selected_circuit)


class SimulationQualidfication(QWidget):
    LancerCourseClicked = pyqtSignal(str, str, list)

    def __init__(self, selected_circuit, selected_driver, parent=None):
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
        # Récupérer la liste des pilotes pour le circuit sélectionné depuis le fichier CSV (vous pouvez ajuster le
        # chemin)
        drivers_df = pd.read_csv("combined_result_with_drivers_2023.csv")
        pilotes = drivers_df[drivers_df['meeting_name'] == self.selected_circuit]['full_name'].tolist()

        # Limiter le nombre de pilotes à 20
        pilotes = pilotes[:20]

        # Simulation d'un classement aléatoire
        random.shuffle(pilotes)
        return pilotes

    @pyqtSlot()
    def emit_signal(self):
        if self.selected_driver not in self.pilotes_affiches:
            # Afficher le nom du pilote uniquement s'il n'a pas encore été affiché
            label_pilote = QLabel(f"Nom du pilote : {self.selected_driver}", self)
            label_pilote.setAlignment(Qt.AlignCenter)
            label_pilote.setFont(QFont("Arial", 20))
            self.layout().addWidget(label_pilote)
            self.pilotes_affiches.add(self.selected_driver)  # Ajouter le pilote à l'ensemble des pilotes déjà affichés

        # Émettre le signal pour lancer la course
        self.LancerCourseClicked.emit(self.selected_driver, self.selected_circuit, self.pilotes)


class ConditionsCourse(QWidget):
    ChoixPneuClicked = pyqtSignal(str)

    def __init__(self, selected_circuit, selected_driver, pilotes, parent=None):
        super().__init__(parent)

        self.selected_circuit = selected_circuit
        self.selected_driver = selected_driver
        self.pilotes = pilotes

        # Utilisez les données pour créer votre modèle
        # Par exemple :
        self.X, self.y = Model.create_dataframe("data.csv", [2022, 2023], self.selected_circuit)

        self.model = Model.train_polynomial_regression_model(self.X, self.y)
        # Model.plot_polynomial_predictions(model, X, y, Model.dico)
        print("Model done")
        # Utilisation de la méthode data pour obtenir les données pour le pilote et le nombre de tours donnés
        self.data = Simulation.data(self.X, self.selected_driver, 20)

        # Création du layout vertical pour organiser les widgets
        layout = QVBoxLayout()

        # Affichage des conditions actuelles de la course
        conditions_label = QLabel("Conditions Actuelles de la Course", self)
        conditions_label.setAlignment(Qt.AlignCenter)
        conditions_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(conditions_label)

        # Ajout d'une table pour afficher les conditions
        conditions_table = QTableWidget(self)
        conditions_table.setColumnCount(2)
        conditions_table.setHorizontalHeaderLabels(["Condition", "Valeur"])

        # Vérifier si la table a suffisamment de lignes
        num_rows = len(["AirTemp", "Humidity", "Rainfall", "TrackTemp"])
        if conditions_table.rowCount() < num_rows:
            conditions_table.setRowCount(num_rows)

        # Ajout des données de conditions
        for index, condition in enumerate(["AirTemp", "Humidity", "Rainfall", "TrackTemp"]):
            condition_value = self.data[condition].values[0] if condition in self.data.columns else "N/A"
            item = QTableWidgetItem(str(condition_value))  # Convertir en chaîne si ce n'est pas déjà le cas
            conditions_table.setItem(index, 0, QTableWidgetItem(condition))
            conditions_table.setItem(index, 1, item)

        layout.addWidget(conditions_table)

        # Ajout d'une liste déroulante pour choisir les pneus
        pneu_label = QLabel("Choisir les pneus:", self)
        pneu_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(pneu_label)

        self.pneu_combo = QComboBox(self)
        self.pneu_combo.addItems(["Pneu1", "Pneu2", "Pneu3"])  # Remplacez par les options réelles
        layout.addWidget(self.pneu_combo)

        # Ajout d'un bouton pour valider le choix
        button_valider_pneu = QPushButton("Valider le choix de pneus", self)
        button_valider_pneu.clicked.connect(self.emit_signal)
        layout.addWidget(button_valider_pneu)

        # Application du style CSS
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

            QComboBox {
                font-size: 18px;
                padding: 10px;
                margin: 10px;
            }
            """
        )

        self.setLayout(layout)

    @pyqtSlot()
    def emit_signal(self):
        selected_pneu = self.pneu_combo.currentText()
        self.ChoixPneuClicked.emit(selected_pneu)


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("F1 Strategy Simulator")

        # Création de la page d'accueil
        self.home_page = QWidget(self)
        self.setWindowState(Qt.WindowMaximized)

        # Création du layout vertical pour organiser les widgets
        layout = QVBoxLayout()
        self.home_page.setLayout(layout)

        label_message = QLabel("Bienvenue sur notre simulateur de stratégie F1", self)
        label_message.setAlignment(Qt.AlignCenter)
        label_message.setFont(QFont("Arial", 30))
        label_message.setObjectName("label_message_identifiant")
        layout.addWidget(label_message)

        # Création du widget QLabel pour afficher l'image
        image_widget = QWidget(self.home_page)
        image_layout = QVBoxLayout(image_widget)
        image_layout.setAlignment(Qt.AlignCenter)  # Centrer le contenu du layout
        layout.addWidget(image_widget)

        # Création du label pour afficher l'image
        image_label = QLabel(self.home_page)
        pixmap = QPixmap("logo.png")
        pixmap = pixmap.scaledToWidth(500, 500)
        image_label.setPixmap(pixmap)

        # Ajout du label au layout centré horizontalement
        image_layout.addWidget(image_label)

        # Ajout du widget contenant le logo au layout vertical principal
        layout.addWidget(image_widget)

        # Ajout d'un bouton pour passer à la page suivante
        button_suivant = QPushButton("Suivant", self.home_page)
        button_suivant.clicked.connect(self.show_circuit_page)
        layout.addWidget(button_suivant)

        # Application du style CSS aux boutons
        button_suivant.setObjectName("home_button")

        # Configuration de la feuille de style CSS
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

        # Affichage de la page d'accueil
        self.setCentralWidget(self.home_page)

    @pyqtSlot()
    def show_circuit_page(self):
        # Récupérer la liste des circuits depuis le fichier CSV
        circuits_df = pd.read_csv("combined_result_with_drivers_2023.csv")
        circuits = circuits_df['meeting_name'].unique().tolist()
        # Créer la page de choix de circuit avec la liste des circuits
        circuit_page = ChoixCircuit(circuits, self)

        circuit_page.LancerSimulationClicked.connect(self.show_driver_page)
        self.setCentralWidget(circuit_page)

    @pyqtSlot(str)
    def show_driver_page(self, selected_circuit):
        if selected_circuit == "Pre-Season Testing":
            QMessageBox.warning(self, "Erreur", "La simulation n'est pas possible pour Pre-Season Testing.")
            return

        # Créer la page de choix de pilote avec la liste des pilotes pour le circuit sélectionné
        driver_page = ChoixDriver(selected_circuit, self)
        driver_page.LancerClicked.connect(self.resumeChoice)
        self.setCentralWidget(driver_page)

    @pyqtSlot(str, str)
    def resumeChoice(self, selected_driver, selected_circuit):
        # Récupérer l'URL de la photo du pilote depuis le fichier CSV
        drivers_df = pd.read_csv("combined_result_with_drivers_2023.csv")
        headshot_url = drivers_df.loc[(drivers_df['meeting_name'] == selected_circuit) & (
                drivers_df['full_name'] == selected_driver), 'headshot_url'].iloc[0]

        resume_page = ChoiceResume(selected_circuit, selected_driver, headshot_url, self)
        resume_page.LancerSimulationClicked.connect(self.lancer_simulation)
        self.setCentralWidget(resume_page)

    @pyqtSlot(str, str)
    def lancer_simulation(self, selected_driver, selected_circuit):
        # Lancer la simulation de la qualification ici
        simulation_qualification = SimulationQualidfication(selected_circuit, selected_driver, self)
        simulation_qualification.LancerCourseClicked.connect(self.conditions_courses)
        self.setCentralWidget(simulation_qualification)

    @pyqtSlot(str, str, list)
    def conditions_courses(self, selected_driver, selected_circuit, pilotes):
        course_choix = ConditionsCourse(selected_circuit, selected_driver, pilotes, self)
        course_choix.ChoixPneuClicked.connect(self.lancer_course)
        self.setCentralWidget(course_choix)
        print(f"Course lancée avec le pilote {selected_driver} dans le cricuit {selected_circuit}")

    def lancer_course(self):
        print("course lancée")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: white; }")

    window = HomePage()
    window.show()
    sys.exit(app.exec_())
