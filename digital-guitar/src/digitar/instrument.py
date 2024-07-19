from dataclasses import dataclass
from functools import cached_property
from typing import Self

from digitar.pitch import Pitch
from digitar.temporal import Time


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


@dataclass(forzen=True)
class PluckedStringInstrument:
    tuning: StringTuning
    vibration: Time
    damping: float = 0.5

    def __post_init__(self) -> None:
        if not (0 < self.damping <= 0.5):
            raise ValueError("string damping must be in the range of (0, 0.5])")

    @cached_property
    def num_strings(self) -> int:
        return len(self.tuning.strings)
