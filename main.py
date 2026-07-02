from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# création de l'API
app = FastAPI()

# ===== tests GET basiques =====
# fonction de route sur requete get sur la racine (localhost/)
@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}

# une variable dans le chemin peux être utilisé comme argument de la callback (path parameter). l'argument q (query parameter) peut également être donné dans l'url en ajoutant une "query" : `?q=<votre input pour q>`
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}



# ===== tests CRUD =====
# on créé un objet pour définir des types précis et vérifiés automatiquement par pydantic à la reception du json
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

tasks_db = []
next_id = 1

# callback pour créer des instances de Tasks qui seront stockées dans tasks_db (à terme dans une base SQL)
@app.post("/tasks")
async def create_task(task: Task):
    global next_id
    task_data = task.model_dump()
    task_data["id"] = next_id
    next_id += 1
    tasks_db.append(task_data)
    return task_data

# lecture de toutes la tasks_db par un GET
@app.get("/tasks")
async def list_tasks():
    return tasks_db

# lecture d'une task en particulier avc task_id
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# mettre à jour une task en particulier
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated: Task):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            new_data = updated.model_dump()
            new_data["id"] = task_id
            tasks_db[index] = new_data
            return new_data
    raise HTTPException(status_code=404, detail="Task not found")

# suppression d'une task en particulier
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            deleted = tasks_db.pop(index)
            return {"deleted_id": deleted["id"]}
    raise HTTPException(status_code=404, detail="Task not found")

