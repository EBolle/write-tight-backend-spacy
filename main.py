import spacy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

nlp = spacy.load("en_core_web_sm")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501"
    ],  # default live server host and port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/is-adverb/{word}")
def is_adverb(word: str) -> dict[str, bool]:
    return {"outcome": nlp(word)[0].pos_ == "ADV"}
