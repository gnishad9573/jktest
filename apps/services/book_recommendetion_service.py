from repositories.book_recommendetion_repository import BookRecommendetion


class BookRecommendetionService:
    def __init__(self, book_recommendetion: BookRecommendetion):
        self.book_recommendetion = book_recommendetion

    async def get_book_recommendetion(self, user_id: int):
        recommended_book = await self.book_recommendetion.recommend_similar_books(user_id)
        return recommended_book