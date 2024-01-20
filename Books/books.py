from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title one", "author": "Author one", "category": "science"},
    {"title": "Title two", "author": "Author two", "category": "science"},
    {"title": "Title three", "author": "Author three", "category": "history"},
    {"title": "Title four", "author": "Author four", "category": "math"},
    {"title": "Title five", "author": "Author five", "category": "math"},
    {"title": "Title six", "author": "Author two", "category": "math"},
]

# GET Requests


@app.get("/")
async def home():
    return {"message": "Heath Check!!"}


@app.get("/api-endpoint")
async def first_api():
    user = "Sidharth"
    return {"message": f"Hello {user}"}


@app.get("/books/list-books")
async def read_all_books():
    return BOOKS


# URL with Path parameter 1
@app.get("/books/id/{book_id}")
async def read_book_by_id(book_id: int):
    return BOOKS[book_id - 1]


# URL with Path parameter 2
@app.get("/books/title/{book_title}")
async def read_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


# URL with query parameter
@app.get("/books/category")
async def read_book_by_category(category: str) -> list[dict]:
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/author")
async def read_all_book_by_author(book_author: str) -> list[dict]:
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return


# URL with path and query parameter
@app.get("/books/author-and-category/{book_author}")
async def read_book_by_author_and_category(
    book_author: str, category: str
) -> list[dict]:
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# POST Requests


@app.post("/books/create-book")
async def create_book(new_book=Body()) -> dict:
    BOOKS.append(new_book)
    return new_book


# PUT Requests


@app.put("/books/update-book")
async def update_book_by_title(updated_book=Body()) -> dict:
    for idx in range(len(BOOKS)):
        if BOOKS[idx].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[idx] = updated_book
    return updated_book


# DELETE Requests


@app.delete("/books/delete-book/{book_title}")
async def delete_book_by_title(book_title: str) -> dict:
    for idx in range(len(BOOKS)):
        if BOOKS[idx].get("title").casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(idx)
            break
    return deleted_book
