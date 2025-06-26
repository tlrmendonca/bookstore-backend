## To run:

#### > locally at port 8000
poetry run uvicorn app.main:app --reload

### Some notes and considerations:

1. This application is for demo purposes only and is not complete.

2. Models used are very simplified, e.g. `Book` is used for everything from creation to retrieval, and perhaps a different pattern using helper models such as `BookCreate` and `BookUpdate` would be more appropriate in a production application.

3. Many of the API methods do not use any *service* layer, which would not be a good practice in a production application, but for the sake of brevity, only a few methods actually utilize a *Router -> Service -> Database* pattern.

4. Auth is literally just for show. In a real scenario, there would be at least roles with permissions and tokens would bear a role rather than just being accepted by default. A login system would kind of be required, but that's out of scope for this demo.

### Structure:
```
/app/
├── models/
│   ├── book.py
│   ├── client.py
│   └── bookstore.py
├── routes/
│   ├── book.py
│   ├── client.py
│   └── bookstore.py
├── services/
│   └── borrowing.py
├── utils/
│   └── utils.py
├── db.py
└── main.py
poetry.lock
pyproject.toml
```