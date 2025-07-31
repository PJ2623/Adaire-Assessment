from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, genre

app = FastAPI(
    title="Adaire Assessment API",
    description="API for managing music genres and sales data.",
    version="1.0.0",
    summary="This API provides endpoints to manage music genres, track sales, and user authentication.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    

app.include_router(auth.router)
app.include_router(genre.router)