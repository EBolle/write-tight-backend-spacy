import spacy
from spacy.matcher import Matcher

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from patterns import (
    description,
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


# ** Main **


@app.get("/patterns/all/{text}")
def get_all_patterns(text: str) -> dict[str, list[str]]:
    doc = nlp(text.lstrip())

    output = {
        "text": [token.text for token in doc],
        "pos": [token.pos_ for token in doc],
        "patternName": [""] * len(doc),
    }

    matcher.add("ambiguousOpenings", [ambiguous_openings])
    matcher.add("ambiguousPronouns", [ambiguous_pronouns])
    matcher.add("passiveVoice", [passive_voice])
    matcher.add("lyAdverbs", [ly_adverbs])

    matches = matcher(doc)

    for match_id, match_start_idx, _ in matches:
        string_id = nlp.vocab.strings[match_id]
        output["patternName"][match_start_idx] = string_id

    output["description"] = [
        description.get(match, "") for match in output["patternName"]
    ]

    return output


@app.get("/")
def root():
    return {"message": "Hello World"}
