import os
import uvicorn
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="English Dictionary API")

class Word(BaseModel):
    definition: str
    type: str  # noun, verb, adjective, etc.

JSON_PATH = "english_dictionary.json"

def read_dictionary():
    """Lee el JSON completo bajo demanda."""
    if not os.path.exists(JSON_PATH):
        return {}
    with open(JSON_PATH, "r") as f:
        return json.load(f)

def write_dictionary(dictionary):
    """Guarda el JSON."""
    with open(JSON_PATH, "w") as f:
        json.dump(dictionary, f, indent=2)

@app.get("/")
def home():
    return {"message": "English Dictionary API"}

@app.get("/words")
def list_words():
    dictionary = read_dictionary()
    return {"words": list(dictionary.keys())}

@app.get("/words/{word}")
def get_word(word: str):
    dictionary = read_dictionary()
    word = word.lower()
    if word in dictionary:
        return {word: dictionary[word]}
    raise HTTPException(status_code=404, detail="Word not found")

@app.get("/words/type/{word_type}")
def get_words_by_type(word_type: str):
    dictionary = read_dictionary()
    filtered = {w: d for w, d in dictionary.items() if d["type"].lower() == word_type.lower()}
    if filtered:
        return filtered
    raise HTTPException(status_code=404, detail=f"No words found for type '{word_type}'")

@app.post("/words/{word}")
def add_word(word: str, data: Word):
    dictionary = read_dictionary()
    word = word.lower()
    if word in dictionary:
        raise HTTPException(status_code=400, detail="Word already exists")
    dictionary[word] = {"definition": data.definition, "type": data.type.lower()}
    write_dictionary(dictionary)
    return {"message": f"Word '{word}' added"}

@app.delete("/words/{word}")
def delete_word(word: str):
    dictionary = read_dictionary()
    word = word.lower()
    if word in dictionary:
        del dictionary[word]
        write_dictionary(dictionary)
        return {"message": f"Word '{word}' deleted"}
    raise HTTPException(status_code=404, detail="Word not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)