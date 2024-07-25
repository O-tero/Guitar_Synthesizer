from dataclasses import dataclass
from fractions import Fraction

from pedalboard.io import AudioFile

from digitar.chord import chord
from digitar.instrument import PluckedStringInstrument, StringTuning
from digitar.stroke import Velocity
from digitar.processing import normalize
from digitar.synthesis import Synthesizer
from digitar.temporal import MeasuredTimeline, Time
from digitar.temporal import Time

BEATS_PER_MINUTE = 75
BEATS_PER_MEASURE = 4
NOTE_VALUE = Fraction(1, 4)


class MeasureTiming:
    BEAT = Time(seconds=60 / BEATS_PER_MINUTE)
    MEASURE = BEAT * BEATS_PER_MEASURE


class Note:
    WHOLE = MeasureTiming.BEAT * NOTE_VALUE.denominator
    SEVEN_SIXTEENTH = WHOLE * Fraction(7, 16)
    FIVE_SIXTEENTH = WHOLE * Fraction(5, 16)
    THREE_SIXTEENTH = WHOLE * Fraction(3, 16)
    ONE_EIGHTH = WHOLE * Fraction(1, 8)
    ONE_SIXTEENTH = WHOLE * Fraction(1, 16)
    ONE_THIRTY_SECOND = WHOLE * Fraction(1, 32)


class StrummingSpeed:
    SLOW = Time.from_milliseconds(40)
    FAST = Time.from_milliseconds(20)
    SUPER_FAST = Time.from_milliseconds(5)


def main() -> None:
    acoustic_guitar = PluckedStringInstrument(
        tuning=StringTuning.from_notes("E2", "A2", "D3", "G3", "B3", "E4"),
        vibration=Time(seconds=10),
        damping=0.498,
    )
    synthesizer = Synthesizer(acoustic_guitar)
    audio_track = AudioTrack(synthesizer.sampling_rate)
    timeline = MeasuredTimeline(measure=MeasureTiming.MEASURE)
    for measure in measures(timeline):
        for stroke in measure:
            audio_track.add_at(
                stroke.instant,
                synthesizer.strum_strings(stroke.chord, stroke.velocity),
            )
    save(audio_track, "diablo.mp3")


def measures(timeline: MeasuredTimeline) -> tuple[tuple[Stroke, ...], ...]:
    return (
        measure_01(timeline),
        measure_02(timeline),
    )


def save(audio_track: AudioTrack, filename: str) -> None:
    with AudioFile(filename, "w", audio_track.sampling_rate) as file:
        file.write(normalize(audio_track.samples))
    print(f"\nSaved file {filename!r}")


@dataclass(frozen=True)
class Stroke:
    instant: Time
    chord: Chord
    velocity: Velocity


if __name__ == "__main__":
    main()
