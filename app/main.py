from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse


from app.api.v1 import users, specialists, slots, appointments

app = FastAPI(title="Smart Queue API")

app.include_router(users.router, prefix="/api/v1")
app.include_router(specialists.router, prefix="/api/v1")
app.include_router(slots.router, prefix="/api/v1")
app.include_router(appointments.router, prefix="/api/v1")


app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("app/templates/index.html")

