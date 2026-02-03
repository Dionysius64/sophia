import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from typing import List
from graph_manager import GraphManager
from dotenv import load_dotenv

# -----------------
# INIT
# -----------------

load_dotenv()

verbosity_var =  os.getenv("LOG_VERBOSITY")
if verbosity_var.upper() == "DEBUG":
    verbosity_level = logging.DEBUG
elif verbosity_var.upper() == "INFO":
    verbosity_level = logging.INFO
else:
    verbosity_level = logging.INFO

logging.basicConfig(
    level=verbosity_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


NEO4J_NAME = os.getenv("NEO4J_DB_NAME")
NEO4J_USER = os.getenv("NEO4J_DB_USER")
NEO4J_PASS = os.getenv("NEO4J_DB_PASS")
NEO4J_URI = os.getenv("NEO4J_DB_URI")

graph_manager = None

logger.debug("Starting application")
logger.debug(
    "Neo4j config loaded | uri=%s user=%s db=%s",
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_NAME,
)

# -----------------
# API
# -----------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global graph_manager
    try:
        logger.debug("Initializing GraphManager")
        graph_manager = GraphManager(
            NEO4J_URI,
            NEO4J_USER,
            NEO4J_PASS,
        )
        logger.info("GraphManager initialized successfully")
        yield
    except Exception as ex:
        logger.error(f"GraphManagerInitError - {ex}")
        raise
    finally:
        if graph_manager:
            logger.debug("Closing GraphManager")
            graph_manager.close()
            logger.info("GraphManager closed")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    logger.debug("Health check called")
    return {
        "message": "I am alive!",
        "graph_manager": graph_manager is not None,
    }

@app.get("/interpret")
def interpret(
    text: str,
    items: List[str] = Query(...)
):
    logger.debug("Interpret called | text_len=%d items=%d", len(text), len(items))

    result_dict = {
        "input_text": text,
        "num_items": len(items),
    }

    result_list = [item.upper() for item in items]

    return {
        "result_dict": result_dict,
        "result_list": result_list,
    }
