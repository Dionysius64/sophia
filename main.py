from fastapi import FastAPI, Query
from typing import List, Dict, Any

app = FastAPI()

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
