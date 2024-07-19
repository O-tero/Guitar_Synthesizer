from dataclasses import dataclass
from typing import self


from digitar.temporal import Hertz

@dataclass(frozen=True)
class Pitch:
    frequency: Hertz
    
    def adjust(self, num_semitones: int) -> Self:
        return Pitch(self.frequency * 2 ** (num_semitones / 12))
    