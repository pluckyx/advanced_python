from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio
import functools

# 1. CREATE THE APP
app = FastAPI(title="Simple Finder")

# 2. THE PYDANTIC MODEL (Just like 'CharName' in the book)
# This guarantees our API will always return an 'id' and a 'name'.
class Fruit(BaseModel):
    id: int
    name: str

# 3. SETUP STATE (Just like the 'init()' function in the book)
# The book stored the big InvertedIndex and HTML file in 'app.state'. 
# We are doing the same thing, but with a tiny list and a simple HTML string.
def setup_data(app):
    app.state.db = [
        {"id": 1, "name": "Apple"},
        {"id": 2, "name": "Banana"},
        {"id": 3, "name": "Cherry"}
    ]
    app.state.html_page = "<h1>Welcome to Fruit Finder!</h1><p>Go to /docs to search.</p>"

setup_data(app)

# 4. THE SEARCH API (Just like '@app.get('/search')' in the book)
# We tell FastAPI to use our Fruit model to format the response.
@app.get("/search", response_model=list[Fruit])
async def search_fruit(q: str):
    # Loop through our state database and find any fruits that match the query 'q'
    results = []
    for fruit in app.state.db:
        if q.lower() in fruit["name"].lower():
            results.append(fruit)
            
    return results

# 5. THE HTML HOMEPAGE (Just like '@app.get('/')' in the book)
# 'include_in_schema=False' hides this from the /docs page, just like the book did.
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    # Return the raw HTML string we saved in app.state earlier
    return app.state.html_page


async def finder(db, reader, writer):
    pass

async def supervisor(db, host: str, port: int):
    await asyncio.start_server(functools.partial(finder(finder,db)),host,port)
    print(f'Fruit Server running on {host}:{port}')