from argparse import ArgumentParser, Namespace
from fractions import Fraction
from pathlib import Path

import numpy as np
from digitar.chord import Chord
from digitar.instrument import PluckedStringInstrument, StringTuning
from digitar.stroke import Velocity
from digitar.synthesis import Synthesizer
from digitar.temporal import MeasuredTimeline, Time
from digitar.track import AudioTrack

from tablature import models

SAMPLING_RATE = 44100


def main() -> None:
    play(parse_args())


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("path", type=Path, help="tablature file (.yaml)")
    parser.add_argument("-o", "--output", type=Path, default=None)
    return parser.parse_args()


def play(args: Namespace) -> None:
    song = models.Song.from_file(args.path)
    tracks = [track.weight * synthesize(track) for track in song.tracks.values()]


def synthesize(track: models.Track) -> np.ndarray:
    synthesizer = Synthesizer(
        instrument=PluckedStringInstrument(
            tuning=StringTuning.from_notes(*track.instrument.tuning),
            damping=track.instrument.damping,
            vibration=Time(track.instrument.vibration),
        ),
        sampling_rate=SAMPLING_RATE,
    )
    audio_track = AudioTrack(synthesizer.sampling_rate)
    timeline = MeasuredTimeline()
    read(track.tablature, synthesizer, audio_track, timeline)
    return apply_effects(audio_track, track.instrument)


def read(
    tablature: models.Tablature,
    synthesizer: Synthesizer,
    audio_track: AudioTrack,
    timeline: MeasuredTimeline,
) -> None:
    beat = Time(seconds=60 / tablature.beats_per_minute)
    for measure in tablature.measures:
        timeline.measure = beat * measure.beats_per_measure
        whole_note = beat * measure.note_value.denominator
        for note in measure.notes:
            stroke = Velocity.up if note.upstroke else Velocity.down
            audio_track.add_at(
                (timeline >> (whole_note * Fraction(note.offset))).instant,
                synthesizer.strum_strings(
                    chord=Chord(note.frets),
                    velocity=stroke(delay=Time(note.arpeggio)),
                    vibration=(Time(note.vibration) if note.vibration else None),
                ),
            )
        next(timeline)
