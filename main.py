from fastapi import FastAPI
from routers.tasks import router as tasks_router

# Création de l'application FastAPI.
# C'est ici qu'on assemble les différentes parties (routers, middleware, config, etc.)
app = FastAPI()

# Inclusion du router des tâches.
# Cela "branche" toutes les routes définies dans routers/tasks.py.
app.include_router(tasks_router)

# Route GET basique pour tester que l'API fonctionne.
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}
