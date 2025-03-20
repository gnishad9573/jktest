from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.models import SecurityScheme
from fastapi.security import OAuth2PasswordBearer
from routers import book_routes, review_routes, book_summary_generate_routes, users_routes, user_login_routes, book_recommendention_routes
from fastapi.security import OAuth2PasswordRequestForm
from database import init_db, create_database
from auth.auth import create_access_token

app = FastAPI()

app.include_router(book_routes.router)
app.include_router(review_routes.router)
app.include_router(book_summary_generate_routes.router)
app.include_router(users_routes.router)
app.include_router(user_login_routes.router)
app.include_router(book_recommendention_routes.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
@app.on_event("startup")
async def on_startup():
    """Initialize the database on startup"""
    await create_database()
    await init_db()

@app.get("/")
async def hello():
    return {"msg" : " Hello this is JK Tech Test "}
