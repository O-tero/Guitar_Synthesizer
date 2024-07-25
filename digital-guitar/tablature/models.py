from pathlib import Path
from typing import Optional, Self

import yaml
from pydantic import BaseModel
from pydantic import BaseModel, HttpUrl, NonNegativeFloat, model_validator


class Track(BaseModel):
    url: Optional[HttpUrl] = None
    weight: Optional[NonNegativeFloat] = 1.0
    instrument: Instrument
    tablature: Tablature

    @model_validator(mode="after")
    def check_frets(self) -> Self:
        num_strings = len(self.instrument.tuning)
        for measure in self.tablature.measures:
            for notes in measure.notes:
                if len(notes.frets) != num_strings:
                    raise ValueError("Incorrect number of frets")
        return self


class Song(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    tracks: dict[str, Track]

    @classmethod
    def from_file(cls, path: str | Path) -> Self:
        with Path(path).open(encoding="utf-8") as file:
            return cls(**yaml.safe_load(file))
