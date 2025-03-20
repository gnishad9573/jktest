import asyncio
import pytest
import httpx
import json
import os
import pytest_asyncio
from httpx import ASGITransport
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from main import app
from database import get_db, engine, AsyncSessionLocal
from db.base_class import Baseclass
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db" 

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Baseclass.metadata.create_all)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    """Create and drop tables for testing."""
    async with engine.begin() as conn:
        await conn.run_sync(Baseclass.metadata.create_all)

    yield 

    async with engine.begin() as conn:
        await conn.run_sync(Baseclass.metadata.drop_all)

async def override_get_db():
    async with AsyncSessionLocal() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="module")
async def auth_headers():
    """Creates a test user and returns authentication headers."""
    async with AsyncSessionLocal() as db:
        async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
            user_response = await async_client.post("/users/", json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass"
            })
            print("User Response:", user_response.status_code, user_response.text)  # Debugging

            assert user_response.status_code == 201, "User creation failed!"

            response = await async_client.post("/login/", data={
                "username": "testuser",
                "password": "testpass"
            })
            assert response.status_code == 200, "Login failed!"

            token = response.json()["access_token"]
            return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncior
async def test_create_book(auth_headers):
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/books/", json={
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Fiction",
            "year_published": 2021,
            "summary": "A great book."
        }, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"

@pytest.mark.asyncior
async def test_get_book_id(auth_headers):
    book_id = 1
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get(f"/books/{book_id}",headers=auth_headers)
        print(response.text)
    assert response.status_code == 200

@pytest.mark.asyncior
async def test_get_book(auth_headers):
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/books/",headers=auth_headers)
    assert response.status_code == 200


@pytest.mark.asyncior
async def test_update_book(auth_headers):
    book_id = 1
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.put(f"/books/{book_id}", json={
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Fiction",
            "year_published": 2021,
            "summary": "A mahana book"
        }, headers=auth_headers)
        assert response.status_code == 200




@pytest.mark.asyncior
async def test_create_review(auth_headers):
    book_id = 1
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post(f"/books/{book_id}/reviews", json={
            "review_text": "string",
            "rating": 1,
            "user_id": 1
        }, headers=auth_headers)
    
    assert response.status_code == 201
   
@pytest.mark.asyncior
async def test_get_book_reviews(auth_headers):
    book_id = 1
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get(f"/books/{book_id}/reviews",headers=auth_headers)
        print(response.text)
    assert response.status_code == 200

@pytest.mark.asyncior
async def test_get_book_summary(auth_headers):
    book_id = 1
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get(f"/books/{book_id}/summary",headers=auth_headers)
    assert response.status_code == 200


@pytest.mark.asyncior
async def test_delete_book(auth_headers):
    book_id = 1
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.delete(f"/books/{book_id}",headers=auth_headers)
        print(response.text)
    assert response.status_code == 200
