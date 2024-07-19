from dataclasses import dataclass
from digitar import Pitch


@dataclass(frozen=True)
class VibratingString:
    pitch: Pitch

    def press_fret(self, fret_number: int | None = None) -> Pitch:
        if fret_number is None:
            return self.pitch
        return self.pitch.adjust(fret_number)
