from fastapi import FastAPI

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"mensagem": "Olá, FastAPI!"}

@app.get("/saudacao")
def saudacao():
    return{
        "Message" : "Sauve"
    }