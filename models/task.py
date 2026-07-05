from typing import Optional
from pydantic import BaseModel

# Modèle de données pour une tâche.
# Pydantic valide automatiquement les types lors de la réception du JSON.
# Chaque champ est typé, ce qui garantit que l'API reçoit des données correctes.
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False
