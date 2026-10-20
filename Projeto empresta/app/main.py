from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path

from routes.SobreRoutes import SobreRouter
from routes.EquipamentoRoutes import EquipamentoRouter
from routes.UsuarioRoutes import UsuarioRouter
from routes.authroutes import AuthRouter
from routes.EmprestimoRoutes import EmprestimoRouter

app = FastAPI(
    title="Empresta",
    description="Gerenciamento de empréstimos de equipamentos com permissões por perfil",
    version="1.0.0"
)

app.include_router(SobreRouter)
app.include_router(EquipamentoRouter)
app.include_router(UsuarioRouter)
app.include_router(AuthRouter)
app.include_router(EmprestimoRouter)


@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse("/ui/login.html")


app.mount("/ui", StaticFiles(directory=Path(__file__).resolve().parents[2] / "Front", html=True), name="frontend")
