import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from typing import List, Dict, Any
from graph_manager import GraphManager
from dotenv import load_dotenv
load_dotenv()

### INIT ###

NEO4J_NAME = str(os.getenv("NEO4J_DB_NAME"))
NEO4J_USER = str(os.getenv("NEO4J_DB_USER"))
NEO4J_PASS = str(os.getenv("NEO4J_DB_PASS"))
NEO4J_URI = str(os.getenv("NEO4J_DB_URI"))

graph_manager = None


### API ###

@asynccontextmanager
async def lifespan(app: FastAPI):
    graph_manager = GraphManager(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    yield
    graph_manager.close()

app = FastAPI()

@app.get("/health")
def health():
    return {
        "message": "I am alive!",
        "graph_manager": True if graph_manager else False
    }

@app.get("/interpret")
def interpret(
    text: str,
    items: List[str] = Query(...)
):
    # Mocked logic for now
    result_dict = {
        "input_text": text,
        "num_items": len(items)
    }

    result_list = [item.upper() for item in items]

    return {
        "result_dict": result_dict,
        "result_list": result_list
    }
