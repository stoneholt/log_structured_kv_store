# Simple Python implemention of Bitcask

Implements a key-value store using an append-only log. Modified to be able to do prefix queries on indexes.


# Working with the KV-Store
to run the database webserver, simply run:
```bash
    uvicorn database.server:app --port 8000
```

for development for hot-reloading:
```bash
    uvicorn database.server:app --port 8000 --reload
```

## Operations
- Retrieve a value by key
- Update a value by key
- Insert a value by key
- Prefix search for values by key

# Working with the sample webserver
```bash
    uvicorn app.main:app --port 8001 --reload
```
