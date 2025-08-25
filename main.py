
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="English Dictionary API")

class Word(BaseModel):
    definition: str
    type: str  # noun, verb, adjective, etc.

with open("english_dictionary.json", "r") as f:
    dictionary = json.load(f)

@app.get("/")
def home():
    return {"message": "English Dictionary API"}

@app.get("/words")
def list_words():
    return {"words": list(dictionary.keys())}

@app.get("/words/{word}")
def get_word(word: str):
    word = word.lower()
    if word in dictionary:
        return {word: dictionary[word]}
    raise HTTPException(status_code=404, detail="Word not found")

@app.get("/words/type/{word_type}")
def get_words_by_type(word_type: str):
    filtered = {w: d for w, d in dictionary.items() if d["type"].lower() == word_type.lower()}
    if filtered:
        return filtered
    raise HTTPException(status_code=404, detail=f"No words found for type '{word_type}'")

@app.post("/words/{word}")
def add_word(word: str, data: Word):
    word = word.lower()
    if word in dictionary:
        raise HTTPException(status_code=400, detail="Word already exists")
    dictionary[word] = {"definition": data.definition, "type": data.type.lower()}
    with open("english_dictionary.json", "w") as f:
        json.dump(dictionary, f, indent=2)
    return {"message": f"Word '{word}' added"}

@app.delete("/words/{word}")
def delete_word(word: str):
    word = word.lower()
    if word in dictionary:
        del dictionary[word]
        with open("english_dictionary.json", "w") as f:
            json.dump(dictionary, f, indent=2)
        return {"message": f"Word '{word}' deleted"}
    raise HTTPException(status_code=404, detail="Word not found")
