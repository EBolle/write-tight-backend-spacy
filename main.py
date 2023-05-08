import spacy
from spacy.matcher import Matcher

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize spaCy 

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab) 

# Initialize FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # default live server host and port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Main

@app.get("/patterns/all/{sentence}")
def get_all_patterns(sentence: str) -> dict[str, list[str]]:
    doc = nlp(sentence.lstrip())

    text = [token.text for token in doc]
    pos = [token.pos_ for token in doc]

    return {"text": text, "pos": pos}

@app.get("/")
def root():
    return {"message": "Hello World"}