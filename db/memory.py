# "Pseudo base de données" en mémoire.
# Dans un vrai backend, cette partie sera remplacée par une base SQL (PostgreSQL, SQLite, etc.)
tasks_db = [
    {
        "title": "tache de test",
        "description": "tester la bonne gestion des tâches",
        "done": False
    }
]

# Auto-incrément simple pour générer des IDs uniques.
# Dans une vraie base SQL, ce serait géré automatiquement.
next_id = 1
