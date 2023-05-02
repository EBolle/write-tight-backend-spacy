import spacy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

nlp = spacy.load("en_core_web_sm")

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


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/pos/is-adverb/{word}")
def is_adverb(word: str) -> dict[str, bool]:
    return {"outcome": nlp(word)[0].pos_ == "ADV"}


@app.get("/pos/all/{sentence}")
def get_pos(sentence: str) -> dict[str, list[str]]:
    doc = nlp(sentence.lstrip())

    text = [token.text for token in doc]
    pos = [token.pos_ for token in doc]

    return {"text": text, "pos": pos}
