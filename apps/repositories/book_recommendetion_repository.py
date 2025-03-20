
import faiss
import numpy as np
from models.book_model import Book
from models.review_model import Review
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

class BookRecommendetion:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_book_embeddings(self):
        """Fetch books from DB and generate embeddings."""
        result = await self.db.execute(select(Book.id, Book.summary))
        books = result.fetchall()

        book_ids = []
        book_embeddings = []

        for book_id, summary in books:
            embedding = embedding_model.encode(summary)
            book_ids.append(book_id)
            book_embeddings.append(embedding)

        index = faiss.IndexFlatL2(len(book_embeddings[0])) 
        index.add(np.array(book_embeddings))

        return book_ids, index
    
    async def recommend_similar_books(self, user_id: int, num_recs: int = 5):
        """Recommend books similar to those rated >3 by a user."""
        # Step 1: Fetch books rated >3 by user
        query = (
            select(Book.id, Book.summary)
            .join(Review)
            .where(Review.user_id == user_id, Review.rating > 3)
        )
        result = await self.db.execute(query)
        user_books = result.fetchall()

        if not user_books:
            return {"message": "No high-rated books found for this user."}

        book_ids, index = await self.generate_book_embeddings()

        recommended_books = set()
        for book_id, summary in user_books:
            embedding = embedding_model.encode(summary).reshape(1, -1)
            _, indices = index.search(embedding, num_recs)

            for idx in indices[0]:
                if book_ids[idx] != book_id: 
                    recommended_books.add(book_ids[idx])
        query = select(Book.id,Book.title, Book.author, Book.genre, Book.summary).where(Book.id.in_(recommended_books))
        result = await self.db.execute(query)
        
        return [{"title": row[0], "author": row[1], "genre": row[2]} for row in result.fetchall()]



    


