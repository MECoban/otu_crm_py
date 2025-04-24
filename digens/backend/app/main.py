from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, users
from .core.database import engine
from .models import base

# Veritabanı tablolarını oluştur
base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digens CRM",
    description="Dijital ürünler için entegre CRM sistemi",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API rotaları
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {
        "message": "Digens CRM API'ye hoş geldiniz",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 