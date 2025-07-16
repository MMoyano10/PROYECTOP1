from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
import logging
from .logging_config import setup_logging
import time

Base.metadata.create_all(bind=engine)

# Initialize logging
logger = setup_logging("assettags_service")

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    request_body = await request.body()
    logger.info({
        "event": "request",
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": request_body.decode(errors="replace")
    })
    try:
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        logger.info({
            "event": "response",
            "status_code": response.status_code,
            "url": str(request.url),
            "process_time": process_time,
            "headers": dict(response.headers),
        })
        return response
    except Exception as e:
        logger.error({
            "event": "error",
            "url": str(request.url),
            "error": str(e)
        })
        raise

@app.options("/login")
async def options_login():
    return JSONResponse(content={}, status_code=200)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assettags/", response_model=schemas.AssetTagResponse)
def create_assettag(assettag: schemas.AssetTagCreate, db: Session = Depends(get_db)):
    return crud.create_assettag(db, assettag)

@app.get("/assettags/", response_model=list[schemas.AssetTagResponse])
def read_assettags(db: Session = Depends(get_db)):
    return crud.get_assettags(db)

@app.delete("/assettags/")
def delete_assettag(id_asset: int, id_tag: int, db: Session = Depends(get_db)):
    deleted = crud.delete_assettag(db, id_asset, id_tag)
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset-Tag relation not found")
    return {"message": "Relation deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)