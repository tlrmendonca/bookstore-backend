from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import client

from app.routes.book import router as book_router
from app.routes.bookstore import router as bookstore_router
from app.routes.borrowing import router as borrowing_router
from app.routes.client import router as client_router
from app.routes.sale import router as sale_router
from app.routes.login import router as login_router

# Main app
app = FastAPI(
    title="Bookstore Project",
    description="A simple bookstore API built with FastAPI",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include routers
app.include_router(book_router)
app.include_router(bookstore_router)
app.include_router(borrowing_router)
app.include_router(client_router)
app.include_router(sale_router)
app.include_router(login_router)

# MongoDB connection
async def startup_event():
    try:
        await client.admin.command('ping')
        print("MongoDB connected")

        from .utils.utils import populate_db_with_books, clear_books_collection 
        await clear_books_collection()
        await populate_db_with_books()
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

app.add_event_handler("startup", startup_event)

async def shutdown_event():
    client.close()
    print("MongoDB connection closed")

app.add_event_handler("shutdown", shutdown_event)

# Root and health check endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Bookstore API!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # local host
    uvicorn.run(app, host="0.0.0.0", port=8000)