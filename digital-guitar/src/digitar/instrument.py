from dataclasses import dataclass
from typing import Self

from digitar.pitch import Pitch


@dataclass(frozen=True)
class VibratingString:
    pitch: Pitch

    def press_fret(self, fret_number: int | None = None) -> Pitch:
        if fret_number is None:
            return self.pitch
        return self.pitch.adjust(fret_number)


@dataclass(frozen=True)
class StringTuning:
    strings: tuple[VibratingString, ...]

    @classmethod
    def from_notes(cls, *notes: str) -> Self:
        return cls(
            tuple(
                VibratingString(Pitch.from_scientific_notation(note)) for note in notes
            )
        )
