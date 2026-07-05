from fastapi import APIRouter, HTTPException
from models.task import Task
from db.memory import tasks_db, next_id

# Router dédié aux tâches.
# Le prefix "/tasks" signifie que toutes les routes définies ici commencent par /tasks.
router = APIRouter(prefix="/tasks", tags=["tasks"])


# ====== CRUD : CREATE ======
# Création d'une nouvelle tâche.
# FastAPI lit le corps JSON, le valide via Task (Pydantic),
# puis nous fournit un objet Python déjà typé.
@router.post("/")
async def create_task(task: Task):
    global next_id
    task_data = task.model_dump()  # conversion du modèle Pydantic en dict
    task_data["id"] = next_id      # ajout d'un ID unique
    next_id += 1
    tasks_db.append(task_data)     # stockage dans la "base"
    return task_data


# ====== CRUD : READ (all) ======
# Lecture de toutes les tâches.
# Retourne simplement la liste complète.
@router.get("/")
async def list_tasks():
    return tasks_db


# ====== CRUD : READ (one) ======
# Lecture d'une tâche en particulier via son ID.
# Si l'ID n'existe pas, on renvoie une erreur HTTP 404.
@router.get("/{task_id}")
async def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ====== CRUD : UPDATE ======
# Mise à jour complète d'une tâche.
# Le corps JSON doit contenir un objet Task complet (PUT = remplacement total).
@router.put("/{task_id}")
async def update_task(task_id: int, updated: Task):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            new_data = updated.model_dump()  # dict validé
            new_data["id"] = task_id         # on conserve l'ID
            tasks_db[index] = new_data       # remplacement dans la liste
            return new_data
    raise HTTPException(status_code=404, detail="Task not found")


# ====== CRUD : DELETE ======
# Suppression d'une tâche via son ID.
# Retourne l'ID supprimé pour confirmation.
@router.delete("/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            deleted = tasks_db.pop(index)
            return {"deleted_id": deleted["id"]}
    raise HTTPException(status_code=404, detail="Task not found")
