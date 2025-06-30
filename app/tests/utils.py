from .db import db
from datetime import datetime, timedelta
from bson import ObjectId

def generate_data():
    """Generates sample data."""
    
    # Generate ObjectIds for consistent relationships
    book_ids = [ObjectId() for _ in range(5)]
    client_ids = [ObjectId() for _ in range(3)]
    bookstore_id = ObjectId()
    
    # 5 Books with real titles
    books = [
        {
            "_id": book_ids[0],
            "isbn": "9780451524935",
            "title": "1984",
            "author": "George Orwell",
            "genre": "Dystopian Fiction",
            "price": 12.99,
            "condition": "New"
        },
        {
            "_id": book_ids[1],
            "isbn": "9780060935467",
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "genre": "Fiction",
            "price": 14.50,
            "condition": "Good"
        },
        {
            "_id": book_ids[2],
            "isbn": "9780316769174",
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "genre": "Fiction",
            "price": 13.25,
            "condition": "Good"
        },
        {
            "_id": book_ids[3],
            "isbn": "9780743273565",
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "genre": "Classic Literature",
            "price": 11.75,
            "condition": "Poor"
        },
        {
            "_id": book_ids[4],
            "isbn": "9780061120084",
            "title": "Where the Crawdads Sing",
            "author": "Delia Owens",
            "genre": "Mystery",
            "price": 16.99,
            "condition": "New"
        }
    ]
    
    # 3 Clients
    clients = [
        {
            "_id": client_ids[0],
            "first_name": "Emily",
            "last_name": "Johnson",
            "email": "emily.johnson@email.com",
            "address": "123 Maple Street, Springfield, IL 62701",
            "is_active": True
        },
        {
            "_id": client_ids[1],
            "first_name": "Michael",
            "last_name": "Chen",
            "email": "michael.chen@email.com",
            "address": "456 Oak Avenue, Portland, OR 97205",
            "is_active": True
        },
        {
            "_id": client_ids[2],
            "first_name": "Sarah",
            "last_name": "Williams",
            "email": "sarah.williams@email.com",
            "address": "789 Pine Road, Austin, TX 73301",
            "is_active": True
        }
    ]
    
    # 1 Bookstore
    bookstore = {
        "_id": bookstore_id,
        "name": "Corner Book Haven",
        "address": "321 Literary Lane, Boston, MA 02108",
        "email": "info@cornerbookhaven.com"
    }
    
    # Book Inventory for the bookstore
    book_inventory = [
        {
            "_id": ObjectId(),
            "bookstore_id": bookstore_id,
            "isbn": int(books[0]["isbn"]),  # 1984
            "quantity_available": 3
        },
        {
            "_id": ObjectId(),
            "bookstore_id": bookstore_id,
            "isbn": int(books[1]["isbn"]),  # To Kill a Mockingbird
            "quantity_available": 2
        },
        {
            "_id": ObjectId(),
            "bookstore_id": bookstore_id,
            "isbn": int(books[4]["isbn"]),  # Where the Crawdads Sing
            "quantity_available": 5
        }
    ]
    
    # Current date for calculations
    now = datetime.now()
    
    # Borrowings (mix of bookstore-to-client and client-to-client)
    borrowings = [
        {
            "_id": ObjectId(),
            "borrower_id": client_ids[0],  # Emily borrows from bookstore
            "source_type": "bookstore",
            "source_id": bookstore_id,
            "book_id": book_ids[0],  # 1984
            "borrow_date": now - timedelta(days=10),
            "due_date": now + timedelta(days=4),
            "return_date": None,
            "status": "active"
        },
        {
            "_id": ObjectId(),
            "borrower_id": client_ids[1],  # Michael borrows from Emily (client-to-client)
            "source_type": "client",
            "source_id": client_ids[0],
            "book_id": book_ids[2],  # The Catcher in the Rye
            "borrow_date": now - timedelta(days=5),
            "due_date": now + timedelta(days=9),
            "return_date": None,
            "status": "active"
        },
        {
            "_id": ObjectId(),
            "borrower_id": client_ids[2],  # Sarah borrowed and returned (overdue)
            "source_type": "bookstore",
            "source_id": bookstore_id,
            "book_id": book_ids[1],  # To Kill a Mockingbird
            "borrow_date": now - timedelta(days=25),
            "due_date": now - timedelta(days=11),
            "return_date": now - timedelta(days=3),
            "status": "returned_overdue"
        },
        {
            "_id": ObjectId(),
            "borrower_id": client_ids[0],  # Emily borrows from Sarah (client-to-client)
            "source_type": "client",
            "source_id": client_ids[2],
            "book_id": book_ids[3],  # The Great Gatsby
            "borrow_date": now - timedelta(days=20),
            "due_date": now - timedelta(days=6),
            "return_date": None,
            "status": "overdue"
        }
    ]
    
    # Sales
    sales = [
        {
            "_id": ObjectId(),
            "client_id": client_ids[1],  # Michael buys from bookstore
            "book_id": book_ids[4],  # Where the Crawdads Sing
            "bookstore_id": bookstore_id,
            "amount": 16.99,
            "sale_date": now - timedelta(days=15)
        },
        {
            "_id": ObjectId(),
            "client_id": client_ids[0],  # Emily buys from bookstore
            "book_id": book_ids[0],  # 1984
            "bookstore_id": bookstore_id,
            "amount": 12.99,
            "sale_date": now - timedelta(days=8)
        },
        {
            "_id": ObjectId(),
            "client_id": client_ids[2],  # Sarah buys from bookstore
            "book_id": book_ids[1],  # To Kill a Mockingbird
            "bookstore_id": bookstore_id,
            "amount": 14.50,
            "sale_date": now - timedelta(days=30)
        }
    ]
    
    return {
        "books": books,
        "clients": clients,
        "bookstore": bookstore,
        "book_inventory": book_inventory,
        "borrowings": borrowings,
        "sales": sales
    }


async def populate_db():
    """Populate database with sample data."""
    await clear_db()

    data = generate_data()

    print("Inserting sample data into the database...")
    
    # Insert data into respective collections
    await db.books.insert_many(data["books"])
    await db.clients.insert_many(data["clients"])
    await db.bookstores.insert_one(data["bookstore"])
    await db.book_inventory.insert_many(data["book_inventory"])
    await db.borrowings.insert_many(data["borrowings"])
    await db.sales.insert_many(data["sales"])
    
    print("Sample data inserted successfully!")
    print(f"Created: {len(data['books'])} books, {len(data['clients'])} clients, "
          f"1 bookstore, {len(data['borrowings'])} borrowings, {len(data['sales'])} sales")
    
async def clear_db():
    """Drop everything in the database."""
    print("Clearing database...")
    await db.client.drop_database("bookstore")
    print("Database cleared successfully!")