from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import spacy
from spacy.matcher import Matcher
from pydantic import BaseModel

from patterns import (
    pattern_descriptions,
    ambiguous_openings,
    ambiguous_pronouns,
    ly_adverbs,
    passive_voice,
)

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


class Token(BaseModel):
    text: str
    pos: str
    patternName: str | None = None
    description: str | None = None


# ** Main **


@app.get("/patterns/all/{text}")
def get_all_patterns(text: str) -> list[Token]:
    doc = nlp(text.lstrip())

    text_list = [token.text for token in doc]
    pos_list = [token.pos_ for token in doc]
    patternName_list = [""] * len(doc)

    matcher.add("ambiguousOpenings", [ambiguous_openings])
    matcher.add("ambiguousPronouns", [ambiguous_pronouns])
    matcher.add("passiveVoice", [passive_voice])
    matcher.add("lyAdverbs", [ly_adverbs])

    matches = matcher(doc)

    for match_id, match_start_idx, _ in matches:
        string_id = nlp.vocab.strings[match_id]
        patternName_list[match_start_idx] = string_id

    description_list = [
        pattern_descriptions.get(match, "") for match in patternName_list
    ]

    output = [
        Token(
            text=text,
            pos=pos,
            patternName=patternName,
            description=description,
        )
        for text, pos, patternName, description in zip(
            text_list, pos_list, patternName_list, description_list
        )
    ]

    return output


@app.get("/")
def root():
    return {"message": "Hello World"}
