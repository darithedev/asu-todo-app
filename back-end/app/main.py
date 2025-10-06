from fastapi import FastAPI

app = FastAPI()

@app.get(
    "/root",
    tags=["/root"],
    summary="Returns a welcome message",
)
def read_root():
    return {"message": "Welcome to FastAPI!"}