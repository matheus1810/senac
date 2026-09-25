from fastapi import FastAPI

from routes.SobreRoutes import SobreRouter
from routes.EquipamentoRoutes import EquipamentoRouter

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)

app.include_router(SobreRouter)
app.include_router(EquipamentoRouter)
