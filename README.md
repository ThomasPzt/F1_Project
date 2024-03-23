# F1 Strategy Simulator

## Version 0.6
La version actuelle est encore en développement, donc des erreurs peuvent survenir pendant son utilisation.

## Limitations actuelles
Il convient de noter que le modèle sous-jacent utilisé dans le simulateur peut être trop limité dans certains cas. Par exemple, si les données pour un type de pneu spécifique ne sont pas disponibles pour un circuit ou sont très limitées, cela peut entraîner des erreurs ou des comportements inattendus dans la simulation. Nous prévoyons d'améliorer le modèle pour prendre en compte ces limitations et fournir une expérience de simulation plus réaliste dans les futures versions du projet.

## Description
Le F1 Strategy Simulator est un package Python conçu pour simuler les stratégies de course en Formule 1 pour la saison 2023. Il permet aux utilisateurs de sélectionner un circuit, de choisir un pilote et de simuler la course en fonction des entrées choisies. Le simulateur fournit des informations sur les choix de pneus, les conditions météorologiques et les résultats de la course pour aider les utilisateurs à développer des stratégies optimales pour chaque course.

## Utilisation du simulateur

Pour utiliser le simulateur, exécutez simplement le fichier `interface.py`. Cela lancera l'interface utilisateur où vous pourrez sélectionner le circuit et les pilotes pour la simulation. Assurez-vous d'avoir toutes les dépendances requises installées (voir la section "Requirements" pour plus de détails).

## Couple Circuit-Pilote

Des erreurs persistent dans le déroulé de la simulation, notamment lors du passage des qualifications au déroulement réel de la course. Voici certains couples plus ou moins fonctionnels :

- **Bahrain Grand Prix** et **Lewis Hamilton** 
- **Australian Grand Prix** et **Carlos Sainz** (pas de données pour les pneus SOFT → temps au tour négatif)
- **Monaco Grand Prix** et **Max Verstappen**
- **Monaco Grand Prix** et **Charles Leclerc**
- **Miami Grand Prix** et **Charles Leclerc** (Bug sur les 5 premiers tours)

## Fonctionnalités
- Sélection de Circuit : Choisissez parmi une liste de circuits présentés dans la saison de Formule 1 2023.
- Sélection de Pilote : Choisissez parmi une liste de pilotes participant à la saison 2023.
- Simulation de Course : Simulez la course en fonction des entrées de l'utilisateur, y compris les choix de pneus, les stratégies de carburant et les conditions météorologiques.
- Analyse Stratégique : Analysez les résultats de la course et évaluez les performances des stratégies sélectionnées.

## Requirement
- numpy
- pandas
- PyQt5
- matplotlib
- scikit-learn

## Licence
Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.

## Remerciements
Le F1 Strategy Simulator a été développé en mars 2024 par Thomas Poizot & Esteban Brion.