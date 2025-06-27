from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId



def validate_object_id(id_str: str, entity_name: str = "object") -> ObjectId:
    """
    Validate and convert a string ID to MongoDB ObjectId.

    Raises: HTTPException: 400 status if ID format is invalid
    """
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid {entity_name} ID format"
        )
    
import random

async def clear_books_collection():
    """Clear the books collection in the database."""
    from ..db import db
    result = await db.books.delete_many({})

async def populate_db_with_books():
    """Populate the database with 30 sample books."""
    from ..db import db
    from ..models.book import BookCondition
    
    base_titles = ["The Art of", "Introduction to", "Mastering", "Guide to", "Secrets of"]
    subjects = ["Python", "JavaScript", "Data Science", "Machine Learning", "Web Design", "Cooking"]
    authors = ["Smith", "Johnson", "Garcia", "Brown", "Davis", "Wilson"]
    genres = ["Technology", "Science", "Fiction", "Non-Fiction", "Education", "Biography"]
    
    books = []
    for i in range(30):
        # Generate varied ISBN (simplified)
        isbn = f"978{random.randint(1000000000, 9999999999)}"
        
        # Combine random elements for variety
        title = f"{random.choice(base_titles)} {random.choice(subjects)}"
        if i % 3 == 0:  # Add some variation
            title += f" Volume {(i // 3) + 1}"
            
        author = f"{random.choice(['John', 'Jane', 'Mike', 'Sarah', 'David'])} {random.choice(authors)}"
        
        book_data = {
            "isbn": isbn,
            "title": title,
            "author": author,
            "genre": random.choice(genres),
            "price": round(random.uniform(15.99, 89.99), 2),
            "condition": random.choice(list(BookCondition))
        }
        books.append(book_data)
    
    # Insert all books
    await db.books.insert_many(books)
    print(f"Added {len(books)} books to the database")