import uvicorn
from fastapi import FastAPI
from backend.db.engine import engine, Base
from backend.auth import auth


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)


@app.get("/")
def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
